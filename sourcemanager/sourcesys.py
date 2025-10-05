import sqlite3
from datetime import datetime
from typing import List, Optional, Tuple
from pydantic import BaseModel

import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

# -----------------------------
# Pydantic models
# -----------------------------

class QuoteCard(BaseModel):
    quote_id: Optional[int] = None
    direct_quote: str
    paraphrase: str
    page: Optional[int] = None
    chapter: Optional[str] = None
    timestamp: Optional[str] = None
    context_excerpt: Optional[str] = None
    tags: Optional[List[str]] = None
    topic: Optional[str] = None
    category: Optional[str] = None
    sentiment: Optional[str] = None
    commentary: Optional[str] = None
    relevance: Optional[str] = None
    related_concepts: Optional[List[str]] = None
    date_added: Optional[datetime] = None


class SourceCard(BaseModel):
    entry_type: str
    citation_key: str
    author: Optional[str] = None
    editor: Optional[str] = None
    title: Optional[str] = None
    year: Optional[int] = None
    month: Optional[str] = None
    journal: Optional[str] = None
    booktitle: Optional[str] = None
    volume: Optional[str] = None
    number: Optional[str] = None
    pages: Optional[str] = None
    publisher: Optional[str] = None
    address: Optional[str] = None
    organization: Optional[str] = None
    school: Optional[str] = None
    institution: Optional[str] = None
    howpublished: Optional[str] = None
    series: Optional[str] = None
    edition: Optional[str] = None
    note: Optional[str] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    isbn: Optional[str] = None
    issn: Optional[str] = None
    abstract: Optional[str] = None
    reason_for_interest: Optional[str] = None
    quote_cards: List[QuoteCard] = []

    def to_bibtex(self) -> str:
        field_map = {
            "author": self.author,
            "editor": self.editor,
            "title": self.title,
            "year": self.year,
            "month": self.month,
            "journal": self.journal,
            "booktitle": self.booktitle,
            "volume": self.volume,
            "number": self.number,
            "pages": self.pages,
            "publisher": self.publisher,
            "address": self.address,
            "organization": self.organization,
            "school": self.school,
            "institution": self.institution,
            "howpublished": self.howpublished,
            "series": self.series,
            "edition": self.edition,
            "note": self.note,
            "doi": self.doi,
            "url": self.url,
            "isbn": self.isbn,
            "issn": self.issn,
        }
        fields = [f"  {k} = {{{v}}}" for k, v in field_map.items() if v not in (None, "")]
        return f"@{self.entry_type}{{{self.citation_key},\n" + ",\n".join(fields) + "\n}"

# -----------------------------
# SourceCollection model
# -----------------------------

class SourceCollection(BaseModel):
    collection_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    source_keys: Optional[List[str]] = None  # citation_keys of sources

# -----------------------------
# SQLite DB with indexing + search
# -----------------------------

class SourceDatabase:
    def __init__(self, db_path: str = "sources.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.fts_enabled = False
        self.create_tables()
        self.create_indexes()
        self.enable_fts()

    # Schema
    def create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS source_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_type TEXT,
            citation_key TEXT UNIQUE,
            author TEXT,
            editor TEXT,
            title TEXT,
            year INTEGER,
            month TEXT,
            journal TEXT,
            booktitle TEXT,
            volume TEXT,
            number TEXT,
            pages TEXT,
            publisher TEXT,
            address TEXT,
            organization TEXT,
            school TEXT,
            institution TEXT,
            howpublished TEXT,
            series TEXT,
            edition TEXT,
            note TEXT,
            doi TEXT,
            url TEXT,
            isbn TEXT,
            issn TEXT,
            abstract TEXT,
            reason_for_interest TEXT
        )""")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS quote_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            citation_key TEXT,
            direct_quote TEXT,
            paraphrase TEXT,
            page INTEGER,
            chapter TEXT,
            timestamp TEXT,
            context_excerpt TEXT,
            tags TEXT,
            topic TEXT,
            category TEXT,
            sentiment TEXT,
            commentary TEXT,
            relevance TEXT,
            related_concepts TEXT,
            date_added TEXT,
            FOREIGN KEY (citation_key) REFERENCES source_cards (citation_key)
        )""")
        self.conn.commit()

    # Indexes
    def create_indexes(self):
        cur = self.conn.cursor()
        cur.execute("CREATE INDEX IF NOT EXISTS idx_sources_cite ON source_cards(citation_key)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_sources_author ON source_cards(author)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_sources_title ON source_cards(title)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_sources_year ON source_cards(year)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_quotes_cite ON quote_cards(citation_key)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_quotes_date ON quote_cards(date_added)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_quotes_topic ON quote_cards(topic)")
        self.conn.commit()

    # Optional FTS5 (auto-fallback to LIKE)
    def enable_fts(self):
        try:
            cur = self.conn.cursor()
            # FTS for sources
            cur.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS sources_fts USING fts5(
                title, author, abstract, reason_for_interest, journal, publisher, booktitle, doi, url,
                content='', tokenize='unicode61'
            )""")
            # FTS for quotes
            cur.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS quotes_fts USING fts5(
                direct_quote, paraphrase, context_excerpt, tags, topic, category, commentary, relevance,
                content='', tokenize='unicode61'
            )""")
            self.fts_enabled = True
            self.conn.commit()
        except sqlite3.OperationalError:
            self.fts_enabled = False  # falls back to LIKE searches

    # ------------- Helpers: row->model -------------
    @staticmethod
    def _row_to_quote(row: sqlite3.Row) -> QuoteCard:
        return QuoteCard(
            quote_id=row["id"],
            direct_quote=row["direct_quote"],
            paraphrase=row["paraphrase"],
            page=row["page"],
            chapter=row["chapter"],
            timestamp=row["timestamp"],
            context_excerpt=row["context_excerpt"],
            tags=row["tags"].split(", ") if row["tags"] else [],
            topic=row["topic"],
            category=row["category"],
            sentiment=row["sentiment"],
            commentary=row["commentary"],
            relevance=row["relevance"],
            related_concepts=row["related_concepts"].split(", ") if row["related_concepts"] else [],
            date_added=datetime.fromisoformat(row["date_added"]) if row["date_added"] else None,
        )

    def _row_to_source(self, row: sqlite3.Row) -> SourceCard:
        quotes = self.get_quotes_for_source(row["citation_key"])
        base = dict(row)
        base.pop("id", None)
        return SourceCard(**base, quote_cards=quotes)

    # ------------- Upserts -------------
    def upsert_source(self, source: SourceCard):
        """Insert/update a source; keeps FTS in sync when enabled."""
        cur = self.conn.cursor()
        cur.execute("""
        INSERT INTO source_cards (
            entry_type, citation_key, author, editor, title, year, month, journal, booktitle,
            volume, number, pages, publisher, address, organization, school, institution,
            howpublished, series, edition, note, doi, url, isbn, issn, abstract, reason_for_interest
        ) VALUES (
            :entry_type, :citation_key, :author, :editor, :title, :year, :month, :journal, :booktitle,
            :volume, :number, :pages, :publisher, :address, :organization, :school, :institution,
            :howpublished, :series, :edition, :note, :doi, :url, :isbn, :issn, :abstract, :reason_for_interest
        )
        ON CONFLICT(citation_key) DO UPDATE SET
            entry_type=excluded.entry_type,
            author=excluded.author, editor=excluded.editor, title=excluded.title, year=excluded.year,
            month=excluded.month, journal=excluded.journal, booktitle=excluded.booktitle, volume=excluded.volume,
            number=excluded.number, pages=excluded.pages, publisher=excluded.publisher, address=excluded.address,
            organization=excluded.organization, school=excluded.school, institution=excluded.institution,
            howpublished=excluded.howpublished, series=excluded.series, edition=excluded.edition,
            note=excluded.note, doi=excluded.doi, url=excluded.url, isbn=excluded.isbn, issn=excluded.issn,
            abstract=excluded.abstract, reason_for_interest=excluded.reason_for_interest
        """, source.model_dump(exclude={"quote_cards"}))
        self.conn.commit()

        # Ensure quotes exist/are synced
        for q in source.quote_cards:
            self.add_quote(source.citation_key, q)

        # FTS sync
        if self.fts_enabled:
            self._upsert_sources_fts(source.citation_key)

    def add_quote(self, citation_key: str, quote: QuoteCard) -> int:
        """Add a new quote and return its row id."""
        cur = self.conn.cursor()
        cur.execute("""
        INSERT INTO quote_cards (
            citation_key, direct_quote, paraphrase, page, chapter, timestamp, context_excerpt,
            tags, topic, category, sentiment, commentary, relevance, related_concepts, date_added
        ) VALUES (
            :citation_key, :direct_quote, :paraphrase, :page, :chapter, :timestamp, :context_excerpt,
            :tags, :topic, :category, :sentiment, :commentary, :relevance, :related_concepts, :date_added
        )""", {
            "citation_key": citation_key,
            "direct_quote": quote.direct_quote,
            "paraphrase": quote.paraphrase,
            "page": quote.page,
            "chapter": quote.chapter,
            "timestamp": quote.timestamp,
            "context_excerpt": quote.context_excerpt,
            "tags": ", ".join(quote.tags or []),
            "topic": quote.topic,
            "category": quote.category,
            "sentiment": quote.sentiment,
            "commentary": quote.commentary,
            "relevance": quote.relevance,
            "related_concepts": ", ".join(quote.related_concepts or []),
            "date_added": quote.date_added.isoformat() if quote.date_added else datetime.now().isoformat(),
        })
        self.conn.commit()
        new_id = cur.lastrowid

        if self.fts_enabled:
            self._upsert_quotes_fts(new_id)

        return new_id

    # ------------- Getters -------------
    def get_source(self, citation_key: str) -> Optional[SourceCard]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM source_cards WHERE citation_key=?", (citation_key,))
        row = cur.fetchone()
        return self._row_to_source(row) if row else None

    def get_quote(self, quote_id: int) -> Optional[QuoteCard]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM quote_cards WHERE id=?", (quote_id,))
        row = cur.fetchone()
        return self._row_to_quote(row) if row else None

    def get_quotes_for_source(self, citation_key: str) -> List[QuoteCard]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM quote_cards WHERE citation_key=? ORDER BY date_added DESC, id DESC", (citation_key,))
        return [self._row_to_quote(r) for r in cur.fetchall()]

    # ------------- Search (FTS → LIKE fallback) -------------
    def search_sources(self, query: str, limit: int = 25) -> List[Tuple[SourceCard, float]]:
        """Search across title/author/abstract/reason fields."""
        cur = self.conn.cursor()
        results: List[Tuple[SourceCard, float]] = []

        if self.fts_enabled:
            cur.execute("""
                SELECT s.*, bm25(sources_fts) AS rank
                FROM sources_fts
                JOIN source_cards s ON s.rowid = sources_fts.rowid
                WHERE sources_fts MATCH ?
                ORDER BY rank ASC
                LIMIT ?
            """, (query, limit))
            for r in cur.fetchall():
                sc = self._row_to_source(r)
                results.append((sc, r["rank"]))
        else:
            like = f"%{query}%"
            cur.execute("""
                SELECT s.*, 0.0 AS rank
                FROM source_cards s
                WHERE s.title LIKE ? OR s.author LIKE ? OR s.abstract LIKE ? OR s.reason_for_interest LIKE ?
                ORDER BY s.year DESC NULLS LAST, s.title ASC
                LIMIT ?
            """, (like, like, like, like, limit))
            for r in cur.fetchall():
                results.append((self._row_to_source(r), 0.0))
        return results

    def search_quotes(self, query: str, limit: int = 50) -> List[Tuple[QuoteCard, float, str]]:
        """Search across direct_quote, paraphrase, and context; returns (QuoteCard, score, citation_key)."""
        cur = self.conn.cursor()
        out: List[Tuple[QuoteCard, float, str]] = []

        if self.fts_enabled:
            cur.execute("""
                SELECT q.*, bm25(quotes_fts) AS rank
                FROM quotes_fts
                JOIN quote_cards q ON q.rowid = quotes_fts.rowid
                WHERE quotes_fts MATCH ?
                ORDER BY rank ASC
                LIMIT ?
            """, (query, limit))
            for r in cur.fetchall():
                out.append((self._row_to_quote(r), r["rank"], r["citation_key"]))
        else:
            like = f"%{query}%"
            cur.execute("""
                SELECT q.*, 0.0 AS rank
                FROM quote_cards q
                WHERE q.direct_quote LIKE ? OR q.paraphrase LIKE ? OR q.context_excerpt LIKE ? OR q.tags LIKE ?
                ORDER BY q.date_added DESC, q.id DESC
                LIMIT ?
            """, (like, like, like, like, limit))
            for r in cur.fetchall():
                out.append((self._row_to_quote(r), 0.0, r["citation_key"]))
        return out

    # Convenience filters
    def search_quotes_by_tag(self, tag: str, limit: int = 50) -> List[Tuple[QuoteCard, str]]:
        cur = self.conn.cursor()
        like = f"%{tag}%"
        cur.execute("""
            SELECT * FROM quote_cards
            WHERE tags LIKE ?
            ORDER BY date_added DESC, id DESC
            LIMIT ?
        """, (like, limit))
        return [(self._row_to_quote(r), r["citation_key"]) for r in cur.fetchall()]

    def list_sources(self) -> List[Tuple[str, Optional[str], Optional[int]]]:
        """Quick list: (citation_key, title, year)."""
        cur = self.conn.cursor()
        cur.execute("SELECT citation_key, title, year FROM source_cards ORDER BY year DESC NULLS LAST, title ASC")
        return [(r["citation_key"], r["title"], r["year"]) for r in cur.fetchall()]

    # ------------- FTS upsert helpers -------------
    def _upsert_sources_fts(self, citation_key: str):
        """Push current source row into sources_fts."""
        cur = self.conn.cursor()
        cur.execute("SELECT id, title, author, abstract, reason_for_interest, journal, publisher, booktitle, doi, url FROM source_cards WHERE citation_key=?", (citation_key,))
        r = cur.fetchone()
        if not r:
            return
        cur.execute("DELETE FROM sources_fts WHERE rowid=?", (r["id"],))
        cur.execute("""
            INSERT INTO sources_fts(rowid, title, author, abstract, reason_for_interest, journal, publisher, booktitle, doi, url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["id"], r["title"], r["author"], r["abstract"], r["reason_for_interest"], r["journal"], r["publisher"], r["booktitle"], r["doi"], r["url"]))
        self.conn.commit()

    def _upsert_quotes_fts(self, quote_rowid: int):
        """Push current quote row into quotes_fts."""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id, direct_quote, paraphrase, context_excerpt, tags, topic, category, commentary, relevance
            FROM quote_cards WHERE id=?
        """, (quote_rowid,))
        r = cur.fetchone()
        if not r:
            return
        cur.execute("DELETE FROM quotes_fts WHERE rowid=?", (r["id"],))
        cur.execute("""
            INSERT INTO quotes_fts(rowid, direct_quote, paraphrase, context_excerpt, tags, topic, category, commentary, relevance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["id"], r["direct_quote"], r["paraphrase"], r["context_excerpt"], r["tags"], r["topic"], r["category"], r["commentary"], r["relevance"]))
        self.conn.commit()

    # Rebuild FTS from scratch (handy after bulk imports)
    def rebuild_fts(self):
        if not self.fts_enabled:
            return
        cur = self.conn.cursor()
        cur.execute("DELETE FROM sources_fts")
        cur.execute("DELETE FROM quotes_fts")
        cur.execute("SELECT citation_key FROM source_cards")
        for r in cur.fetchall():
            self._upsert_sources_fts(r["citation_key"])
        cur.execute("SELECT id FROM quote_cards")
        for r in cur.fetchall():
            self._upsert_quotes_fts(r["id"])
        self.conn.commit()

    # ------------- Export -------------
    def export_all_bibtex(self, filepath: Optional[str] = "library_export.bib") -> str:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM source_cards ORDER BY year DESC NULLS LAST, title ASC")
        bibs = []
        for r in cur.fetchall():
            src = self._row_to_source(r)
            bibs.append(src.to_bibtex())
        content = "\n\n".join(bibs)
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
        return content


# --- tiny query language + engine (drop-in on top of your SourceDatabase) ---

# -----------------------------
# Parsing
# -----------------------------

_FIELD_OP_RE = re.compile(r"^(?P<field>[a-zA-Z_][a-zA-Z0-9_]*)\s*(?P<op>:|=|<=|>=|<|>)\s*(?P<value>.+)$")
_RANGE_RE = re.compile(r"^(?P<lo>-?\d+)\.\.(?P<hi>-?\d+)$")

# Columns available for field:term on sources_fts / source_cards
SOURCE_TEXT_COLUMNS = {
    "title", "author", "editor", "abstract", "reason_for_interest", "journal",
    "publisher", "booktitle", "doi", "url", "series", "note", "address",
    "organization", "school", "institution", "howpublished"
}
SOURCE_NUM_COLUMNS = {"year"}

# Columns available for field:term on quotes_fts / quote_cards
QUOTE_TEXT_COLUMNS = {
    "direct_quote", "paraphrase", "context_excerpt", "tags", "topic",
    "category", "commentary", "relevance", "chapter", "timestamp"
}
QUOTE_NUM_COLUMNS = {"page"}

def _split_or_groups(q: str) -> List[str]:
    """Split on OR not inside quotes. Implicit AND within a group."""
    out, buf, in_quotes = [], [], False
    i = 0
    while i < len(q):
        ch = q[i]
        if ch == '"':
            in_quotes = not in_quotes
            buf.append(ch)
            i += 1
            continue
        if not in_quotes and q[i:i+3].upper() == " OR":
            # finalize group
            out.append("".join(buf).strip())
            buf = []
            i += 3
            continue
        buf.append(ch)
        i += 1
    if buf:
        out.append("".join(buf).strip())
    # Clean empties
    return [g for g in out if g]

def _tokenize(group: str) -> List[str]:
    """Split by whitespace but keep quoted phrases."""
    tokens, buf, in_quotes = [], [], False
    for ch in group.strip():
        if ch == '"':
            in_quotes = not in_quotes
            buf.append(ch)
        elif ch.isspace() and not in_quotes:
            if buf:
                tokens.append("".join(buf))
                buf = []
        else:
            buf.append(ch)
    if buf:
        tokens.append("".join(buf))
    return tokens

@dataclass
class Clause:
    # A clause is either a free text term (phrase) or a fielded filter with an operator
    field: Optional[str] = None
    op: Optional[str] = None        # :, =, <=, >=, <, >
    value: Optional[str] = None     # raw value
    is_text: bool = False           # true for bare terms like: "deep learning"

@dataclass
class ParsedGroup:
    clauses: List[Clause]           # AND across clauses

@dataclass
class ParsedQuery:
    groups: List[ParsedGroup]       # OR across groups

def parse_query(q: str) -> ParsedQuery:
    """Parse into OR-groups of AND-clauses."""
    groups = []
    for g in _split_or_groups(q):
        clauses: List[Clause] = []
        for tok in _tokenize(g):
            # strip surrounding quotes for values later; keep them here for type detection
            m = _FIELD_OP_RE.match(tok)
            if m:
                field = m.group("field").lower()
                op = m.group("op")
                value = m.group("value")
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                clauses.append(Clause(field=field, op=op, value=value, is_text=False))
            else:
                # free text
                if tok.startswith('"') and tok.endswith('"'):
                    tok = tok[1:-1]
                clauses.append(Clause(is_text=True, value=tok))
        groups.append(ParsedGroup(clauses=clauses))
    return ParsedQuery(groups=groups)

# -----------------------------
# Compiler to SQL/FTS
# -----------------------------

class QueryEngine:
    """
    Compiles the tiny DSL to SQL for sources and quotes.
    Uses FTS5 MATCH + bm25 when db.fts_enabled=True, otherwise LIKE fallback.
    """

    def __init__(self, db: "SourceDatabase"):
        self.db = db

    # ---- PUBLIC API ---------------------------------------------------------

    def search_sources(self, query: str, limit: int = 25) -> List[Tuple["SourceCard", float]]:
        pq = parse_query(query)
        sql, params, use_rank = self._compile_sources_sql(pq, limit)
        cur = self.db.conn.cursor()
        cur.execute(sql, params)
        rows = cur.fetchall()
        out = []
        for r in rows:
            sc = self.db._row_to_source(r)
            score = r["rank"] if use_rank else 0.0
            out.append((sc, score))
        return out

    def search_quotes(self, query: str, limit: int = 50) -> List[Tuple["QuoteCard", float, str]]:
        pq = parse_query(query)
        sql, params, use_rank = self._compile_quotes_sql(pq, limit)
        cur = self.db.conn.cursor()
        cur.execute(sql, params)
        rows = cur.fetchall()
        out = []
        for r in rows:
            qc = self.db._row_to_quote(r)
            score = r["rank"] if use_rank else 0.0
            out.append((qc, score, r["citation_key"]))
        return out

    # ---- COMPILERS ----------------------------------------------------------

    def _compile_sources_sql(self, pq: ParsedQuery, limit: int) -> Tuple[str, List[Any], bool]:
        """
        Returns (sql, params, use_rank)
        - If FTS is enabled and any text/fielded-text present, builds an FTS MATCH query joined to source_cards.
        - Always applies numeric/range filters (e.g., year) via SQL WHERE.
        - OR between groups, AND within a group.
        """
        fts_terms_by_group: List[str] = []
        where_by_group: List[str] = []
        params: List[Any] = []

        any_text = False

        for g in pq.groups:
            fts_terms: List[str] = []
            where_terms: List[str] = []
            for c in g.clauses:
                if c.is_text:
                    any_text = True
                    if self.db.fts_enabled:
                        # bare terms hit all FTS columns
                        fts_terms.append(_fts_escape(c.value))
                    else:
                        # LIKE fallback across key text columns
                        like = f"%{c.value}%"
                        where_terms.append("(" + " OR ".join([f"s.{col} LIKE ?" for col in ["title", "author", "abstract", "reason_for_interest", "journal", "publisher", "booktitle"]]) + ")")
                        params.extend([like] * 7)
                else:
                    # fielded
                    if c.field in SOURCE_NUM_COLUMNS:
                        # numeric / range
                        if c.op == ":":
                            rng = _as_range(c.value)
                            if rng:
                                where_terms.append("(s.year >= ? AND s.year <= ?)")
                                params.extend([rng[0], rng[1]])
                            else:
                                where_terms.append("s.year = ?")
                                params.append(int(c.value))
                        elif c.op in (">=", "<=", ">", "<", "="):
                            where_terms.append(f"s.{c.field} {c.op} ?")
                            params.append(int(c.value))
                    elif c.field in SOURCE_TEXT_COLUMNS:
                        # text field
                        if self.db.fts_enabled and c.op in (":", "="):
                            # column-specific FTS
                            fts_terms.append(f"{c.field}:{_fts_escape(c.value)}")
                            any_text = True
                        else:
                            like = f"%{c.value}%"
                            where_terms.append(f"s.{c.field} LIKE ?")
                            params.append(like)
                    elif c.field in {"tag", "tags"}:
                        # tags are in quotes table; allow source-level search by joining via EXISTS
                        like = f"%{c.value}%"
                        where_terms.append("EXISTS (SELECT 1 FROM quote_cards q WHERE q.citation_key = s.citation_key AND q.tags LIKE ?)")
                        params.append(like)
                    else:
                        # unknown field -> treat as free text
                        if self.db.fts_enabled:
                            fts_terms.append(_fts_escape(f"{c.field}:{c.value}"))
                            any_text = True
                        else:
                            like = f"%{c.value}%"
                            where_terms.append("(" + " OR ".join([f"s.{col} LIKE ?" for col in ["title", "author", "abstract", "reason_for_interest"]]) + ")")
                            params.extend([like] * 4)

            fts_terms_by_group.append(" AND ".join(fts_terms) if fts_terms else "")
            where_by_group.append(" AND ".join(where_terms) if where_terms else "")

        use_rank = self.db.fts_enabled and any(any(t.strip() for t in fts_terms_by_group))
        # Build OR across groups
        if self.db.fts_enabled and use_rank:
            # Join FTS with cards
            ors = []
            for fts, wh in zip(fts_terms_by_group, where_by_group):
                parts = []
                if fts:
                    parts.append("(sources_fts MATCH ?)")
                    params.insert(len(params), fts)  # ensure fts param order aligns; append is fine too
                if wh:
                    parts.append(f"({wh})")
                ors.append("(" + " AND ".join(parts) + ")" if parts else "(1=1)")
            where_sql = " OR ".join(ors) if ors else "1=1"
            sql = f"""
                SELECT s.*, bm25(sources_fts) AS rank
                FROM sources_fts
                JOIN source_cards s ON s.rowid = sources_fts.rowid
                WHERE {where_sql}
                ORDER BY rank ASC
                LIMIT {int(limit)}
            """
        else:
            # LIKE fallback: no FTS table
            ors = []
            # in fallback, fts_terms are transformed already into LIKE in where_by_group
            for wh in where_by_group:
                if wh.strip():
                    ors.append(f"({wh})")
                else:
                    ors.append("(1=1)")
            where_sql = " OR ".join(ors) if ors else "1=1"
            sql = f"""
                SELECT s.*, 0.0 AS rank
                FROM source_cards s
                WHERE {where_sql}
                ORDER BY s.year DESC NULLS LAST, s.title ASC
                LIMIT {int(limit)}
            """
        return sql, params, use_rank

    def _compile_quotes_sql(self, pq: ParsedQuery, limit: int) -> Tuple[str, List[Any], bool]:
        fts_terms_by_group: List[str] = []
        where_by_group: List[str] = []
        params: List[Any] = []
        any_text = False

        for g in pq.groups:
            fts_terms: List[str] = []
            where_terms: List[str] = []
            for c in g.clauses:
                if c.is_text:
                    if self.db.fts_enabled:
                        fts_terms.append(_fts_escape(c.value))
                        any_text = True
                    else:
                        like = f"%{c.value}%"
                        where_terms.append("(" + " OR ".join([f"q.{col} LIKE ?" for col in ["direct_quote", "paraphrase", "context_excerpt", "tags", "topic", "category"]]) + ")")
                        params.extend([like] * 6)
                else:
                    # fielded
                    if c.field in QUOTE_NUM_COLUMNS:
                        if c.op == ":":
                            rng = _as_range(c.value)
                            if rng:
                                where_terms.append("(q.page >= ? AND q.page <= ?)")
                                params.extend([rng[0], rng[1]])
                            else:
                                where_terms.append("q.page = ?")
                                params.append(int(c.value))
                        else:
                            where_terms.append(f"q.{c.field} {c.op} ?")
                            params.append(int(c.value))
                    elif c.field in QUOTE_TEXT_COLUMNS:
                        if self.db.fts_enabled and c.op in (":", "="):
                            fts_terms.append(f"{c.field}:{_fts_escape(c.value)}")
                            any_text = True
                        else:
                            like = f"%{c.value}%"
                            where_terms.append(f"q.{c.field} LIKE ?")
                            params.append(like)
                    elif c.field in SOURCE_TEXT_COLUMNS or c.field in SOURCE_NUM_COLUMNS:
                        # Allow filtering quotes by source fields via join to source_cards
                        if c.field == "year":
                            if c.op == ":":
                                rng = _as_range(c.value)
                                if rng:
                                    where_terms.append("(s.year >= ? AND s.year <= ?)")
                                    params.extend([rng[0], rng[1]])
                                else:
                                    where_terms.append("s.year = ?")
                                    params.append(int(c.value))
                            else:
                                where_terms.append(f"s.year {c.op} ?")
                                params.append(int(c.value))
                        else:
                            like = f"%{c.value}%"
                            where_terms.append(f"s.{c.field} LIKE ?")
                            params.append(like)
                    elif c.field in {"tag", "tags"}:
                        like = f"%{c.value}%"
                        where_terms.append("q.tags LIKE ?")
                        params.append(like)
                    else:
                        if self.db.fts_enabled:
                            fts_terms.append(_fts_escape(f"{c.field}:{c.value}"))
                            any_text = True
                        else:
                            like = f"%{c.value}%"
                            where_terms.append("(" + " OR ".join([f"q.{col} LIKE ?" for col in ["direct_quote", "paraphrase", "context_excerpt"]]) + ")")
                            params.extend([like] * 3)

            fts_terms_by_group.append(" AND ".join(fts_terms) if fts_terms else "")
            where_by_group.append(" AND ".join(where_terms) if where_terms else "")

        use_rank = self.db.fts_enabled and any(any(t.strip() for t in fts_terms_by_group))
        if self.db.fts_enabled and use_rank:
            ors = []
            for fts, wh in zip(fts_terms_by_group, where_by_group):
                parts = []
                if fts:
                    parts.append("(quotes_fts MATCH ?)")
                    params.insert(len(params), fts)
                if wh:
                    parts.append(f"({wh})")
                ors.append("(" + " AND ".join(parts) + ")" if parts else "(1=1)")
            where_sql = " OR ".join(ors) if ors else "1=1"
            sql = f"""
                SELECT q.*, q.citation_key, bm25(quotes_fts) AS rank
                FROM quotes_fts
                JOIN quote_cards q ON q.rowid = quotes_fts.rowid
                LEFT JOIN source_cards s ON s.citation_key = q.citation_key
                WHERE {where_sql}
                ORDER BY rank ASC
                LIMIT {int(limit)}
            """
        else:
            ors = []
            for wh in where_by_group:
                ors.append(f"({wh})" if wh else "(1=1)")
            where_sql = " OR ".join(ors) if ors else "1=1"
            sql = f"""
                SELECT q.*, q.citation_key, 0.0 AS rank
                FROM quote_cards q
                LEFT JOIN source_cards s ON s.citation_key = q.citation_key
                WHERE {where_sql}
                ORDER BY q.date_added DESC, q.id DESC
                LIMIT {int(limit)}
            """
        return sql, params, use_rank

# -----------------------------
# Utilities
# -----------------------------

def _fts_escape(s: str) -> str:
    """
    Escape FTS5 special chars minimally; also convert spaces to AND for better matching.
    Quoted phrases are passed as-is.
    """
    s = s.strip()
    if " " in s and not (s.startswith('"') and s.endswith('"')):
        # split into tokens and AND them
        parts = [p for p in re.split(r"\s+", s) if p]
        return " AND ".join(_fts_token_escape(p) for p in parts)
    return _fts_token_escape(s)

def _fts_token_escape(tok: str) -> str:
    tok = tok.replace("'", "''")
    # FTS supports simple tokens; avoid special chars acting weird
    return tok

def _as_range(value: str) -> Optional[Tuple[int, int]]:
    m = __RANGE_RE.match(value)
    if not m:
        return None
    lo, hi = int(m.group("lo")), int(m.group("hi"))
    if lo > hi:
        lo, hi = hi, lo
    return lo, hi

