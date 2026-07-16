def bepaal_prioriteit(probleem):
    if "lekt" in probleem:
        return "SPOED"
    elif "geen warm water" in probleem or "geen water" in probleem:
        return "DRINGEND"
    else:
        return "REGULIER"

klantnaam = input("Wat is uw naam? ")
probleem = input("Wat is het probleem? ")

prioriteit = bepaal_prioriteit(probleem)

print("Bedankt,", klantnaam)
print("We hebben genoteerd:", probleem)
print("Prioriteit:", prioriteit)