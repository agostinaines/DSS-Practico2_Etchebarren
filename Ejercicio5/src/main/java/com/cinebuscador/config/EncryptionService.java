package com.cinebuscador.config;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

public class EncryptionService {
    private static final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    // Genera un hash para una contraseña
    public static String encode(String plainPassword) {
        return passwordEncoder.encode(plainPassword);
    }

    // Compara el hash de la contraseña original con la contraseña ingresada a la hora de iniciar sesión
    public static boolean matches(String plainPassword, String hashedPassword) {
        return passwordEncoder.matches(plainPassword, hashedPassword);
    }
}
