'''
El test se ejecuta de la siguiente manera, dentro del directorio Ejercicio1:
python -m pytest tests -v
'''

#Importamos la biblioteca de SQLite para crear una base de datos temporal sobre la cual efectuar tests.
import sqlite3

#Importamos el framework de testeo.
import pytest

# Importamos la aplicación para poder acceder a su contexto más adelante, la función que queremos evaluar y el método para conseguir una conexión a la base de datos.
from app import app, buscar_funciones, get_db

# El decorador define que este método es un 'Fixture'.
# Esto significa que prepara recursos o datos que precisa el test. 
@pytest.fixture
def test_db(tmp_path):

    # El fixture tmp_path provee un directorio único y temporal para cada método de un test.
    # En este caso creamos el path hacia ese nuevo directorio temporal.
    # Más adelante creamos el archivo como tal.
    # https://docs.pytest.org/en/stable/how-to/tmp_path.html
    db_path = tmp_path / "test.db"

    # Este método establece una conexión al abrir un archivo de base de datos.
    # En este caso, al no existir el archivo, el método lo crea.
    # https://www.geeksforgeeks.org/python/python-sqlite-connecting-to-database/
    db = sqlite3.connect(db_path)

    # Usamos el método executeScript para poder ejecutar varios comandos, en este caso crear y rellenar la base de datos.
    # Creamos las tablas y colocamos información solo de aquello que vayamos a utilizar.
    # https://www.geeksforgeeks.org/python/how-to-execute-many-sqlite-statements-in-python/
    db.executescript("""
        CREATE TABLE peliculas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            genero TEXT NOT NULL,
            director TEXT NOT NULL
        );
        
        CREATE TABLE funciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pelicula_id INTEGER NOT NULL,
            fecha_hora TEXT NOT NULL,
            asientos_totales INTEGER NOT NULL DEFAULT 100,
            asientos_ocupados INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (pelicula_id) REFERENCES peliculas(id)
        );

        INSERT INTO peliculas (nombre, genero, director) VALUES
            ('Dune: Parte Dos', 'Ciencia Ficción', 'Denis Villeneuve'),
            ('Oppenheimer', 'Drama/Biografía', 'Christopher Nolan');

        INSERT INTO funciones
            (pelicula_id, fecha_hora, asientos_totales, asientos_ocupados)
        VALUES
            (1, '2026-07-13 14:30:00', 120, 85),
            (1, '2026-07-14 18:00:00', 120, 60);
    """)

    # Guarda los cambios hechos en la base de datos.
    db.commit()

    # Cierra la conexión con la base de datos.
    db.close()

    # Guardamos la configuración original de la conexión a la base de datos de nuestra aplicación.
    # Esto nos permite restituirla más adelante una vez haya terminado el test.
    # De querer hacer más tests, esto evita que las configuraciones afecten en algo más adelante.
    original_database = app.config["DATABASE"]

    # Hacemos que Flask use la nueva base de datos temporal.
    app.config["DATABASE"] = str(db_path)

    # Creamos el contexto de la aplicación para poder acceder al objeto g de Flask.
    # Este objeto se utiliza para hacer que ciertos datos y recursos puedan ser accedidos de forma global por varias funciones.
    # Esto nos permite guardar y acceder a la conexión con nuestra base de datos, por ejemplo.
    # https://testdriven.io/blog/flask-contexts/
    # https://www.geeksforgeeks.org/python/when-should-flask-g-be-used/
    with app.app_context():
        # Era importante utilizar el contexto de la aplicación porque el método get_db() utiliza el objeto g.
        # La palabra clave yield provee la conexión con la base de datos.
        # Inmediatamente luego de yield se da lo que se conoce como la fase de preparación (set-up phase)
        yield get_db()

        # Aquí la ejecución sigue dentro del test como tal.
        # Luego de esto, volvemos la ejecución dentro del fixture y se da la fase de limpieza (clean-up phase)
        # Cerramos la conexión con la base de datos utilizado en el test.
        get_db().close()

        # Volvemos la configuración a su versión original.
        app.config["DATABASE"] = original_database

# pytest lo puede identificar porque el nombre de la función empieza con 'test_'.
# https://docs.pytest.org/en/stable/explanation/goodpractices.html#test-discovery
# Recibe como parámetro el fixture definido anteriormente, de modo que se ejecuta automáticamente antes del test.
# https://docs.pytest.org/en/stable/how-to/fixtures.html
def test_injection(test_db):

    # Invoca el método a evaluar con un payload malicioso.
    query_result = buscar_funciones(
        query="' OR 1=1 --",
        sort_by="nombre",
        sort_dir="ASC"
    )

    # Verifica que el resultado no tiene filas.
    # Si se devuelven filas, este test fallará.
    assert len(query_result) == 0
