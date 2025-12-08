"""
app.py
---------------------------
Dies ist die Hauptdatei der Flask-Anwendung.

Sie kümmert sich um:
- Initialisierung der App
- Laden der Datenbank
- Definieren der API-Routen
- Ausliefern des HTML-Frontends
- Drag & Drop Endpoint zum Verschieben von Themen
"""

from flask import Flask, render_template, request, jsonify
from models import db, Jahrgang, Thema, ThemaJahrgang
import os
from datetime import datetime


# ----------------------------------------------------
# Flask-App konfigurieren
# ----------------------------------------------------
app = Flask(__name__)

# Pfad zur SQLite-Datenbank (curriculum.db)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "curriculum.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Datenbank für Flask initialisieren
db.init_app(app)


# ----------------------------------------------------
# Startseite: lädt das HTML-Frontend
# ----------------------------------------------------
@app.route("/")
def index():
    """
    Gibt die HTML-Oberfläche zurück (templates/index.html).
    Alles weitere wird per JavaScript über die API geladen.
    """
    return render_template("index.html")


# ----------------------------------------------------
# API: Liste aller Jahrgänge
# ----------------------------------------------------
@app.route("/api/jahrgaenge")
def api_jahrgaenge():
    jahrgaenge = Jahrgang.query.order_by(Jahrgang.ordnung).all()

    # JSON-Antwort bauen
    return jsonify([
        {"id": j.id, "name": j.name}
        for j in jahrgaenge
    ])


# ----------------------------------------------------
# API: Themen suchen oder alle Themen laden
# ----------------------------------------------------
@app.route("/api/themen")
def api_themen():
    """
    Parameter:
      q: optionaler Suchtext
    """
    q = request.args.get("q", "").strip()

    query = Thema.query

    # Falls suche → Titel/Beschreibung/Fachbereich durchsuchen
    if q:
        query = query.filter(
            (Thema.titel.contains(q)) |
            (Thema.beschreibung.contains(q)) |
            (Thema.fachbereich.contains(q))
        )

    themen = query.all()

    # JSON-Antwort: zusätzlich Zugehörigkeit zu Jahrgängen anhängen
    response = []
    for t in themen:
        mapping = ThemaJahrgang.query.filter_by(thema_id=t.id).all()

        jahrgaenge = [
            {"id": m.jahrgang_id, "position": m.position}
            for m in mapping
        ]

        response.append({
            "id": t.id,
            "titel": t.titel,
            "beschreibung": t.beschreibung,
            "jahrgaenge": jahrgaenge
        })

    return jsonify(response)


# ----------------------------------------------------
# API: Thema in anderen Jahrgang verschieben
# ----------------------------------------------------
@app.route("/api/move_thema", methods=["POST"])
def api_move_thema():
    """
    Erwartet JSON:
    {
        "thema_id": 3,
        "target_jahrgang_id": 2,
        "position": 4
    }
    """
    data = request.get_json()

    thema_id = data["thema_id"]
    jahrgang_id = data["target_jahrgang_id"]
    position = data.get("position", 0)

    # Eintrag suchen oder neu anlegen
    mapping = ThemaJahrgang.query.filter_by(thema_id=thema_id, jahrgang_id=jahrgang_id).first()

    if mapping:
        mapping.position = position
    else:
        mapping = ThemaJahrgang(
            thema_id=thema_id,
            jahrgang_id=jahrgang_id,
            position=position
        )
        db.session.add(mapping)

    db.session.commit()

    return jsonify({"status": "ok"})


# ----------------------------------------------------
# API: DB initialisieren (nur für dich im lokalen Dev-Modus)
# ----------------------------------------------------
@app.route("/init_db")
def init_db():
    """
    Erstellt alle Tabellen und legt Beispiel-Jahrgänge an.
    Wird nur einmal verwendet.
    """

     # App-Kontext erzwingen:
    with app.app_context():
        db.create_all()

        if Jahrgang.query.count() == 0:
            db.session.add_all([
                Jahrgang(name="Jahrgang 5", ordnung=1),
                Jahrgang(name="Jahrgang 6", ordnung=2),
                Jahrgang(name="Jahrgang 7", ordnung=3)
            ])
        db.session.commit()

    return "Datenbank initialisiert ✔"


# -----------------------------------------------------
# Formular anzeigen
# -----------------------------------------------------
@app.route("/thema/new")
def thema_new():
    jahrgaenge = Jahrgang.query.order_by(Jahrgang.ordnung).all()
    return render_template("thema_new.html", jahrgaenge=jahrgaenge)

# ------------------------------------------------------
# Thema speichern
# ------------------------------------------------------
@app.route("/thema/create", methods=["POST"])
def thema_create():
    titel = request.form["titel"]
    beschreibung = request.form.get("beschreibung", "")
    fachbereich = request.form.get("fachbereich", "")
    methode = request.form.get("methode", "")
    digitale_hilfsmittel = request.form.get("digitale_hilfsmittel", "")
    schwierigkeit = int(request.form.get("schwierigkeit", 1))

    # Neues Thema anlegen
    thema = Thema(
        titel=titel,
        beschreibung=beschreibung,
        fachbereich=fachbereich,
        schwierigkeit=schwierigkeit
    )

    # Neue zusätzliche Felder (werden in models.py ergänzt!)
    thema.methode = methode
    thema.digitale_hilfsmittel = digitale_hilfsmittel

    db.session.add(thema)
    db.session.commit()

    # Jahrgang-Zuordnung
    jahrgang_ids = request.form.getlist("jahrgang_ids")

    for jid in jahrgang_ids:
        mapping = ThemaJahrgang(
            thema_id=thema.id,
            jahrgang_id=int(jid),
            position=0
        )
        db.session.add(mapping)

    db.session.commit()

    return render_template("index.html")


# ----------------------------------------------------
# App lokal starten
# ----------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
