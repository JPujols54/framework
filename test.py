import secrets

def generar_session_id(bytes_entropia: int = 32) -> str:
    """Genera un session_id aleatorio de alta entropía.

    32 bytes de entropía generan una cadena hexadecimal de 64 caracteres.
    """
    return secrets.token_hex(bytes_entropia)

hash = generar_session_id()
print(hash)