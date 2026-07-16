import json

alle_intakes = []

with open("intakes.jsonl", "r") as bestand:
    for regel in bestand:
        intake = json.loads(regel)
        alle_intakes.append(intake)

print("Aantal intakes:", len(alle_intakes))
print()

for intake in alle_intakes:
    print(intake["naam"], "-", intake["probleem"], "->", intake["prioriteit"])

# Bonus: alleen de SPOED-meldingen tonen
print()
print("Spoedmeldingen:")
for intake in alle_intakes:
    if intake["prioriteit"] == "SPOED":
        print("-", intake["naam"], ":", intake["probleem"])