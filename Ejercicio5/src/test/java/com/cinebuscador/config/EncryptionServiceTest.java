/*
Para ejecutar este test podemos utilizar los triángulos o símbolos de Play al lado de cada test o en la clase en general.
*/

package com.cinebuscador.config;

import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNull;

// Nos permite definir los test que se deben ejecutar.
import org.junit.jupiter.api.Test;

public class EncryptionServiceTest {
    
    // Este test evalúa si dos contraseñas iguales generan el mismo texto encriptado.
    @Test 
    void passwordEncoderShouldCreateDifferentHashes() {
        // Definimos una contraseña.
        String testPassword = "SoyUnaContraseña";

        // La encriptamos dos veces.
        String firstEncrypt = EncryptionService.encrypt(testPassword);
        String secondEncrypt = EncryptionService.encrypt(testPassword);

        // Verificamos que la encriptación no sea la misma.
        // Esto no es verdad por lo que el test falla.
        assertNotEquals(firstEncrypt, secondEncrypt);
    }

    // Los siguientes test muestran que el servicio devuelve información sobre la clave utilizada para encriptar contraseñas.
    @Test
    void serviceShouldNotGetSecretKey() {
        String key = EncryptionService.getStaticKey();

        assertNull(key);
    }

    @Test 
    void serviceShouldNotGetKeyBytes() {
        byte[] bytes = EncryptionService.getKeyBytes();

        assertNull(bytes);
    }

    @Test 
    void serviceShouldNotGetKeyHex() {
        String keyHex = EncryptionService.getKeyHex();

        assertNull(keyHex);
    }
}
