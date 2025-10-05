#!/usr/bin/env python3
"""
sources_cli.py — CLI for Source/Quote library (no SourceCollection dependency)

Examples:

  # Add a source from flags
  python sources_cli.py --db sources.db add-source \
      --entry-type article --citation-key Malcolm1964Education \
      --author "Malcolm X" --title "Speech on Education" --year 1964 \
      --publisher "Nation of Islam" \
      --reason "Core perspective on empowerment through learning."

  # Add a quote
  python sources_cli.py --db sources.db add-quote \
      --citation-key Malcolm1964Education \
      --direct "Education is the passport to the future." \
      --paraphrase "Learning opens doors to tomorrow." \
      --tags education,empowerment --topic "Social mobility"

  # SEARCH DOES NOT WORK

  # Search sources
  python sources_cli.py --db sources.db search-sources --q 'author:"Malcolm X" year:1950..1970'

  # Search quotes
  python sources_cli.py --db sources.db search-quotes --q 'tag:education "passport to the future"'

  # Get one
  python sources_cli.py --db sources.db get-source --citation-key Malcolm1964Education
  python sources_cli.py --db sources.db get-quote --id 1

  # List, export
  python sources_cli.py --db sources.db list-sources
  python sources_cli.py --db sources.db export-bibtex --out my_library.bib

  # Bulk import/export JSON (single or list of sources)
  python sources_cli.py --db sources.db import-json --file sources.json
  python sources_cli.py --db sources.db export-json --out dump.json

  # Maintenance
  python sources_cli.py --db sources.db rebuild-fts
"""

import argparse
import json
import sys
from datetime import datetime
from typing import List, Optional

from sourcesys import SourceDatabase, QueryEngine, SourceCard, QuoteCard  # adjust as needed


# -----------------------------
# Helpers
# -----------------------------

def _csv_to_list(s: Optional[str]) -> Optional[List[str]]:
    if s is None or s == "":
        return None
    return [x.strip() for x in s.split(",") if x.strip()]

def _print_json(obj) -> None:
    if hasattr(obj, "model_dump_json"):
        print(obj.model_dump_json(indent=2, ensure_ascii=False))
    else:
        print(json.dumps(obj, indent=2, ensure_ascii=False))

def _load_sources_from_json(path: str) -> List[SourceCard]:
    """Load a JSON file that is either a single SourceCard object or a list of SourceCards."""
    data = json.load(sys.stdin) if path == "-" else json.load(open(path, "r", encoding="utf-8"))
    if isinstance(data, list):
        return [SourceCard(**item) for item in data]
    elif isinstance(data, dict):
        return [SourceCard(**data)]
    else:
        raise ValueError("JSON must be an object (single SourceCard) or an array (list of SourceCard objects).")


# -----------------------------
# Commands
# -----------------------------

def cmd_add_source(args):
    db = SourceDatabase(args.db)

    if args.file:
        sources = _load_sources_from_json(args.file)
        for src in sources:
            db.upsert_source(src)
        print(f"Upserted {len(sources)} source(s) from JSON.")
        return

    # Validate required flags when not using --file
    if not args.entry_type or not args.citation_key:
        raise SystemExit("--entry-type and --citation-key are required when not using --file")

    src = SourceCard(
        entry_type=args.entry_type,
        citation_key=args.citation_key,
        author=args.author,
        editor=args.editor,
        title=args.title,
        year=args.year,
        month=args.month,
        journal=args.journal,
        booktitle=args.booktitle,
        volume=args.volume,
        number=args.number,
        pages=args.pages,
        publisher=args.publisher,
        address=args.address,
        organization=args.organization,
        school=args.school,
        institution=args.institution,
        howpublished=args.howpublished,
        series=args.series,
        edition=args.edition,
        note=args.note,
        doi=args.doi,
        url=args.url,
        isbn=args.isbn,
        issn=args.issn,
        abstract=args.abstract,
        reason_for_interest=args.reason,
        quote_cards=[],  # add quotes separately or via import-json
    )
    db.upsert_source(src)
    print(f"Upserted source: {args.citation_key}")

def cmd_add_quote(args):
    db = SourceDatabase(args.db)
    quote = QuoteCard(
        direct_quote=args.direct,
        paraphrase=args.paraphrase,
        page=args.page,
        chapter=args.chapter,
        timestamp=args.timestamp,
        context_excerpt=args.context,
        tags=_csv_to_list(args.tags),
        topic=args.topic,
        category=args.category,
        sentiment=args.sentiment,
        commentary=args.commentary,
        relevance=args.relevance,
        related_concepts=_csv_to_list(args.related),
        date_added=datetime.now(),
    )
    qid = db.add_quote(args.citation_key, quote)
    print(f"Added quote id={qid} to {args.citation_key}")

def cmd_get_source(args):
    db = SourceDatabase(args.db)
    src = db.get_source(args.citation_key)
    if src is None:
        print(f"No source found for citation_key={args.citation_key}")
        return
    _print_json(src)

def cmd_get_quote(args):
    db = SourceDatabase(args.db)
    q = db.get_quote(args.id)
    if q is None:
        print(f"No quote found for id={args.id}")
        return
    _print_json(q)

def cmd_list_sources(args):
    db = SourceDatabase(args.db)
    items = db.list_sources()
    if args.json:
        rows = [{"citation_key": ck, "title": title, "year": year} for (ck, title, year) in items]
        _print_json(rows)
        return
    for ck, title, year in items:
        y = year if year is not None else "-"
        print(f"{ck:30}  {y:6}  {title or ''}")

def cmd_search_sources(args):
    db = SourceDatabase(args.db)
    qe = QueryEngine(db)
    hits = qe.search_sources(args.q, limit=args.limit)
    out = []
    for sc, rank in hits:
        out.append({
            "rank": rank,
            "citation_key": sc.citation_key,
            "title": sc.title,
            "author": sc.author,
            "year": sc.year,
            "journal": sc.journal,
            "publisher": sc.publisher,
        })
    _print_json(out)

def cmd_search_quotes(args):
    db = SourceDatabase(args.db)
    qe = QueryEngine(db)
    hits = qe.search_quotes(args.q, limit=args.limit)
    out = []
    for q, rank, cite in hits:
        out.append({
            "rank": rank,
            "citation_key": cite,
            "quote_id": q.quote_id,
            "direct_quote": q.direct_quote,
            "paraphrase": q.paraphrase,
            "tags": q.tags,
            "topic": q.topic,
            "page": q.page,
            "date_added": q.date_added.isoformat() if q.date_added else None,
        })
    _print_json(out)

def cmd_export_bibtex(args):
    db = SourceDatabase(args.db)
    content = db.export_all_bibtex(args.out)
    print(content)

def cmd_rebuild_fts(args):
    db = SourceDatabase(args.db)
    db.rebuild_fts()
    print("FTS rebuilt.")

def cmd_update_quote(args):
    db = SourceDatabase(args.db)
    updates = {}
    if args.direct is not None: updates["direct_quote"] = args.direct
    if args.paraphrase is not None: updates["paraphrase"] = args.paraphrase
    if args.page is not None: updates["page"] = args.page
    if args.chapter is not None: updates["chapter"] = args.chapter
    if args.timestamp is not None: updates["timestamp"] = args.timestamp
    if args.context is not None: updates["context_excerpt"] = args.context
    if args.tags is not None: updates["tags"] = ", ".join(_csv_to_list(args.tags) or [])
    if args.topic is not None: updates["topic"] = args.topic
    if args.category is not None: updates["category"] = args.category
    if args.sentiment is not None: updates["sentiment"] = args.sentiment
    if args.commentary is not None: updates["commentary"] = args.commentary
    if args.relevance is not None: updates["relevance"] = args.relevance
    if args.related is not None: updates["related_concepts"] = ", ".join(_csv_to_list(args.related) or [])
    if args.touch_date:
        updates["date_added"] = datetime.now().isoformat()

    if not updates:
        print("No fields to update; provide at least one flag to change.")
        return

    # Execute update directly (no dependency on db.update_quote)
    fields = ", ".join([f"{k} = :{k}" for k in updates.keys()])
    updates["id"] = args.id
    cur = db.conn.cursor()
    cur.execute(f"UPDATE quote_cards SET {fields} WHERE id = :id", updates)
    db.conn.commit()
    print(f"Updated quote id={args.id}")

def cmd_delete_quote(args):
    db = SourceDatabase(args.db)
    cur = db.conn.cursor()
    cur.execute("DELETE FROM quote_cards WHERE id = ?", (args.id,))
    db.conn.commit()
    print(f"Deleted quote id={args.id}")

def cmd_import_json(args):
    db = SourceDatabase(args.db)
    sources = _load_sources_from_json(args.file)
    count = 0
    for src in sources:
        db.upsert_source(src)
        count += 1
    print(f"Imported {count} source(s).")

def cmd_export_json(args):
    db = SourceDatabase(args.db)
    items = db.list_sources()
    sources = []
    for ck, _, _ in items:
        sc = db.get_source(ck)
        if sc:
            sources.append(sc.model_dump())
    out_str = json.dumps(sources, indent=2, ensure_ascii=False)
    if args.out == "-":
        print(out_str)
    else:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out_str)
        print(f"Wrote {len(sources)} sources to {args.out}")


# -----------------------------
# Argparse
# -----------------------------

def build_parser():
    p = argparse.ArgumentParser(description="Source/Quote library CLI (no SourceCollection)")
    p.add_argument("--db", default="sources.db", help="SQLite database path (default: sources.db)")
    sub = p.add_subparsers(dest="cmd", required=True)

    # add-source
    sp = sub.add_parser("add-source", help="Add or update a source (flags or --file JSON)")
    sp.add_argument("--file", help="JSON file (use '-' for stdin)")
    sp.add_argument("--entry-type")
    sp.add_argument("--citation-key")
    sp.add_argument("--author")
    sp.add_argument("--editor")
    sp.add_argument("--title")
    sp.add_argument("--year", type=int)
    sp.add_argument("--month")
    sp.add_argument("--journal")
    sp.add_argument("--booktitle")
    sp.add_argument("--volume")
    sp.add_argument("--number")
    sp.add_argument("--pages")
    sp.add_argument("--publisher")
    sp.add_argument("--address")
    sp.add_argument("--organization")
    sp.add_argument("--school")
    sp.add_argument("--institution")
    sp.add_argument("--howpublished")
    sp.add_argument("--series")
    sp.add_argument("--edition")
    sp.add_argument("--note")
    sp.add_argument("--doi")
    sp.add_argument("--url")
    sp.add_argument("--isbn")
    sp.add_argument("--issn")
    sp.add_argument("--abstract")
    sp.add_argument("--reason", help="Reason for interest")
    sp.set_defaults(func=cmd_add_source)

    # add-quote
    sp = sub.add_parser("add-quote", help="Add a quote to a source")
    sp.add_argument("--citation-key", required=True)
    sp.add_argument("--direct", required=True, help="Direct quote")
    sp.add_argument("--paraphrase", required=True)
    sp.add_argument("--page", type=int)
    sp.add_argument("--chapter")
    sp.add_argument("--timestamp")
    sp.add_argument("--context")
    sp.add_argument("--tags", help="Comma-separated")
    sp.add_argument("--topic")
    sp.add_argument("--category")
    sp.add_argument("--sentiment")
    sp.add_argument("--commentary")
    sp.add_argument("--relevance")
    sp.add_argument("--related", help="Comma-separated")
    sp.set_defaults(func=cmd_add_quote)

    # get-source
    sp = sub.add_parser("get-source", help="Get one source as JSON")
    sp.add_argument("--citation-key", required=True)
    sp.set_defaults(func=cmd_get_source)

    # get-quote
    sp = sub.add_parser("get-quote", help="Get one quote as JSON")
    sp.add_argument("--id", type=int, required=True)
    sp.set_defaults(func=cmd_get_quote)

    # list-sources
    sp = sub.add_parser("list-sources", help="List sources")
    sp.add_argument("--json", action="store_true", help="Output JSON instead of text table")
    sp.set_defaults(func=cmd_list_sources)

    # search-sources
    sp = sub.add_parser("search-sources", help="Search sources with the mini query language")
    sp.add_argument("--q", required=True, help="Query string")
    sp.add_argument("--limit", type=int, default=25)
    sp.set_defaults(func=cmd_search_sources)

    # search-quotes
    sp = sub.add_parser("search-quotes", help="Search quotes with the mini query language")
    sp.add_argument("--q", required=True, help="Query string")
    sp.add_argument("--limit", type=int, default=50)
    sp.set_defaults(func=cmd_search_quotes)

    # update-quote
    sp = sub.add_parser("update-quote", help="Update fields on a quote")
    sp.add_argument("--id", type=int, required=True)
    sp.add_argument("--direct")
    sp.add_argument("--paraphrase")
    sp.add_argument("--page", type=int)
    sp.add_argument("--chapter")
    sp.add_argument("--timestamp")
    sp.add_argument("--context")
    sp.add_argument("--tags", help="Comma-separated")
    sp.add_argument("--topic")
    sp.add_argument("--category")
    sp.add_argument("--sentiment")
    sp.add_argument("--commentary")
    sp.add_argument("--relevance")
    sp.add_argument("--related", help="Comma-separated")
    sp.add_argument("--touch-date", action="store_true", help="Set date_added to now")
    sp.set_defaults(func=cmd_update_quote)

    # delete-quote
    sp = sub.add_parser("delete-quote", help="Delete a quote by ID")
    sp.add_argument("--id", type=int, required=True)
    sp.set_defaults(func=cmd_delete_quote)

    # export-bibtex
    sp = sub.add_parser("export-bibtex", help="Export all sources as BibTeX")
    sp.add_argument("--out", default="library_export.bib")
    sp.set_defaults(func=cmd_export_bibtex)

    # rebuild-fts
    sp = sub.add_parser("rebuild-fts", help="Rebuild FTS indexes")
    sp.set_defaults(func=cmd_rebuild_fts)

    # import-json
    sp = sub.add_parser("import-json", help="Import SourceCard JSON (- for stdin) [single object OR list]")
    sp.add_argument("--file", required=True, help="Path or '-' for stdin")
    sp.set_defaults(func=cmd_import_json)

    # export-json
    sp = sub.add_parser("export-json", help="Export entire DB as JSON (list of SourceCard)")
    sp.add_argument("--out", required=True, help="Path or '-' for stdout")
    sp.set_defaults(func=cmd_export_json)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
