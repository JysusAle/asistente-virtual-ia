from kb_medico import hechos, reglas

def inferir(hechos, reglas):
    nuevos_hechos = set()
    cambios = True
    
    while cambios:
        cambios = False
        for premisas, conclusion in reglas:
            if premisas.issubset(hechos) and conclusion not in hechos:
                hechos.add(conclusion)
                nuevos_hechos.add(conclusion)
                cambios = True
    return nuevos_hechos

def medico():
    print("Agente Medico Simple")

    sintomas = ["tiene_fiebre", "tiene_tos", "tiene_dolor_garganta", 
                "tiene_mucosidad", "tiene_dificultad_respirar", "tiene_dolor_cabeza"]

    for s in sintomas:
        resp = input(f"¿El paciente {s.replace('_', ' ')}? (s/n): ").lower()
        if resp == "s":
            hechos.add(s)

    nuevos = inferir(hechos, reglas)

    print("\nHechos inferidos:")
    for h in nuevos:
        print(" -", h)

    if not nuevos:
        print("No se encontró diagnóstico.")

if __name__ == "__main__":
    main()