/*
Para ejecutar este test podemos utilizar los triángulos o símbolos de Play al lado de cada test o en la clase en general.
*/

package com.cinebuscador.controller;

// Importamos el servicio de contraseñas.
import com.cinebuscador.config.EncryptionService;

// Importamos la entidad que represeta un usuario en la aplicación.
import com.cinebuscador.model.User;

// Importamos el repositorio para buscar y almacenar usuarios.
import com.cinebuscador.repository.UserRepository;

// Importamos el decorador que identifica cada uno de los test.
import org.junit.jupiter.api.Test;

// Importamos la clase ArgumentCaptor que nos permite interceptar los argumentos de un Mock para realizar evaluaciones sobre ellos.
import org.mockito.ArgumentCaptor;

// Un Mock nos permite crear objetos falsos que simulan el comportamiento del objeto en cuestión.
import org.mockito.Mock;
import org.mockito.InjectMocks;

// Permite extender nuestra clase de test con funcionalidades de Mockito
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;

// Representa el modelo utilizado para enviar información a la vista HTML.
import org.springframework.ui.Model;

// Representa un resultado opcional que puede ser vacío.
import java.util.Optional;

// Importamos las formas de verificar los resultados que esperamos: la palabra clave assert y todas sus variantes.
import static org.junit.jupiter.api.Assertions.*;

// Importamos Mockito para configurar y verificar el comportamiento de objetos Mock.
import static org.mockito.Mockito.*;

// Nos permite utilizar funcionalidades de Mockito dentro de la clase.
@ExtendWith(MockitoExtension.class)
class AuthControllerTest {

    // Creamos un objeto simulando UserRepository.
    // Esto significa que cualquier llamada a este objeto no se conectará realmente con una base de datos.
    @Mock
    private UserRepository userRepository;

    // Creamos un objeto simulando Model.
    // Esto nos permite verificar qué elementos han sido agregados a la vista.
    // No es necesario contar con un archivo HTML real ya que es una simulación.
    @Mock
    private Model model;

    // Creamos un objeto simulando el controlador e inyectamos los objetos Mock creados anteriormente que son necesarios dentro de la clase AuthController.
    @InjectMocks
    private AuthController authController;

    // Este test evalúa si se guarda efectivamente un nuevo usuario con una contraseña encriptada.
    @Test
    void registerShouldSaveUserWithEncryptedPassword() {
        // Definimos un usuario y una contraseña para el usuario.
        String username = "agos";
        String password = "SoyUnaContraseña:)";

        // Esto hace que cuando se llame al método register, no exista un usuario con nuestro mismo nombre, de modo que podemos registrarnos correctamente.
        when(userRepository.findByUsername(username))
            .thenReturn(Optional.empty());

        // Llamamos al método de registro, teniendo en cuenta que las contraseñas sean las mismas.
        // El método debería validar que sean iguales, generar el hash correspondiente, guardar el usuario e informar el éxito de la operación en el Modelo.
        String view = authController.register(
            username, password, password, model
        );

        // Verificamos que el método haya terminado éxitosamente.
        // Hacemos esto por medio de lo que devuelva el método register, si todo funcionó correctamente, este devuelve "index".
        assertEquals("index", view);

        // Creamos un ArgumentCaptor de tipo Usuario para almacenar el argumento interceptado más adelante.
        ArgumentCaptor<User> captor =
            ArgumentCaptor.forClass(User.class);

        // Verificamos que se haya llamado el método save, y que este haya guardado un argumento de tipo User.
        // https://www.digitalocean.com/community/tutorials/mockito-verify
        // https://www.baeldung.com/mockito-argumentcaptor
        verify(userRepository).save(captor.capture());

        // Conseguimos el usuario guardado en el repositorio.
        User savedUser = captor.getValue();

        // Verificamos que el usuario guardado y el usuario creado al principio es el mismo.
        assertEquals(username, savedUser.getUsername());

        // Verificamos que la contraseña no haya sido guardad en texto plano.
        assertNotEquals(password, savedUser.getPassword());

        // Verificamos que el hash guardado corresponda a la contraseña original.
        assertTrue(EncryptionService.matches(
            password, savedUser.getPassword()
        ));

        // Verificamos que se hayan agregado los atributos correspondientes en el modelo.
        verify(model).addAttribute("registerSuccess", true);
        verify(model).addAttribute("registeredUsername", username);
    }

    // Este test evalúa si el inicio de sesión es exitoso cuando se coloca la contraseña correcta.
    @Test
    void loginShouldSucceedWithCorrectPassword() {
        // Nuevamente creamos un usuario.
        String username = "agos";
        String password = "SoyUnaContraseña:)";

        User user = new User();
        user.setUsername(username);
        user.setPassword(EncryptionService.encode(password));

        // Cuando se llame al método findByUsername, dentro de AuthController por ejemplo, se devolverá el objeto User que preparamos anteriormente.
        when(userRepository.findByUsername(username))
            .thenReturn(Optional.of(user));

        // Invocamos el método de inicio de sesión con el usuario creado.
        String view = authController.login(username, password, model);

        // Verificamos que el método haya funcionado correctamente con la misma lógica de antes con el método register.
        assertEquals("index", view);

        // Verificamos que se hayan agregado los atributos correspondientes a la vista HTML.
        verify(model).addAttribute("loginSuccess", true);
        verify(model).addAttribute("welcomeUser", username);
        verify(model).addAttribute(
            "encryptedPassword", user.getPassword()
        );
    }

    // Este test evalúa que el inicio de sesión falle cuando la contraseña es incorrecta.
    @Test
    void loginShouldFailWithIncorrectPassword() {
        // Definimos un usuario y lo creamos.
        String username = "agos";

        User user = new User();
        user.setUsername(username);
        user.setPassword(
            EncryptionService.encode("ContraseñaCorrecta:)")
        );

        // Definimos que la llamada a findByUsername devuelva el usuario creado anteriormente.
        when(userRepository.findByUsername(username))
            .thenReturn(Optional.of(user));

        // Llamamos al método de iniciar sesión con una contraseña incorrecta.
        String view = authController.login(
            username, "ContraseñaIncorrecta:(", model
        );

        // Verificamos que todo haya funcionado.
        assertEquals("index", view);

        // Verificamos efectivamente que no se haya realizado el inicio de sesión y que se devuelva un mensaje de error en la vista HTML.
        verify(model).addAttribute(
            "loginError", "Usuario o contraseña incorrecta"
        );
    }
}
