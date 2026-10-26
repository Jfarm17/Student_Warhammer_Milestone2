# Milestone 2: Security-Hardened Warhammer 40K RAG Assistant

DATA 790 · Joshua Farmer

A RAG assistant that answers Warhammer 40,000 10th edition rules, datasheet and lore questions from the official
Core Rules, 30 BSData chapter datasheets (Black Templars, Dark Angels, Deathwatch) and section-capped Fandom wiki lore,
hardened against prompt injection, poisoned documents, prompt leakage and PII exposure. Milestone 1 is tagged `milestone-1`.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env        #Add API Keys for Pinecone and OpenAI
```

The source texts are not in this repo (Games Workshop content is copyrighted). Download them into `Data/`:

- `Data/Warhammer40k10EDCoreRules.pdf` -- free Core Rules PDF from warhammer-community.com
- `Data/raw/bsdata/` -- from github.com/BSData/wh40k-10e: `Imperium - Black Templars.cat`,
  `Imperium - Dark Angels.cat`, `Imperium - Deathwatch.cat`
- `Data/` -- the Fandom wiki pages (warhammer40k.fandom.com) for Space Marines, Black Templars, Dark Angels and
  Deathwatch, saved from the browser as PDF, named `<Page> _ Warhammer 40k Wiki _ Fandom.pdf`

Then build the datasheet text files (once):

```bash
python parse_bsdata.py
```

## Run

Open `Milestone_2_Farmer_Joshua.ipynb` and run it top to bottom. It loads the corpus, ingests it into
Pinecone (index `rag-benchmark`, namespace `m2-c500`), and builds both pipelines (Demo-RAG and Self-RAG).

- **Gold-set eval:** run the *Gold Question Evaluation Set*, *Eval* and *Part 2 Retrieve and Score* cells.
- **Attack suite:** run the *Attack Suite*, plant/unplant and *Run + Score* cells.

Run each twice: with `defenses_on = False` in the Security Cell (undefended baseline), then `True` (defended).
Rerun the Security Cell after changing it. Results are written to `result/`.

## Files

| Path | What it is |
|---|---|
| `Milestone_2_Farmer_Joshua.ipynb` | the system, evaluation and attack suite |
| `parse_bsdata.py` | converts BSData XML datasheets to plain text + manifest entries |
| `manifest.jsonl` | every document: id, source, format, page, chapter, license |
| `Data/GoldenSet_Questions.csv` | 40-question gold set with labelled documents |
| `result/gold_*.csv`, `result/attacks_*.csv` | the numbers quoted in the audit report |
| `gold_set_support.ipynb` | lookup helpers used to label the gold set |

Keys live only in `.env`, which is git-ignored. Attacks target only this system and its own Pinecone index.
