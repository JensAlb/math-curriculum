-- -----------------------------------------
-- SQLite-Datenbankschema für Mathematik-Curriculum
-- -----------------------------------------

BEGIN TRANSACTION;

-- Tabelle: Jahrgänge (5,6,7,... / Unter-, Mittel-, Oberstufe)
CREATE TABLE IF NOT EXISTS jahrgang (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,        -- z.B.: "Jahrgang 7"
  ordnung INTEGER NOT NULL DEFAULT 0
);

-- Tabelle: Themen
CREATE TABLE IF NOT EXISTS thema (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  titel TEXT NOT NULL,              -- z.B.: "Lineare Funktionen"
  beschreibung TEXT,                -- längere Beschreibung
  schwierigkeit INTEGER DEFAULT 1,  -- von 1 bis 5
  fachbereich TEXT,                 -- "Zahl", "Geometrie", "Funktionen", ...
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME
);

-- Materialien zu Themen
CREATE TABLE IF NOT EXISTS material (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  thema_id INTEGER NOT NULL,
  titel TEXT NOT NULL,              -- Name des Materials
  dateiname TEXT,                   -- optional; falls Datei vorhanden
  typ TEXT,                         -- "Arbeitsblatt", "PDF", "Link"
  url TEXT,                         -- optional; Link
  bemerkung TEXT,
  FOREIGN KEY (thema_id) REFERENCES thema(id) ON DELETE CASCADE
);

-- Zuordnungstabelle Thema ↔ Jahrgang
-- Ein Thema kann in mehreren Jahrgängen vorkommen
CREATE TABLE IF NOT EXISTS thema_jahrgang (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  thema_id INTEGER NOT NULL,
  jahrgang_id INTEGER NOT NULL,
  position INTEGER DEFAULT 0,       -- Reihenfolge im Jahrgang
  UNIQUE(thema_id, jahrgang_id),
  FOREIGN KEY (thema_id) REFERENCES thema(id) ON DELETE CASCADE,
  FOREIGN KEY (jahrgang_id) REFERENCES jahrgang(id) ON DELETE CASCADE
);

COMMIT;
