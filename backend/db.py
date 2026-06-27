import json
from datetime import datetime, timezone
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from schemas import AnalyzeResponse, ScanSummary
from settings import get_settings

_engine = None


def _get_engine():
    global _engine
    if _engine:
        return _engine

    settings = get_settings()
    url = settings.database_url

    if url.startswith("sqlite"):
        _engine = create_engine(
            url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
    else:
        _engine = create_engine(url)

    _init_table(_engine)
    return _engine


def _init_table(engine):
    is_sqlite = str(engine.url).startswith("sqlite")
    id_col = "INTEGER PRIMARY KEY AUTOINCREMENT" if is_sqlite else "INTEGER PRIMARY KEY AUTO_INCREMENT"
    with engine.connect() as conn:
        conn.execute(text(f"""
            CREATE TABLE IF NOT EXISTS scans (
                id {id_col},
                image_filename TEXT,
                hard_hat TEXT,
                hi_vis TEXT,
                fatigue_risk TEXT,
                priority TEXT,
                supervisor_action TEXT,
                zone_id TEXT,
                zone_name TEXT,
                zone_overall TEXT,
                vision_json TEXT,
                nemotron_json TEXT,
                zone_json TEXT,
                provider_vision TEXT,
                provider_nemotron TEXT,
                created_at TEXT
            )
        """))
        conn.commit()
        _migrate_scans_table(conn)


def _migrate_scans_table(conn):
    """Add columns introduced after initial schema (CREATE IF NOT EXISTS does not alter)."""
    if not str(conn.engine.url).startswith("sqlite"):
        return
    existing = {
        row[1]
        for row in conn.execute(text("PRAGMA table_info(scans)")).fetchall()
    }
    for col, col_type in [
        ("zone_id", "TEXT"),
        ("zone_name", "TEXT"),
        ("zone_overall", "TEXT"),
        ("zone_json", "TEXT"),
        ("provider_vision", "TEXT"),
        ("provider_nemotron", "TEXT"),
    ]:
        if col not in existing:
            conn.execute(text(f"ALTER TABLE scans ADD COLUMN {col} {col_type}"))
    conn.commit()


def save_scan(result: AnalyzeResponse) -> int:
    engine = _get_engine()
    ts = datetime.now(timezone.utc).isoformat()
    zc = result.zone_compliance
    with engine.connect() as conn:
        r = conn.execute(text("""
            INSERT INTO scans
              (image_filename, hard_hat, hi_vis, fatigue_risk, priority,
               supervisor_action, zone_id, zone_name, zone_overall,
               vision_json, nemotron_json, zone_json,
               provider_vision, provider_nemotron, created_at)
            VALUES
              (:image_filename, :hard_hat, :hi_vis, :fatigue_risk, :priority,
               :supervisor_action, :zone_id, :zone_name, :zone_overall,
               :vision_json, :nemotron_json, :zone_json,
               :provider_vision, :provider_nemotron, :created_at)
        """), {
            "image_filename": result.image_filename,
            "hard_hat": result.vision.ppe.hard_hat,
            "hi_vis": result.vision.ppe.hi_vis,
            "fatigue_risk": result.vision.fatigue.risk,
            "priority": result.nemotron.priority,
            "supervisor_action": result.nemotron.supervisor_action,
            "zone_id": zc.zone_id if zc else None,
            "zone_name": zc.zone_name if zc else None,
            "zone_overall": zc.overall if zc else None,
            "vision_json": result.vision.model_dump_json(),
            "nemotron_json": result.nemotron.model_dump_json(),
            "zone_json": zc.model_dump_json() if zc else None,
            "provider_vision": result.provider.vision,
            "provider_nemotron": result.provider.nemotron,
            "created_at": ts,
        })
        conn.commit()
        row_id = r.lastrowid
        if not row_id:
            row_id = conn.execute(text("SELECT last_insert_rowid()")).scalar()
        return int(row_id or 0)


def get_recent_scans(limit: int = 20) -> list[ScanSummary]:
    engine = _get_engine()
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT id, image_filename, hard_hat, hi_vis, fatigue_risk, priority, supervisor_action, zone_id, zone_name, created_at "
            "FROM scans ORDER BY id DESC LIMIT :limit"
        ), {"limit": limit}).fetchall()

    return [
        ScanSummary(
            id=row.id,
            image_filename=row.image_filename or "",
            hard_hat=row.hard_hat or "unclear",
            hi_vis=row.hi_vis or "unclear",
            fatigue_risk=row.fatigue_risk or "unclear",
            priority=row.priority or "none",
            supervisor_action=row.supervisor_action or "",
            zone_id=getattr(row, "zone_id", None),
            zone_name=getattr(row, "zone_name", None),
            created_at=row.created_at or "",
        )
        for row in rows
    ]
