"""Reglas de validación de ShopGo (Parte 2)."""

LARGO_MIN_PASSWORD = 8
LARGO_MAX_PASSWORD = 20
UMBRAL_ENVIO_GRATIS = 25_000
COSTO_ENVIO = 2_500


def validar_password(password: str) -> bool:
    """Devuelve True si la contraseña cumple las reglas de ShopGo.

    Reglas: entre 8 y 20 caracteres, al menos una mayúscula, al menos un número
    y ningún espacio. Cualquier valor que no sea un str (por ejemplo None) es inválido (S-6).
    """
    if not isinstance(password, str):
        return False
    if not LARGO_MIN_PASSWORD <= len(password) <= LARGO_MAX_PASSWORD:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    if any(c.isspace() for c in password):  # espacio, tab, salto de línea (S-7)
        return False
    return True


def calcular_envio(subtotal: float) -> int:
    """Devuelve el costo de envío en colones según el subtotal del carrito.

    0 si el subtotal es de ₡25 000 o más, 2500 si es menor.
    Lanza ValueError si el subtotal es negativo.
    """
    if subtotal < 0:
        raise ValueError(f"El subtotal no puede ser negativo: {subtotal}")
    if subtotal >= UMBRAL_ENVIO_GRATIS:
        return 0
    return COSTO_ENVIO
