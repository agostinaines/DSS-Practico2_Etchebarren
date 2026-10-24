'''
Para ejecutar el test debemos tener corriendo el contenedor de docker de la aplicación del ejercicio 4.

Parados en el directorio Ejercicio4:

    En una terminal ejecutar:
    docker compose up --build 

    En otra terminal ejecutar:
    python -m pytest tests -v
'''

# Importamos requests para enviar peticiones HTTP al servidor.
import requests

# Método que sube un archivo al servidor.
def search_function(busqueda):
    # Enviamos una petición GET al endpoint principal, pasando la búsqueda como parámetro.
    return requests.get(
        "http://localhost:8080/",
        params={"buscar": busqueda},

        # Establecemos un tiempo máximo de espera de 10 segundos para la petición.
        timeout=10
    )

# Este test verifica que una expresión SpEL no se evalúe como código al introducirla en la búsqueda.
def test_spel_expression_not_executed():
    # Creamos una expresión que, si se evaluara mediante SpEL, devolvería el valor de PI.
    attack = "T(java.lang.Math).PI"

    # Enviamos la expresión como parámetro de búsqueda al servidor y guardamos la respuesta.
    reply = search_function(attack)

    # Comprobamos que el servidor procese la petición sin producir un error HTTP.
    assert reply.status_code == 200, (
        f"El servidor no procesó correctamente la búsqueda. "
        f"HTTP recibido: {reply.status_code}"
    )

    # Comprobamos que el resultado de evaluar la expresión no aparezca en la respuesta.
    assert "3.141592653589793" not in reply.text, (
        "La aplicación parece haber evaluado la expresión SpEL "
        "en lugar de tratarla como un texto de búsqueda."
    )

# Este test verifica que una expresión que intenta realizar operaciones no se ejecute como tal.
def test_expressions_with_spel_are_not_executed():
    # Este ataque simplemente hace que una palabra pase de minúscula a mayúscula, se pueden hacer cosas más peligrosas que eso.
    # Para este ejemplo, si se encuentra la mayúscula en la respuesta del servidor, el evaluador de expresiones SPEL está funcionando cuando no debería.
    attack = "'expression'.toUpperCase()"
    result = "EXPRESSION"

    # Enviamos la expresión como parámetro de búsqueda al servidor y guardamos la respuesta.
    reply = search_function(attack)

    # Comprobamos que el servidor procese la petición sin producir un error HTTP.
    assert reply.status_code == 200, (
        f"El servidor no procesó correctamente la búsqueda. "
        f"HTTP recibido: {reply.status_code}"
    )

    # Verificamos que la expresión no aparezca en la respuesta del servidor.
    assert result not in reply.text