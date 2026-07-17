from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect
import anthropic
import json
from datetime import datetime

app = Flask(__name__)
client = anthropic.Anthropic()

def analyseer_melding(probleem):
    antwoord = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=500,
        system="Je bent de intake-assistent van een installatiebedrijf. Beoordeel meldingen volgens deze regels: SPOED = waterschade, gaslucht, of directe veiligheidsrisico's. DRINGEND = geen warm water, geen verwarming bij koud weer, geen stroom. REGULIER = alle overige klachten. Antwoord ALLEEN met geldige JSON in dit exacte formaat, zonder extra tekst: {\"prioriteit\": \"...\", \"advies\": \"...\"}. Het advies is één korte zin voor de monteur.",
        messages=[
            {"role": "user", "content": probleem}
        ]
    )
    for blok in antwoord.content:
        if blok.type == "text":
            try:
                return json.loads(blok.text.strip())
            except json.JSONDecodeError:
                return {
                    "prioriteit": "REGULIER",
                    "advies": "Kon niet automatisch worden geanalyseerd, graag handmatig beoordelen."
                }

@app.route("/", methods=["GET", "POST"])
def home():
    resultaat = None
    naam = None
    foutmelding = None

    if request.method == "POST":
        naam = request.form["naam"]
        telefoon = request.form["telefoon"]
        adres = request.form["adres"]
        probleem = request.form["probleem"]

        velden_leeg = (
            naam.strip() == "" or
            probleem.strip() == "" or
            telefoon.strip() == "" or
            adres.strip() == ""
        )

        if velden_leeg:
            foutmelding = "Vul alle velden in."
        else:
            resultaat = analyseer_melding(probleem)

            intake = {
                "naam": naam,
                "telefoon": telefoon,
                "adres": adres,
                "probleem": probleem,
                "prioriteit": resultaat["prioriteit"],
                "advies": resultaat["advies"],
                "status": "nieuw",
                "tijdstip": datetime.now().strftime("%d-%m-%Y %H:%M")
            }
            with open("intakes.jsonl", "a") as bestand:
                bestand.write(json.dumps(intake) + "\n")

    return render_template("index.html", resultaat=resultaat, naam=naam, foutmelding=foutmelding)

def laad_alle_intakes():
    alle_intakes = []
    with open("intakes.jsonl", "r") as bestand:
        for i, regel in enumerate(bestand):
            intake = json.loads(regel)
            intake["id"] = i
            if "status" not in intake:
                intake["status"] = "nieuw"
            alle_intakes.append(intake)
    return alle_intakes

@app.route("/overzicht")
def overzicht():
    alle_intakes = laad_alle_intakes()

    prioriteit_volgorde = {"SPOED": 0, "DRINGEND": 1, "REGULIER": 2}
    alle_intakes.sort(key=lambda intake: prioriteit_volgorde.get(intake["prioriteit"], 3))

    return render_template("overzicht.html", intakes=alle_intakes)

@app.route("/status/<int:intake_id>/<nieuwe_status>", methods=["POST"])
def wijzig_status(intake_id, nieuwe_status):
    alle_intakes = laad_alle_intakes()
    alle_intakes[intake_id]["status"] = nieuwe_status

    with open("intakes.jsonl", "w") as bestand:
        for intake in alle_intakes:
            intake_zonder_id = {k: v for k, v in intake.items() if k != "id"}
            bestand.write(json.dumps(intake_zonder_id) + "\n")

    return redirect("/overzicht")

if __name__ == "__main__":
    app.run(debug=True)