package com.cinebuscador.config;

// Importamos la forma de asegurar que los test generan los resultados esperados: la palabra clave assert.
// En este caso, verificamos que dos objetos no sean iguales, y que un resultado sea verdadero o falso.
// También podemos importar toda la biblioteca de Assertions.
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

// Nos permite definir los test que se deben ejecutar.
import org.junit.jupiter.api.Test;

public class EncryptionServiceTest {

    // Este test evalúa que el método que hashea contraseñas genere diferentes hash para el mismo texto plano.
    // Esto sucede porque la función de hash utilizado usa salt, aumentando la entropía del resultado.
    @Test 
    void passwordEncoderShouldCreateDifferentHashes() {
        // Definimos una contraseña.
        String testPassword = "SoyUnaContraseña";

        // La hasheamos dos veces.
        String firstHash = EncryptionService.encode(testPassword);
        String secondHash = EncryptionService.encode(testPassword);

        // Verificamos que el hash no sea el mismo.
        assertNotEquals(firstHash, secondHash);
    }


    // Este test evalúa que el método de comparar contraseñas con su hash funcione.
    @Test
    void passwordMatches() {
        // Definimos una contraseña.
        String testPassword = "SoyUnaConstraseñaTambién!";

        // Generamos el hash de esta contraseña.
        String hashedTestPassword = EncryptionService.encode(testPassword);

        // Comparamos el texto plano con el hash generado.
        boolean matches = EncryptionService.matches(testPassword, hashedTestPassword);
        
        // Verificamos que el resultado sea verdadero.
        assertTrue(matches);
    }

    // Este test evalúa que se reconozca de forma correcta dos contraseñas distintads.
    @Test
    void passwordDoesNotMatch() {
        // Definimos dos contraseñas distintas.
        String testPasswordOne = "SoyUnaConstraseñaTambién";
        String testPasswordTwo = "SoyLaContraseñaIncorrecta";

        // Generamos el hash de una contraseña.
        String hashedTestPasswordOne = EncryptionService.encode(testPasswordOne);

        // Comparamos dos contraseñas distintas: una en texto plano y otra como hash.
        boolean matches = EncryptionService.matches(testPasswordTwo, hashedTestPasswordOne);
        
        // Verificamos que efectivamente sean distintas.
        assertFalse(matches);
    }
}
