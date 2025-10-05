# Source System — Reference & Quote Management

A simple, extensible Python-based system for managing **sources** (articles, books, etc.) and **quotes** (direct and paraphrased) with structured metadata.

This project uses:
- **SQLite3** for local persistence  
- **Pydantic** for schema validation  
- **FTS5 (Full-Text Search)** for planned text search support  
- **A CLI tool** (`sources_cli.py`) for easy command-line use  

---

## 🧩 Features

### ✅ Core
- Store bibliographic data for each **SourceCard**
- Attach multiple **QuoteCards** per source
- Support for BibTeX export (`.bib` file)
- Indexes for fast retrieval
- Full-text search schema in place (FTS5)

### ⚠️ Note on Search
Full-text search is **under development**.  
The database includes FTS5 tables and a mini query parser, but searching currently **does not return results reliably**.  
You can still use the CLI to add, list, export, and manage data normally.

---

## 🧱 Data Model

### `SourceCard`
Represents a bibliographic source, including all fields necessary to reconstruct a BibTeX entry.

Key fields:
- `entry_type`, `citation_key`
- `author`, `editor`, `title`, `year`, `journal`, etc.
- `abstract`, `reason_for_interest`
- Associated `quote_cards` (list of `QuoteCard`)

### `QuoteCard`
Represents an individual quotation or paraphrase linked to a source.

Key fields:
- `direct_quote`, `paraphrase`
- `page`, `chapter`, `tags`, `topic`
- `commentary`, `relevance`
- `date_added`, `sentiment`, `related_concepts`

---

## 🗄️ Database

All data is stored in an SQLite database (`sources.db` by default).  
The system automatically creates necessary tables and indexes.

**Tables:**
- `source_cards`
- `quote_cards`
- `sources_fts` *(for upcoming full-text search)*
- `quotes_fts` *(for upcoming full-text search)*

---

## 🔧 CLI Usage

Run with:
```bash
python sources_cli.py [command] [options]
````

### Example Commands

#### Add a Source

```bash
python sources_cli.py add-source \
  --entry-type article \
  --citation-key Malcolm1964Education \
  --author "Malcolm X" \
  --title "Speech on Education" \
  --year 1964 \
  --publisher "Nation of Islam" \
  --reason "Core reference for educational philosophy."
```

#### Add a Quote

```bash
python sources_cli.py add-quote \
  --citation-key Malcolm1964Education \
  --direct "Education is the passport to the future." \
  --paraphrase "Learning opens doors to opportunity." \
  --tags education,empowerment
```

#### Export to BibTeX

```bash
python sources_cli.py export-bibtex --out my_library.bib
```

#### List All Sources

```bash
python sources_cli.py list-sources
```

#### Search (⚠️ Not Yet Functional)

```bash
python sources_cli.py search-sources --q 'author:"Malcolm X"'
```

---

## 📦 Import / Export

#### Import from JSON

```bash
python sources_cli.py import-json --file sources.json
```

Accepts either a single `SourceCard` object or a list of sources.

#### Export to JSON

```bash
python sources_cli.py export-json --out dump.json
```

Outputs all data as a JSON list of `SourceCard` entries.

---

## 📚 Example JSON Structure

```json
[
  {
    "entry_type": "article",
    "citation_key": "Malcolm1964Education",
    "author": "Malcolm X",
    "title": "Speech on Education",
    "year": 1964,
    "publisher": "Nation of Islam",
    "abstract": "A speech on education and empowerment.",
    "reason_for_interest": "Core reference for educational philosophy.",
    "quote_cards": [
      {
        "direct_quote": "Education is the passport to the future.",
        "paraphrase": "Learning opens doors to opportunity.",
        "tags": ["education", "empowerment"]
      }
    ]
  }
]
```

---

## 🧠 Planned Enhancements

* [ ] Fix and verify full-text search with FTS5
* [ ] Add result ranking (bm25) and highlighting
* [ ] Add web-based or TUI interface
* [ ] Optional cloud sync or JSON import/export utilities

---

## 🪶 License

MIT License — feel free to fork, modify, and contribute.

---

**Status:** Early prototype.
Most database and export operations are stable, but **search features are not yet working**.
