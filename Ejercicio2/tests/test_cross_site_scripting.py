'''
El test se ejecuta de la siguiente manera, dentro del directorio Ejercicio2:
python -m pytest tests -v
'''

# Importamos la aplicación para acceder a sus plantillas y a funcionalidades de Flask.
import app as repo

# Este test evalúa que un script introducido en la descripción no se interprete como código JavaScript.
def test_script_does_not_execute():
    template = repo.app.jinja_env.get_template("edit.html")

    # Creamos una entrada que intente inyectar código JavaScript mediante una etiqueta script.
    attack = "<script>alert('Ha ocurrido un error, debe volver a iniciar sesión para resolverlo');</script>"

    movie = {
        "nombre": "Titanic",
        "genero": "Drama/Romance",
        "director": "James Cameron",
        "descripcion": attack
    }

    # Generamos el HTML de la plantilla con los datos de la película.
    html = template.render(pelicula=movie)

    # Comprobamos que el ataque no aparezca como una etiqueta ejecutable.
    assert attack not in html

    # Verificamos que la etiqueta script se haya convertido en texto plano.
    # Codificamos los símbolos: < = &lt; y > = &gt;.
    assert "&lt;script&gt;" in html


# Este test evalúa que que el contenido malicioso tampoco se interprete como una etiqueta HTML al momento de mostrar la descripción.
def test_descripcion_no_inyecta_etiquetas_html():
    template = repo.app.jinja_env.get_template("edit.html")

    # Creamos una entrada que intente inyectar una imagen con un evento onerror que se ejecutaría como código JavaScript.
    attack = "<img src=x onerror=alert('Ha ocurrido un error, debe volver a iniciar sesión para resolverlo');>"

    movie = {
        "nombre": "Titanic",
        "genero": "Drama/Romance",
        "director": "James Cameron",
        "descripcion": attack
    }

    html = template.render(pelicula=movie)

    # Comprobamos que el ataque no aparezca como una etiqueta ejecutable.
    assert attack not in html

    # Verificamos que la etiqueta img se haya convertido en texto plano.
    # Codificamos el símbolo: < = &lt;.
    assert "&lt;img" in html

    # Comprobamos que las comillas se hayan convertido en entidades HTML.
    # Codificamos el las comillas: ' = &#39;.
    assert "onerror=alert(&#39;Ha ocurrido un error, debe volver a iniciar sesión para resolverlo&#39;);" in html
