import anthropic
import json

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

klantnaam = input("Wat is uw naam? ")
probleem = input("Wat is het probleem? ")

resultaat = analyseer_melding(probleem)

print("Bedankt,", klantnaam)
print("We hebben genoteerd:", probleem)
print("Prioriteit:", resultaat["prioriteit"])
print("Advies voor monteur:", resultaat["advies"])

# De volledige intake samenvoegen en opslaan
intake = {
    "naam": klantnaam,
    "probleem": probleem,
    "prioriteit": resultaat["prioriteit"],
    "advies": resultaat["advies"]
}

with open("intakes.jsonl", "a") as bestand:
    bestand.write(json.dumps(intake) + "\n")

print("Intake opgeslagen in intakes.jsonl")