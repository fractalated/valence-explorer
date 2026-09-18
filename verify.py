#!/usr/bin/env python3
"""Check the element data in index.html against primary sources.

Sources
  NIST Atomic Spectra Database -- ground-state electron configurations for the
    neutral atoms (Z 1-108) and for every ion charge state it lists.
    https://physics.nist.gov/PhysRefData/ASD/ionEnergy.html
  PubChem (NIH) periodic table -- names, symbols and documented oxidation states.
    https://pubchem.ncbi.nlm.nih.gov/rest/pug/periodictable/CSV

Needs python3, node and a network connection.  Run:  python3 verify.py
"""
import csv, io, json, re, subprocess, sys, tempfile, urllib.request, os

NIST = ("https://physics.nist.gov/cgi-bin/ASD/ie.pl?spectra=H-Og&units=1&format=2"
        "&order=0&at_num_out=on&el_name_out=on&seq_out=on&shells_out=on&conf_out=on"
        "&level_out=on&ion_charge_out=on&e_out=0&submit=Retrieve+Data")
PUBCHEM = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/periodictable/CSV"
TOKEN = re.compile(r'^(\d)([spdfgh])(\d*)$')


def fetch(url):
    # NIST refuses urllib's default user agent with a 403
    req = urllib.request.Request(url, headers={"User-Agent": "valence-explorer-verify/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read().decode("utf-8", "replace")


def run_js(pure, tail):
    fd, path = tempfile.mkstemp(suffix=".js")
    os.write(fd, (pure + tail).encode("utf-8")); os.close(fd)
    try:
        return json.loads(subprocess.check_output(["node", path]))
    finally:
        os.unlink(path)


def pure_part(filename, marker, needle):
    """The chemistry code from the top of a page's script, with the DOM code cut off."""
    src = open(filename, encoding="utf-8").read()
    script = [s for s in re.findall(r"<script>(.*?)</script>", src, re.S) if needle in s][0]
    return (script.split(marker)[0]
            .replace("(function(){", "").replace('"use strict";', ""))


def app_data():
    """index.html: full element data plus the ion chemistry."""
    return run_js(pure_part("index.html", "/* ---- build the table ---- */", "var E = ["), """
console.log(JSON.stringify(DATA.map(function(d){
  var ion = ionOf(d);
  return {z:d.z, sym:d.sym, name:d.name, period:d.period, group:d.group, block:d.block,
          shells:d.shells, occ:d.occ, ionCharge:ionCharge(d),
          ionShells: ion ? ion.shells : null};
})));
""")


def orbital_data():
    """orbitals.html keeps its own copy of the element data; this catches drift."""
    if not os.path.exists("orbitals.html"):
        return None
    return run_js(pure_part("orbitals.html", "/* ---------- orbital shapes ---------- */",
                            'var E = "H Hydrogen'), """
console.log(JSON.stringify(E.map(function(e){
  return {z:e.z, sym:e.sym, name:e.name, occ:e.occ};
})));
""")


def parse_nist(raw):
    def unwrap(v):
        m = re.match(r'^="+(.*?)"+$', v.strip())
        return m.group(1) if m else v.strip().strip('"')
    neutral, ions = {}, {}
    for line in io.StringIO(raw):
        if line.startswith("At. num") or not line.strip():
            continue
        parts = [unwrap(p) for p in next(csv.reader([line]))]
        if len(parts) < 6:
            continue
        try:
            z = int(parts[0])
        except ValueError:
            continue
        if parts[1] in ("0", ""):
            neutral[z] = {"name": parts[2], "sym": parts[3], "shells": parts[4]}
        else:
            ions[(z, parts[1])] = parts[4]
    return neutral, ions


def expand(cfg, cores, depth=0):
    """NIST shorthand such as '[Xe].4f7.5d.6s2' -> {'4f': 7, '5d': 1, ...}"""
    occ = {}
    if depth > 12:
        raise ValueError("core nesting too deep")
    for tok in cfg.replace("(", "").replace(")", "").split("."):
        tok = tok.strip()
        if not tok:
            continue
        if tok.startswith("["):
            for k, v in expand(cores[tok.strip("[]")], cores, depth + 1).items():
                occ[k] = occ.get(k, 0) + v
            continue
        m = TOKEN.match(tok)
        if not m:
            raise ValueError("unparsed token " + tok)
        key = m.group(1) + m.group(2)
        occ[key] = occ.get(key, 0) + (int(m.group(3)) if m.group(3) else 1)
    return occ


def shells(occ):
    sh = [0] * 8
    for k, v in occ.items():
        sh[int(k[0]) - 1] += v
    while sh and sh[-1] == 0:
        sh.pop()
    return sh


def main():
    app = app_data()
    neutral, ions = parse_nist(fetch(NIST))
    pub = {int(r["AtomicNumber"]): r for r in csv.DictReader(io.StringIO(fetch(PUBCHEM)))}
    cores = {v["sym"]: v["shells"] for v in neutral.values()}

    fails, counts = [], {"neutral": 0, "ion": 0, "name": 0, "ox": 0, "predicted": []}
    for e in app:
        z, sym = e["z"], e["sym"]
        p = pub[z]
        if (p["Symbol"], p["Name"].lower()) == (sym, e["name"].lower()):
            counts["name"] += 1
        else:
            fails.append(f"{sym} name/symbol: page has {sym}/{e['name']}, PubChem has {p['Symbol']}/{p['Name']}")

        charge = e["ionCharge"]
        if charge:
            listed = [x.strip().lstrip("+") for x in (p["OxidationStates"] or "").split(",") if x.strip()]
            want = str(charge) if charge < 0 else str(charge)
            if want in listed:
                counts["ox"] += 1
            else:
                fails.append(f"{sym} ion {charge:+d} is not among PubChem's states ({p['OxidationStates']})")

        n = neutral.get(z)
        if not n:
            counts["predicted"].append(z)
            continue
        occ = expand(n["shells"], cores)
        if shells(occ) == e["shells"] and occ == {k: v for k, v in e["occ"].items() if v}:
            counts["neutral"] += 1
        else:
            fails.append(f"{sym} neutral: page {e['shells']}, NIST {shells(occ)} ({n['shells']})")

        if charge and charge > 0 and (z, "+%d" % charge) in ions:
            iocc = expand(ions[(z, "+%d" % charge)], cores)
            if shells(iocc) == e["ionShells"]:
                counts["ion"] += 1
            else:
                fails.append(f"{sym}{charge:+d}: page {e['ionShells']}, NIST {shells(iocc)}")

    orb = orbital_data()
    if orb is None:
        print("orbitals.html                        : not present, skipped")
    else:
        drift = [f"{a['sym']}: {a['occ']} vs {b['occ']}"
                 for a, b in zip(app, orb)
                 if (a["z"], a["sym"], a["name"]) != (b["z"], b["sym"], b["name"])
                 or {k: v for k, v in a["occ"].items() if v} != {k: v for k, v in b["occ"].items() if v}]
        if drift:
            fails += ["orbitals.html differs from index.html -- " + d for d in drift]
        print(f"orbitals.html agreeing with index.html: {len(orb) - len(drift)} / {len(orb)}")

    print(f"neutral configurations matching NIST : {counts['neutral']}")
    print(f"ion configurations matching NIST     : {counts['ion']}")
    print(f"names and symbols matching PubChem   : {counts['name']} / {len(app)}")
    print(f"ion charges that are documented states: {counts['ox']}")
    print(f"predicted (no NIST measurement)      : {counts['predicted']}")
    if fails:
        print("\nFAILURES")
        for f in fails:
            print(" ", f)
    else:
        print("\nno discrepancies")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
