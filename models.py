"""
models.py
---------------------------
Enthält alle SQLAlchemy-Datenbankmodelle.
Damit trennst du Datenlogik (Modelle) von der App-Logik.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Diese Variable wird in app.py initialisiert
db = SQLAlchemy()


# ----------------------------------------------------
# Jahrgang (z.B. 5, 6, 7, 8, 9, …)
# ----------------------------------------------------
class Jahrgang(db.Model):
    """
    Repräsentiert einen Jahrgang in der Schule.
    Die Sortierreihenfolge ('ordnung') legt fest, wie er angezeigt wird.
    """
    __tablename__ = "jahrgang"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    ordnung = db.Column(db.Integer, default=0)


# ----------------------------------------------------
# Thema (z.B. "Lineare Funktionen")
# ----------------------------------------------------
class Thema(db.Model):
    """
    Repräsentiert ein einzelnes mathematisches Thema.
    Ein Thema kann mehreren Jahrgängen zugeordnet sein.
    """
    __tablename__ = "thema"

    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String, nullable=False)
    beschreibung = db.Column(db.Text)
    schwierigkeit = db.Column(db.Integer, default=1)
    fachbereich = db.Column(db.String)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)


# ----------------------------------------------------
# Unterrichtsmaterialien
# ----------------------------------------------------
class Material(db.Model):
    """
    Materialien sind einem Thema eindeutig zugeordnet.
    """
    __tablename__ = "material"

    id = db.Column(db.Integer, primary_key=True)
    thema_id = db.Column(db.Integer, db.ForeignKey("thema.id"), nullable=False)

    titel = db.Column(db.String, nullable=False)
    dateiname = db.Column(db.String)  # falls lokal gespeichert
    typ = db.Column(db.String)        # z.B. "Arbeitsblatt", "Link"
    url = db.Column(db.String)
    bemerkung = db.Column(db.String)


# ----------------------------------------------------
# Beziehung: Thema ↔ Jahrgang
# (Many-to-Many mit Zusatzattribut 'position')
# ----------------------------------------------------
class ThemaJahrgang(db.Model):
    """
    Bindeglied zwischen Themen und Jahrgängen.
    'position' bestimmt die Reihenfolge der Themen in einem Jahrgang.
    """
    __tablename__ = "thema_jahrgang"

    id = db.Column(db.Integer, primary_key=True)
    thema_id = db.Column(db.Integer, db.ForeignKey("thema.id"), nullable=False)
    jahrgang_id = db.Column(db.Integer, db.ForeignKey("jahrgang.id"), nullable=False)

    # Reihenfolge des Themas innerhalb eines Jahrgangs
    position = db.Column(db.Integer, default=0)
