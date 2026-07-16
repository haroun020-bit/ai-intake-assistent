def bepaal_prioriteit(probleem):
    if "lekt" in probleem:
        return "SPOED"
    elif "geen warm water" in probleem or "geen water" in probleem:
        return "DRINGEND"
    else:
        return "REGULIER"

problemen = ["mijn cv ketel lekt", "geen warm water", "radiator tikt", "boiler maakt lawaai", "geeen elektra" , "schade",]

for probleem in problemen:
    prioriteit = bepaal_prioriteit(probleem)
    print(probleem, "->", prioriteit)