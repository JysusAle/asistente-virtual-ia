hechos = set()

reglas = [
    ({"tiene_fiebre", "tiene_tos"}, "posible_gripe"),
    ({"tiene_dolor_garganta", "tiene_mucosidad"}, "posible_resfriado"),
    ({"tiene_dificultad_respirar", "tiene_fiebre"}, "posible_neumonia"),
    ({"posible_gripe", "tiene_dolor_cabeza"}, "recomendar_descanso"),
    ({"posible_resfriado"}, "recomendar_liquidos")
]