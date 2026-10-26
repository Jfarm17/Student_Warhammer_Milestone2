"""BSData XML -> one plain-text doc per chapter datasheet + corpus/manifest.jsonl.  Run: python parse_bsdata.py"""
import json
import xml.etree.ElementTree as ET
from pathlib import Path

RAW = Path("Data/raw/bsdata")
OUT = Path("corpus/datasheets")
CHAPTERS = {"Black Templars": "Imperium - Black Templars.cat",
            "Dark Angels": "Imperium - Dark Angels.cat",
            "Deathwatch": "Imperium - Deathwatch.cat"}
PER_CHAPTER = 10
LICENSE = "BSData community data (github.com/BSData/wh40k-10e); rules text (c) Games Workshop. Not redistributed."


def unique(items):
    return list(dict.fromkeys(items))


def datasheet_text(chapter, e, B):
    stats, abilities = [], []
    for p in e.iter(B + "profile"):
        chars = {c.get("name"): (c.text or "").strip() for c in p.iter(B + "characteristic")}
        if p.get("typeName") == "Unit":
            stats.append(f"{p.get('name')}: " + ", ".join(f"{k} {v}" for k, v in chars.items()))
        elif p.get("typeName") == "Abilities":
            abilities.append(f"- {p.get('name')}: {chars.get('Description', '')}")
    keywords = unique(c.get("name") for c in e.iter(B + "categoryLink"))
    rules = unique(l.get("name") for l in e.iter(B + "infoLink"))
    pts = next((c.get("value") for c in e.iter(B + "cost") if c.get("name") == "pts"), "?")
    lines = [f"{chapter} datasheet: {e.get('name')}", f"Points: {pts}", "Stats:", *unique(stats),
             "Abilities:", *unique(abilities), "Keywords: " + ", ".join(keywords)]
    if rules:
        lines.append("Core rules referenced: " + ", ".join(rules))
    return "\n".join(lines)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for chapter, fname in CHAPTERS.items():
        root = ET.parse(RAW / fname).getroot()
        B = root.tag.split("}")[0] + "}"
        entries = [e for e in root.find(B + "sharedSelectionEntries")
                   if e.get("type") in ("unit", "model") and e.get("hidden") != "true"
                   and "[Legends]" not in e.get("name")
                   and any(c.get("name") == f"Faction: {chapter}" for c in e.iter(B + "categoryLink"))]
        # ponytail: first N in file order, not random; say so in the report
        for e in entries[:PER_CHAPTER]:
            doc_id = f"{chapter.lower().replace(' ', '-')}--{e.get('name').lower().replace(' ', '-')}"
            path = OUT / f"{doc_id}.txt"
            path.write_text(datasheet_text(chapter, e, B), encoding="utf-8")
            manifest.append({"id": doc_id, "path": path.as_posix(), "source": "BSData wh40k-10e",
                             "format": "xml", "chapter": chapter, "license": LICENSE})
        print(f"{chapter}: {len(entries)} chapter datasheets found, kept {min(len(entries), PER_CHAPTER)}")
    with open("corpus/manifest.jsonl", "w", encoding="utf-8") as f:
        f.writelines(json.dumps(m) + "\n" for m in manifest)
    print(f"{len(manifest)} docs -> corpus/manifest.jsonl")


if __name__ == "__main__":
    main()
