"""
Base de datos SQLite para persistencia del bot.
Usa aiosqlite para acceso async.
"""

import aiosqlite
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).parent.parent / "data" / "arca_bot.db"


async def init_db():
    """Inicializa la base de datos y crea las tablas si no existen."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS vigilancias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                denominacion TEXT NOT NULL,
                clase INTEGER DEFAULT -1,
                last_check TEXT,
                last_count INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now')),
                UNIQUE(telegram_id, denominacion, clase)
            )
        """)
        await db.commit()
        logger.info(f"[DB] Base de datos inicializada en {DB_PATH}")


async def agregar_vigilancia(telegram_id: int, denominacion: str, clase: int = -1) -> bool:
    """Agrega una marca a vigilar. Retorna False si ya existe."""
    async with aiosqlite.connect(DB_PATH) as db:
        try:
            await db.execute(
                "INSERT INTO vigilancias (telegram_id, denominacion, clase) VALUES (?, ?, ?)",
                (telegram_id, denominacion.upper(), clase),
            )
            await db.commit()
            return True
        except aiosqlite.IntegrityError:
            return False


async def eliminar_vigilancia(telegram_id: int, denominacion: str) -> bool:
    """Elimina una vigilancia. Retorna True si se eliminó."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "DELETE FROM vigilancias WHERE telegram_id = ? AND denominacion = ?",
            (telegram_id, denominacion.upper()),
        )
        await db.commit()
        return cursor.rowcount > 0


async def listar_vigilancias(telegram_id: int) -> list[dict]:
    """Lista las vigilancias activas de un usuario."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM vigilancias WHERE telegram_id = ? ORDER BY created_at",
            (telegram_id,),
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def obtener_todas_vigilancias() -> list[dict]:
    """Obtiene todas las vigilancias (para el monitor)."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM vigilancias")
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def actualizar_vigilancia(vigilancia_id: int, count: int):
    """Actualiza el last_check y last_count de una vigilancia."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE vigilancias SET last_check = datetime('now'), last_count = ? WHERE id = ?",
            (count, vigilancia_id),
        )
        await db.commit()
