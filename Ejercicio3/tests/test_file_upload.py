'''
Para ejecutar el test debemos tener corriendo el contenedor de docker de la aplicación del ejercicio 3.

Parados en el directorio Ejercicio3:

    En una terminal ejecutar:
    docker compose up --build 

    En otra terminal ejecutar:
    python -m pytest tests -v
'''

# Importamos uuid para generar identificadores únicos para los nombres de los archivos de prueba.
import uuid

# Importamos Path para construir rutas y comprobar si existen archivos.
from pathlib import Path

# Importamos requests para enviar peticiones HTTP al servidor.
import requests

# Método que sube un archivo al servidor.
def upload_file(name, content, mime_type):
    # Enviamos una petición POST al endpoint encargado de recibir los afiches.
    return requests.post(
        "http://localhost:8080/upload/1",
        files={ "afiche": (name, content, mime_type) },
        # Evitamos seguir automáticamente las redirecciones para poder comprobar la respuesta original del servidor.
        allow_redirects=False,
        timeout=10
    )

# Test que evalúa si el servidor permite subir archivos con extensiones relacionadas con las imágenes.
# Este test va a pasar en ambas ramas.
def test_img_extensions_allowed():
    # Construimos la ruta de la imagen de prueba a partir de la ubicación de este archivo de tests.
    TEST_IMAGE = Path(__file__).resolve().parent / "archivos" / "Afiche.jpg"

    # Comprobamos que el archivo de imagen necesario para la prueba exista.
    assert TEST_IMAGE.exists(), (
        f"No se encontró la imagen de prueba."
    )

    # Leemos el contenido binario de la imagen para enviarlo al servidor.
    content = TEST_IMAGE.read_bytes()

    # Recorremos las extensiones de imagen que se consideran permitidas.
    for extension in [".jpg", ".png", ".jpeg"]:
        # Generamos un nombre de archivo único para evitar conflictos con las demás pruebas.
        name = f"prueba_{uuid.uuid4().hex[:8]}{extension}"

        # Enviamos el archivo al servidor y guardamos la respuesta.
        reply = upload_file(name, content, "image/jpeg")

        # Comprobamos que el servidor acepte el archivo y responda con una redirección HTTP 302.
        assert reply.status_code == 302, (
            f"Se rechazó la extensión permitida {extension}. "
            f"HTTP recibido: {reply.status_code}"
        )

# Test que evalúa que el servidor rechace archivos con extensiones no correspondientes a imágenes.
def test_non_img_extension_not_allowed():
    # Recorremos una serie de extensiones no permitidas para probar cada una.
    for extension in [ ".txt", ".pdf", ".exe", ".cmd", ".sh", ".php", ".js", ".py", ".java", ".class", ".jar", ".html", ".xml", ".zip", ".json"]:
        name = f"prueba_{uuid.uuid4().hex[:8]}{extension}"

        # Creamos un contenido de prueba que no corresponde a una imagen.
        content = b"archivo de prueba"

        # Enviamos el archivo al servidor para comprobar si rechaza la extensión.
        respuesta = upload_file(name, content, "application/octet-stream")

        # Comprobamos que el servidor devuelva un código HTTP de error (400 o superior).
        assert respuesta.status_code >= 400, (
            f"El servidor aceptó una extensión no permitida: {extension}. "
            f"HTTP recibido: {respuesta.status_code}"
        )

# Test que evalúa si el servidor rechaza contenido que no sea una imagen, aunque el archivo tenga una extensión permitida.
def test_non_img_content_not_allowed():
    # Creamos contenido de prueba que no corresponde a una imagen.
    content = b"Esto es codigo malicioso"

    # Recorremos aquellas extensiones permitidas.
    for extension in [".jpg", ".png", ".jpeg"]:
        name = f"prueba_{uuid.uuid4().hex[:8]}{extension}"

        # Subimos el archivo y guardamos la respuesta.
        reply = upload_file(name, content, "image/jpeg")

        # Comprobamos que el servidor devuelva un código HTTP de error (400 o superior).
        assert reply.status_code >= 400, (
            f"El servidor aceptó un archivo con extensión .jpg pero contenido falso. "
            f"HTTP recibido: {reply.status_code}"
        )