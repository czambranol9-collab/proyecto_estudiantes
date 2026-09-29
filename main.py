from models import CAMPOS_ESTUDIANTE
from shared.herramientas import (
    imprimir_titulo,
    imprimir_exito,
    imprimir_error,
    imprimir_info,
    confirmar,
)
from views import (
    crear_estudiante,
    obtener_todos,
    obtener_por_id,
    buscar_estudiantes,
    actualizar_estudiante,
    eliminar_estudiante,
    agregar_nota,
    materias_ofertadas,
    estudiantes_en_comun,
)


def pausa():
    input("\nPresione Enter para continuar...")


def mostrar_tabla(estudiantes):
    print(f"{'ID':<5}{'NOMBRE':<25}{'EMAIL':<28}{'CARNET':<18}{'PROMEDIO':<10}")
    print("-" * 86)
    for estudiante in estudiantes:
        print(
            f"{estudiante.id:<5}"
            f"{estudiante.obtener_nombre_completo():<25}"
            f"{estudiante.email:<28}"
            f"{estudiante.carnet:<18}"
            f"{estudiante.obtener_promedio():<10}"
        )
    print("-" * 86)
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")


# ---------- C · CREAR ----------
def opcion_crear():
    imprimir_titulo("CREAR NUEVO ESTUDIANTE")
    datos = {}
    for campo in CAMPOS_ESTUDIANTE:
        datos[campo] = input(f"{campo.capitalize()}: ")

    exito, mensaje = crear_estudiante(datos)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


# ---------- R · LEER TODOS ----------
def opcion_ver_todos():
    imprimir_titulo("LISTA DE ESTUDIANTES")
    estudiantes = obtener_todos()
    if not estudiantes:
        imprimir_info("Todavía no hay estudiantes. Use la opción 1 para crear el primero.")
    else:
        mostrar_tabla(estudiantes)
    pausa()


# ---------- S · BUSCAR ----------
def opcion_buscar():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Nombre, email o carnet: ")
    encontrados = buscar_estudiantes(termino)

    if not encontrados:
        imprimir_info(f"Ningún estudiante coincide con '{termino}'.")
    else:
        mostrar_tabla(encontrados)
    pausa()


# ---------- R · LEER UNO ----------
def opcion_ver_por_id():
    imprimir_titulo("VER ESTUDIANTE POR ID")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    estudiante = obtener_por_id(id_estudiante)
    if not estudiante:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
    else:
        print(f"  ID         : {estudiante.id}")
        print(f"  Nombre     : {estudiante.obtener_nombre_completo()}")
        print(f"  Email      : {estudiante.email}")
        print(f"  Carnet     : {estudiante.carnet}")
        print(f"  Promedio   : {estudiante.obtener_promedio()}")
        print(f"  Materias   : {', '.join(sorted(estudiante.materias)) if estudiante.materias else 'Ninguna'}")
        print("  Notas:")
        if estudiante.notas:
            for materia, notas in estudiante.notas.items():
                print(f"    - {materia}: {notas}")
        else:
            print("    - Sin notas")
    pausa()


# ---------- U · ACTUALIZAR ----------
def opcion_actualizar():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    estudiante = obtener_por_id(id_estudiante)
    if not estudiante:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
        return pausa()

    imprimir_info(f"Editando a {estudiante.obtener_nombre_completo()}")
    print("Deje en blanco el campo que no quiera cambiar.\n")

    cambios = {}
    for campo in CAMPOS_ESTUDIANTE:
        actual = getattr(estudiante, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    exito, mensaje = actualizar_estudiante(id_estudiante, cambios)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


# ---------- D · ELIMINAR ----------
def opcion_eliminar():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    estudiante = obtener_por_id(id_estudiante)
    if not estudiante:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
        return pausa()

    imprimir_info(f"Se eliminará: {estudiante}")
    if confirmar("¿Confirma la eliminación?"):
        exito, mensaje = eliminar_estudiante(id_estudiante)
        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)
    else:
        imprimir_info("Operación cancelada")
    pausa()


# ---------- EXTRA · AGREGAR NOTA ----------
def opcion_agregar_nota():
    imprimir_titulo("AGREGAR NOTA")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    materia = input("Materia: ").strip()
    nota = input("Nota (0-20): ").strip()

    exito, mensaje = agregar_nota(id_estudiante, materia, nota)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


# ---------- EXTRA · VER PROMEDIO ----------
def opcion_ver_promedio():
    imprimir_titulo("VER PROMEDIO")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    estudiante = obtener_por_id(id_estudiante)
    if not estudiante:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
    else:
        print(f"Estudiante: {estudiante.obtener_nombre_completo()}")
        print(f"Promedio general: {estudiante.obtener_promedio()}")
    pausa()


# ---------- EXTRA · MATERIAS OFERTADAS ----------
def opcion_materias_ofertadas():
    imprimir_titulo("MATERIAS OFERTADAS")
    materias = materias_ofertadas()
    if not materias:
        imprimir_info("Todavía no hay materias registradas.")
    else:
        print("Materias registradas sin repetir:")
        for materia in sorted(materias):
            print(f"  - {materia}")
    pausa()


# ---------- EXTRA · MATERIAS EN COMÚN ----------
def opcion_materias_comun():
    imprimir_titulo("MATERIAS EN COMÚN")
    try:
        id_a = int(input("Id del primer estudiante: "))
        id_b = int(input("Id del segundo estudiante: "))
    except ValueError:
        imprimir_error("Los ids deben ser números enteros")
        return pausa()

    comunes, error = estudiantes_en_comun(id_a, id_b)
    if error:
        imprimir_error(error)
    elif comunes:
        print("Materias que ambos comparten:")
        for materia in sorted(comunes):
            print(f"  - {materia}")
    else:
        imprimir_info("Los estudiantes no tienen materias en común.")
    pausa()


def salir():
    imprimir_info("¡Hasta luego! 👋")
    return "salir"


# DICCIONARIO: tecla -> texto y función. Evita un if/elif largo.
OPCIONES = {
    "1": ("Crear estudiante", opcion_crear),
    "2": ("Ver todos", opcion_ver_todos),
    "3": ("Buscar", opcion_buscar),
    "4": ("Ver por id", opcion_ver_por_id),
    "5": ("Actualizar", opcion_actualizar),
    "6": ("Eliminar", opcion_eliminar),
    "7": ("Agregar nota", opcion_agregar_nota),
    "8": ("Ver promedio", opcion_ver_promedio),
    "9": ("Materias ofertadas", opcion_materias_ofertadas),
    "10": ("Materias en común", opcion_materias_comun),
    "0": ("Salir", salir),
}


def mostrar_menu():
    imprimir_titulo("SISTEMA DE GESTIÓN DE ESTUDIANTES")
    for tecla, (texto, _funcion) in OPCIONES.items():
        print(f"  {tecla}. {texto}")
    print()


def main():
    while True:
        mostrar_menu()
        tecla = input("Seleccione una opción: ").strip()

        if tecla not in OPCIONES:
            imprimir_error("Opción no válida")
            pausa()
            continue

        _texto, funcion = OPCIONES[tecla]
        if funcion() == "salir":
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
