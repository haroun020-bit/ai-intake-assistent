from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request
import anthropic
import json

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
            return json.loads(blok.text.strip())

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

        if naam.strip() == "" or probleem.strip() == "" or telefoon.strip() == "" or adres.strip() == "":
            foutmelding = "Vul alle velden in."
        else:
            resultaat = analyseer_melding(probleem)

            intake = {
                "naam": naam,
                "telefoon": telefoon,
                "adres": adres,
                "probleem": probleem,
                "prioriteit": resultaat["prioriteit"],
                "advies": resultaat["advies"]
            }
            with open("intakes.jsonl", "a") as bestand:
                bestand.write(json.dumps(intake) + "\n")

    return render_template("index.html", resultaat=resultaat, naam=naam, foutmelding=foutmelding)

@app.route("/overzicht")
def overzicht():
    alle_intakes = []
    with open("intakes.jsonl", "r") as bestand:
        for regel in bestand:
            alle_intakes.append(json.loads(regel))
    return render_template("overzicht.html", intakes=alle_intakes)

if __name__ == "__main__":
    app.run(debug=True)