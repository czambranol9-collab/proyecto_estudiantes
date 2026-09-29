from models import Estudiante, CAMPOS_ESTUDIANTE
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

# CONTROLADOR: aquí están las reglas y operaciones. No hay print() ni input().
gestor = GestorJSON("data/estudiantes.json")

# TUPLAS: configuración fija para validar y buscar.
CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")


def emails_registrados(excepto_id=None):
    """CONJUNTO con los emails usados para detectar duplicados."""
    return {
        registro["email"].lower()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


def carnets_registrados(excepto_id=None):
    """CONJUNTO con los carnets usados para impedir duplicados."""
    return {
        registro["carnet"].lower()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


def siguiente_id():
    ids = [registro["id"] for registro in gestor.leer()]
    return max(ids) + 1 if ids else 1


# ===================== C · CREATE =====================
def crear_estudiante(datos):
    try:
        valores = {
            campo: str(datos.get(campo, "")).strip()
            for campo in CAMPOS_ESTUDIANTE
        }

        faltantes = [campo for campo in CAMPOS_OBLIGATORIOS if not valores[campo]]
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        if not es_email_valido(valores["email"]):
            return False, f"El email '{valores['email']}' no tiene un formato válido"

        if valores["email"].lower() in emails_registrados():
            return False, "Ese email ya está registrado"

        if valores["carnet"].lower() in carnets_registrados():
            return False, "Ese carnet ya está registrado"

        estudiante = Estudiante(siguiente_id(), **valores)

        registros = gestor.leer()
        registros.append(estudiante.a_diccionario())

        if not gestor.guardar(registros):
            return False, "No se pudo escribir el archivo"

        return True, f"Estudiante {estudiante.obtener_nombre_completo()} creado con id {estudiante.id}"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== R · READ =====================
def obtener_todos():
    return [Estudiante.desde_diccionario(registro) for registro in gestor.leer()]


def obtener_por_id(id_estudiante):
    for estudiante in obtener_todos():
        if estudiante.id == id_estudiante:
            return estudiante
    return None


# ===================== S · SEARCH =====================
def buscar_estudiantes(termino):
    """Búsqueda lineal revisando los campos buscables."""
    termino = termino.strip().lower()
    if not termino:
        return []

    encontrados = []
    for registro in gestor.leer():
        for campo in CAMPOS_BUSCABLES:
            if termino in str(registro.get(campo, "")).lower():
                encontrados.append(Estudiante.desde_diccionario(registro))
                break
    return encontrados


# ===================== U · UPDATE =====================
def actualizar_estudiante(id_estudiante, cambios):
    try:
        desconocidos = set(cambios) - set(CAMPOS_ESTUDIANTE)
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        if not cambios:
            return False, "No se indicó ningún cambio"

        cambios = {campo: str(valor).strip() for campo, valor in cambios.items()}

        if "email" in cambios:
            if not es_email_valido(cambios["email"]):
                return False, "El email no tiene un formato válido"
            if cambios["email"].lower() in emails_registrados(excepto_id=id_estudiante):
                return False, "Ese email ya lo usa otro estudiante"

        if "carnet" in cambios:
            if not cambios["carnet"]:
                return False, "El carnet no puede quedar vacío"
            if cambios["carnet"].lower() in carnets_registrados(excepto_id=id_estudiante):
                return False, "Ese carnet ya lo usa otro estudiante"

        registros = gestor.leer()
        posicion = None

        for indice, registro in enumerate(registros):
            if registro["id"] == id_estudiante:
                posicion = indice
                break

        if posicion is None:
            return False, f"No existe un estudiante con id {id_estudiante}"

        registros[posicion].update(cambios)

        if not gestor.guardar(registros):
            return False, "No se pudo guardar la actualización"

        return True, f"Estudiante {id_estudiante} actualizado ({len(cambios)} campo/s)"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== D · DELETE =====================
def eliminar_estudiante(id_estudiante):
    registros = gestor.leer()

    # LISTA NUEVA sin el registro: no se elimina mientras se recorre la lista.
    quedan = [registro for registro in registros if registro["id"] != id_estudiante]

    if len(quedan) == len(registros):
        return False, f"No existe un estudiante con id {id_estudiante}"

    if not gestor.guardar(quedan):
        return False, "No se pudo guardar la eliminación"

    return True, f"Estudiante {id_estudiante} eliminado"


# ===================== EXTRA · NOTAS =====================
def agregar_nota(id_estudiante, materia, nota):
    """Agrega una nota entre 0 y 20 y guarda los cambios."""
    estudiante = obtener_por_id(id_estudiante)
    if not estudiante:
        return False, f"No existe un estudiante con id {id_estudiante}"

    materia = str(materia).strip()
    if not materia:
        return False, "La materia es obligatoria"

    try:
        nota = float(nota)
    except (TypeError, ValueError):
        return False, "La nota debe ser un número entre 0 y 20"

    if not 0 <= nota <= 20:
        return False, "La nota debe estar entre 0 y 20"

    # Si es un entero, lo guardamos como entero para que el JSON sea más limpio.
    nota = int(nota) if nota.is_integer() else nota

    estudiante.agregar_nota(materia, nota)

    registros = gestor.leer()
    for indice, registro in enumerate(registros):
        if registro["id"] == id_estudiante:
            registros[indice] = estudiante.a_diccionario()
            break
    else:
        return False, f"No existe un estudiante con id {id_estudiante}"

    if not gestor.guardar(registros):
        return False, "No se pudo guardar la nota"

    return True, f"Nota {nota} agregada en {materia}"


# ===================== EXTRA · MATERIAS =====================
def materias_ofertadas():
    """SET con todas las materias de todos los estudiantes, sin repetidos."""
    materias = set()
    for estudiante in obtener_todos():
        materias.update(estudiante.materias)
    return materias


def estudiantes_en_comun(id_a, id_b):
    """INTERSECCIÓN de los sets de materias de dos estudiantes."""
    estudiante_a = obtener_por_id(id_a)
    estudiante_b = obtener_por_id(id_b)

    if not estudiante_a:
        return None, f"No existe un estudiante con id {id_a}"
    if not estudiante_b:
        return None, f"No existe un estudiante con id {id_b}"

    return estudiante_a.materias & estudiante_b.materias, None
