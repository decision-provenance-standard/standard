#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Generate every file that repeats the Conformance Level criteria, from one source.

All paths are relative to the kit folder, the folder that holds declaration/ and skill/.

Sources (edit these):
  declaration/criteria.json               the criteria, levels and the level rule
  declaration/dps-declaration.schema.json the declaration format (and its fixed statements)
  badges/*.svg                            the badge art (full mode only)
  the TEMPLATES below                     the plain-text declaration shapes

Generated (never edit by hand):
  declaration/prompt.md                                   the "Write it with your AI" prompt
  skill/dps-declaration/references/criteria.md            the criteria, readable
  skill/dps-declaration/references/criteria.json          byte copy of the source
  skill/dps-declaration/references/dps-declaration.schema.json  byte copy of the source
  badges.html, between the GEN markers                    the checklist, the prompt, the data (full mode only)

Two modes:
  kit only (--kit-only)  the prompt and the skill's references. This is the mode for the Standard's repository,
                         where the badge page does not live.
  full (the default)     the same, plus the badge page's GEN-marked blocks. It needs badges.html and badges/
                         next to declaration/, as in the badge page's own working folder.

The page's Level sections use the plain wording (`plain_intro` per Level, `plain` per criterion); the prompt and the
skill's references keep the exact wording (`question`, `applies_if`, `help`). Both live in criteria.json.

Usage:  python declaration/build.py [--kit-only]          write the generated files
        python declaration/build.py --check [--kit-only]  exit 1 and name every stale file
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DECL = ROOT / "declaration"
SKILL_REF = ROOT / "skill" / "dps-declaration" / "references"
PAGE = ROOT / "badges.html"
SITE = "https://decisionprovenancestandard.org/"
BADGE_PAGE = SITE + "badges.html"
# Heads the generated Markdown files. The badge page embeds the prompt without it.
MD_HEADER = ("<!-- SPDX-License-Identifier: Apache-2.0 -->\n"
             "<!-- Generated from criteria.json by build.py. Do not edit by hand. -->\n\n")

# The plain-text declaration, one shape per kind. The {where} line is the publication page;
# it is left out when no page was given, so the text never points at a page that does not exist yet.
TEMPLATES = {
    "organization": [
        "Decision Provenance Standard: self-declaration",
        "Organization: {name}",
        "Standard: {standard_label} ({standard_url})",
        "Charters covered: {charters}",
        "Conformance Level claimed: Level {level} ({level_name}), self-declared on {date}",
        "Where this declaration can be read: {where}",
        "Stands behind it: {affirmed_name}, {affirmed_role}",
        "{statement}",
    ],
    "product": [
        "Decision Provenance Standard: self-declaration",
        "Product: {name}",
        "Standard: {standard_label} ({standard_url})",
        "Claim: this product implements the Decision Provenance Standard, self-declared on {date}",
        "Where this declaration can be read: {where}",
        "Stands behind it: {affirmed_name}, {affirmed_role}",
        "{statement}",
    ],
}
WHERE_LINE = "Where this declaration can be read: {where}"
assert all(TEMPLATES[k].count(WHERE_LINE) == 1 for k in TEMPLATES)


def fixed_template(crit, statements, kind):
    """The plain-text shape with the fixed parts filled in: the Standard's label and address, and the statement."""
    std = crit["standard"]
    return [line.replace("{statement}", statements[kind]).replace("{standard_label}", std["label"])
            .replace("{standard_url}", std["url"]) for line in TEMPLATES[kind]]


def load():
    crit_raw = (DECL / "criteria.json").read_bytes()
    schema_raw = (DECL / "dps-declaration.schema.json").read_bytes()
    crit = json.loads(crit_raw)
    schema = json.loads(schema_raw)
    # Each kind has two fixed statements, copied word for word. The first is the one to use; the second is used
    # only when the Standard's Steward is the organization declaring, or made the product.
    allowed = {}
    for branch in schema["allOf"]:
        kind = branch["if"]["properties"]["kind"]["const"]
        st = branch["then"]["properties"]["statement"]
        allowed[kind] = [st["const"]] if "const" in st else list(st["enum"])
    assert set(allowed) == {"organization", "product"}, allowed
    assert len(allowed["organization"]) == 2 and len(allowed["product"]) == 2, allowed
    statements = {k: v[0] for k, v in allowed.items()}
    statements["steward"] = allowed["organization"][1]
    statements["steward_product"] = allowed["product"][1]
    levels = {lv["level"]: lv for lv in crit["levels"]}
    ids = [c["id"] for c in crit["criteria"]]
    assert len(ids) == len(set(ids)), "duplicate criterion id"
    for c in crit["criteria"]:
        assert c["level"] in levels, c["id"]
        assert c["question"].strip() and c["sections"], c["id"]
        assert "help" not in c or c["help"].strip(), c["id"]
        assert c.get("plain", "").strip(), c["id"] + ": the page's plain wording is missing"
    for lv in crit["levels"]:
        assert lv.get("plain_intro", "").strip(), f"Level {lv['level']}: the page's plain intro is missing"
    versions = [crit["standard"]["id"]] + [e["id"] for e in crit["standard"].get("earlier", [])]
    assert schema["properties"]["standard_version"]["enum"] == versions, "schema standard_version must list " + ", ".join(versions)
    assert crit["order"].strip() and crit["rule"].strip()
    assert crit["no_charter"]["text"].strip() and crit["no_charter"]["anchor"].strip()
    return crit_raw, schema_raw, crit, schema, statements, levels


def charter_link(crit):
    """The Standard's own section on Charters, for people who have none yet."""
    return crit["standard"]["url"] + "#" + crit["no_charter"]["anchor"]


def by_level(crit):
    out = {}
    for c in crit["criteria"]:
        out.setdefault(c["level"], []).append(c)
    return out


def signal_text(c):
    sigs = ([c["signal"]] if c.get("signal") else []) + c.get("also_signals", [])
    return ", ".join(sigs) if sigs else "none named in §7"


def build_prompt(crit, statements, levels):
    std = crit["standard"]
    L = []
    L.append(f"You are helping me write a self-declaration under the {std['label']} "
             f"({std['url']}). A self-declaration is our own claim about our own records. "
             "Nobody grades it for us: the Standard's Steward does not validate, grade or audit declarations.")
    L.append("")
    L.append("How to work with me:")
    L.append("1. Ask about one topic per message, and wait for my answer. Facts that belong to the same step go together "
             "in one short message (for example our name and our Charters, or the date, the person and the page at the end). "
             "You may ask for the evidence in the same message (\"If yes, where is that written?\").")
    L.append("2. Never ask again for a fact I have already given, including an \"Applies only if\" condition. Use my earlier answer.")
    L.append("3. Never guess or fill in a fact I have not given you. If I am not sure, record \"not sure\". "
             "\"Not sure\" does not meet the criterion.")
    L.append("4. When I answer yes, note where the evidence lives in a few words: a document, a field, a system, or a document "
             "kept elsewhere with its reference. If I say something is true but cannot say where it is written or recorded, "
             "record \"not sure\" too. The list of fixes then tells us what evidence to record, and where.")
    L.append("5. If I answer only part of a question, name the missing part. If I am sure it is missing "
             "(for example \"we record who and when, but not how\"), record \"not met\". "
             "If I don't know whether it is there, record \"not sure\".")
    L.append("6. When I answer a plain no, do not ask for evidence. Record \"not met\" and move on.")
    L.append("7. If I ask for a particular Level, or say we are certified, do not agree. Say plainly that the Level comes only "
             "from the criteria below, and that this is a self-declaration that no one certifies. Then carry on with the questions.")
    L.append("8. Never describe us or the result as certified, compliant, verified or approved. The word to use is \"self-declared\".")
    L.append("9. Keep questions short and plain. Explain a term only if I ask.")
    L.append("")
    L.append("Step 1. Ask whether this declaration is for an organization (about its own Charters, with a Level) "
             "or for a product (a product that implements the Standard; a product never carries a Level). "
             "For a product, go straight to Step 5.")
    L.append("")
    L.append("Step 2 (organization). In one message, ask for the organization's name and which Charters the declaration "
             "should cover, in our own words.")
    L.append(f"If we have no Charter, or do not know what one is, tell me in these two sentences: \"{crit['no_charter']['text']}\" "
             "In the same message, offer a product declaration instead (Step 5), in case we make a product that implements the Standard, "
             f"and point me to the Standard's section on Charters ({charter_link(crit)}). "
             "Unless I then ask for a product declaration, stop there: no Level, no declaration and no JSON block.")
    L.append("")
    L.append(f"Step 3. For each Charter, go through the criteria below. {crit['order']} "
             "Where a criterion says \"Applies only if\", ask that first, unless I have already answered it; if it is not true "
             "for us, record \"does not apply\" with the reason: it counts as met. "
             "Where it says \"How to judge\", use that to decide.")
    L.append("Before L1-01, unless I have already said, ask in one message: at which levels are this Charter's decisions "
             "made and signed off (its records' altitude)? Ask me to name every level that applies: executive; function leader "
             "(the head of a function or department); team leader; an individual professional deciding about their own work. "
             "In the same message, ask whether we work in an EU or UK country with a works council. Use the answers this way: "
             "any level below executive needs use_case_scope_limit_declaration (L1-01); function leader or below, in a country "
             "with a works council, needs works_council_consultation_record (L1-01); function leader or below also brings in "
             "L2-09. Two things are recommended, not required, and never fail a criterion: where records at function leader "
             "or below describe people, naming the employment counsel of record (a note under L1-01); and, at team leader or "
             "below, a minimum group size for team-level records (a note under L2-09).")
    L.append("Ask L1-01 as one checklist in plain words, as given under it, not as one question per field. "
             "Leave out any \"if\" item that my earlier answers already settle.")
    L.append("")
    for lv in sorted(by_level(crit)):
        meta = levels[lv]
        L.append(f"Level {lv}: {meta['name']} ({meta['section']}). {meta['in_short']}")
        for c in by_level(crit)[lv]:
            L.append(f"- [{c['id']}] {c['question']}")
            if c.get("applies_if"):
                L.append(f"  Applies only if: {c['applies_if']}")
            if c.get("help"):
                L.append(f"  How to judge: {c['help']}")
            if c.get("checklist"):
                L.append("  Ask it as one checklist, in plain words. Does the Charter have: " + "; ".join(c["checklist"]) + "?")
            L.append(f"  Evidence to ask for: {c['evidence_hint']}")
            L.append(f"  (Standard: {', '.join(c['sections'])}; signal: {signal_text(c)})")
        L.append("")
    L.append(f"Step 4. Work out the Level. {crit['rule']} "
             "If a Charter's own text claims a Level (its conformance_level_declared) higher than the Level it reaches, "
             "say so plainly: the evidence does not bear that claim out yet. Then add to the list of fixes: lower the Charter's "
             "own claimed Level to the Level it reaches, or close the gaps between them. "
             "If a Charter reaches no Level, tell me plainly and list what we would need to fix for Level 1. "
             "If no Charter reaches Level 1, give me the evidence table (Step 6a) and the list of fixes, then stop: "
             "there is nothing to declare yet.")
    L.append("")
    L.append("Step 5. Ask for the date of the declaration (YYYY-MM-DD); the name and role of the person at our organization "
             "who stands behind it; and, optionally, the https:// page where it will be published. "
             "For a product, also ask for the product's name.")
    L.append("")
    L.append("Step 6. Give me, in this order:")
    L.append("a) For an organization only, and also when no Level is reached: a short evidence table, one row per criterion "
             "checked (criterion ID; met, not met, not sure or does not apply; the evidence I named and where it lives; "
             "what to fix where it is not met). "
             "Then the gaps at the Level where each Charter stopped, and any Charter left out and why. "
             "A product has no evidence table: skip this for a product.")
    L.append("b) The declaration in plain text, in exactly this form (fill the braces; name each Charter as \"Name (ID)\" "
             "from its own charter_name and charter_id fields if I gave them, otherwise in my words; for several Charters, "
             "separate them with \"; \"; for \"where\", use the page I gave you, and if I gave no page, leave that line out, "
             "so the text never points at a page that does not exist yet):")
    L.append("")
    L.append("For an organization:")
    L += ["    " + line for line in fixed_template(crit, statements, "organization")]
    L.append("")
    L.append("For a product:")
    L += ["    " + line for line in fixed_template(crit, statements, "product")]
    L.append("")
    L.append("   The level names are: " + "; ".join(f"Level {k} = {v['name']}" for k, v in sorted(levels.items())) + ".")
    L.append("c) The same declaration as one JSON block, in a ```json fence, with exactly these fields and no others:")
    org_example = {
        "format": "dps-declaration/v1", "kind": "organization", "name": "<organization name>",
        "declaration_page": "<https:// page, or leave this field out>", "standard_version": crit["standard"]["id"],
        "charters": ["<Charter name (ID)>"], "level": 1, "date": "<YYYY-MM-DD>",
        "statement": statements["organization"],
        "affirmed_by": {"name": "<person's name>", "role": "<their role>"},
    }
    prod_example = {
        "format": "dps-declaration/v1", "kind": "product", "name": "<product name>",
        "declaration_page": "<https:// page, or leave this field out>", "standard_version": crit["standard"]["id"],
        "date": "<YYYY-MM-DD>", "statement": statements["product"],
        "affirmed_by": {"name": "<person's name>", "role": "<their role>"},
    }
    L.append("")
    L.append("For an organization:")
    L += ["    " + ln for ln in json.dumps(org_example, indent=2, ensure_ascii=False).splitlines()]
    L.append("")
    L.append("For a product (never include \"level\" or \"charters\"):")
    L += ["    " + ln for ln in json.dumps(prod_example, indent=2, ensure_ascii=False).splitlines()]
    L.append("")
    L.append("   \"level\" is the number 1, 2 or 3. Copy the statement word for word. Leave \"declaration_page\" out if I gave no page; "
             "if I gave one, it must start with https://.")
    L.append(f"   \"standard_version\" is always \"{crit['standard']['id']}\": declarations are drafted against this version only.")
    L.append("   Only if I tell you that our organization is the Standard's Steward, use this organization statement instead, "
             f"in both the plain text and the JSON block: \"{statements['steward']}\"")
    L.append("   Only if I tell you that the Standard's Steward made the product, use this product statement instead, "
             f"in both the plain text and the JSON block: \"{statements['steward_product']}\"")
    L.append("")
    L.append("Then remind me: this is our own claim, and the person named should read and confirm it before it is published; "
             f"and to get the badge, we paste the JSON block into the badge page: {BADGE_PAGE}. "
             "For an organization only, also remind me that the Standard asks us to keep the declaration "
             "in our own decision register (§7.1).")
    text = "\n".join(L) + "\n"
    assert "</script" not in text.lower()
    return text


def build_criteria_md(crit, levels, statements):
    std = crit["standard"]
    nc = crit["no_charter"]
    L = ["# Conformance Level criteria", "",
         f"Standard: {std['label']} ({std['url']})", "",
         "## How to check", "", crit["order"], "",
         "## The rule", "", crit["rule"], "",
         "## No Charter yet", "",
         "When there is no Charter, or the person does not know what one is, say this in two plain sentences:", "",
         f"> {nc['text']}", "",
         f"Then offer a product declaration instead, in case they make a product that implements the Standard, "
         f"and point them to the Standard's section on Charters ({nc['section']}): {charter_link(crit)}. "
         "No Level and no declaration.", ""]
    for lv in sorted(by_level(crit)):
        meta = levels[lv]
        L += [f"## Level {lv}: {meta['name']} ({meta['section']})", "", meta["in_short"], ""]
        for c in by_level(crit)[lv]:
            L.append(f"- **{c['id']}** {c['question']}")
            if c.get("applies_if"):
                L.append(f"  - Applies only if: {c['applies_if']}")
            if c.get("help"):
                L.append(f"  - How to judge: {c['help']}")
            if c.get("checklist"):
                L.append("  - In plain words, the Charter has: " + "; ".join(c["checklist"]) + ".")
            L.append(f"  - Evidence: {c['evidence_hint']}")
            L.append(f"  - Standard: {', '.join(c['sections'])}. Signal: {signal_text(c)}.")
        L.append("")
    L += ["## The declaration in plain text", "",
          "Fill the braces. Name each Charter as \"Name (ID)\", from its charter_name and charter_id fields; "
          "separate several Charters with \"; \". For {where}, use the publication page; if none was given, "
          "leave that line out, so the text never points at a page that does not exist yet.", ""]
    for kind in ("organization", "product"):
        L += [f"For {'an organization' if kind == 'organization' else 'a product'}:", "", "```text"]
        L += fixed_template(crit, statements, kind)
        L += ["```", ""]
    L.append("Level names: " + "; ".join(f"Level {k} = {v['name']}" for k, v in sorted(levels.items())) + ".")
    L.append("")
    L += [f"Use \"{crit['standard']['id']}\" as standard_version: declarations are drafted against this version only.", ""]
    L += ["Only when the organization declaring is the Standard's Steward, use this statement instead of the organization "
          "statement above, in the plain text and in the JSON (the schema allows both):", "",
          f"> {statements['steward']}", "",
          "Only when the Standard's Steward made the product, use this statement instead of the product statement above, "
          "in the plain text and in the JSON (the schema allows both):", "",
          f"> {statements['steward_product']}", ""]
    return "\n".join(L)


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def build_checklist_html(crit, levels):
    """The page's Level sections. Each opens with the Level's plain intro, then lists what the Level looks at in plain
    words (`plain`), with the criterion ID small at the end. The exact check (question, condition, how to judge) is
    folded under each line, word for word as the prompt and the skill use it."""
    std = crit["standard"]
    out = []
    for lv in sorted(by_level(crit)):
        meta = levels[lv]
        out.append(f'<details class="lvl" data-level="{lv}"><summary>Level {lv}: {esc(meta["name"])} '
                   f'<span class="sec">(<a href="{esc(std["url"])}#{esc(meta["anchor"])}">{esc(meta["section"])}</a>)</span></summary>')
        out.append(f'<p class="intro">{esc(meta["plain_intro"])}</p>')
        out.append('<p class="looks">What it looks at:</p><ul>')
        for c in by_level(crit)[lv]:
            cond = f'<p class="muted">Applies only if: {esc(c["applies_if"])}</p>' if c.get("applies_if") else ""
            judge = f'<p class="muted judge">How to judge: {esc(c["help"])}</p>' if c.get("help") else ""
            out.append(f'<li><span class="plain">{esc(c["plain"])}</span> <span class="cid">{esc(c["id"])}</span>'
                       f'<details class="exact"><summary>Exact check</summary><p>{esc(c["question"])}</p>{cond}{judge}</details></li>')
        out.append("</ul></details>")
    return "\n".join(out)


def build_data_js(crit, schema, statements, levels):
    svgs = {}
    for key, fname in (("1", "dps-self-declared-level-1.svg"), ("2", "dps-self-declared-level-2.svg"),
                       ("3", "dps-self-declared-level-3.svg"), ("product", "dps-implements.svg")):
        svgs[key] = (ROOT / "badges" / fname).read_text(encoding="utf-8").strip()
    data = {
        "site": SITE,
        "badgePage": BADGE_PAGE,
        "standard": {k: v for k, v in crit["standard"].items() if k != "earlier"},
        "standards": {s["id"]: {"label": s["label"], "url": s["url"]}
                      for s in [crit["standard"]] + crit["standard"].get("earlier", [])},
        "levels": {str(k): {"name": v["name"], "section": v["section"], "anchor": v["anchor"]} for k, v in levels.items()},
        "statements": {"organization": statements["organization"], "product": statements["product"]},
        "stewardStatements": {"organization": statements["steward"], "product": statements["steward_product"]},
        "templates": TEMPLATES,
        "whereLine": WHERE_LINE,
        "schema": schema,
        "svg": svgs,
        "badgeFiles": {"1": "dps-self-declared-level-1.svg", "2": "dps-self-declared-level-2.svg",
                       "3": "dps-self-declared-level-3.svg", "product": "dps-implements.svg"},
        "badgeSize": {"level": [220, 40], "product": [250, 40]},
    }
    js = json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")
    return "var DPS = " + js + ";"


def splice(text, start, end, body):
    i = text.index(start) + len(start)
    j = text.index(end, i)
    return text[:i] + body + text[j:]


def outputs(kit_only):
    crit_raw, schema_raw, crit, schema, statements, levels = load()
    prompt = build_prompt(crit, statements, levels)
    out = {
        DECL / "prompt.md": (MD_HEADER + prompt).encode("utf-8"),
        SKILL_REF / "criteria.md": (MD_HEADER + build_criteria_md(crit, levels, statements)).encode("utf-8"),
        SKILL_REF / "criteria.json": crit_raw,
        SKILL_REF / "dps-declaration.schema.json": schema_raw,
    }
    if not kit_only:
        page = PAGE.read_text(encoding="utf-8")
        page = splice(page, "<!--GEN:checklist-->", "<!--/GEN:checklist-->", "\n" + build_checklist_html(crit, levels) + "\n")
        page = splice(page, '<script type="text/plain" id="dps-prompt">', "</script>", prompt)
        page = splice(page, "/*GEN:data*/", "/*/GEN:data*/", "\n" + build_data_js(crit, schema, statements, levels) + "\n")
        out[PAGE] = page.encode("utf-8")
    return out


def main(argv):
    unknown = [a for a in argv if a not in ("--check", "--kit-only")]
    if unknown:
        print("Unknown option:", *unknown, "\nUsage: build.py [--check] [--kit-only]")
        return 2
    check, kit_only = "--check" in argv, "--kit-only" in argv
    if not kit_only and not PAGE.exists():
        print(f"The badge page ({PAGE.name}) is not next to this kit, so the full mode cannot run here. "
              "Use --kit-only to build or check the prompt and the skill's references only.")
        return 2
    stale = []
    for path, content in outputs(kit_only).items():
        current = path.read_bytes() if path.exists() else None
        if current != content:
            stale.append(path)
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
    rel = [str(p.relative_to(ROOT)) for p in stale]
    if check:
        if stale:
            print("STALE (run: python " + pathlib.Path(sys.argv[0]).as_posix() + (" --kit-only" if kit_only else "") + "):",
                  *rel, sep="\n  ")
            return 1
        print("OK: every generated file matches its sources" + (" (kit only)." if kit_only else "."))
        return 0
    print("Wrote:", *(rel or ["nothing (already current)"]), sep="\n  ")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
