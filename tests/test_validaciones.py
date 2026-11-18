"""Pruebas de la Parte 2: validar_password y calcular_envio."""

import pytest

from shopgo.validaciones import calcular_envio, validar_password


# ---------------------------------------------------------------------------
# validar_password: valores límite de longitud (8 a 20 caracteres)
# Cada contraseña cumple todas las demás reglas, así que solo la longitud decide.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    ("password", "largo", "esperado"),
    [
        ("Clave12", 7, False),
        ("Clave123", 8, True),
        ("Clave1234", 9, True),
        ("ClaveSegura12345678", 19, True),
        ("ClaveSegura123456789", 20, True),
        ("ClaveSegura1234567890", 21, False),
    ],
    ids=[
        "7_caracteres_invalida",
        "8_caracteres_limite_inferior_valida",
        "9_caracteres_valida",
        "19_caracteres_valida",
        "20_caracteres_limite_superior_valida",
        "21_caracteres_invalida",
    ],
)
def test_validar_password_respeta_limites_de_longitud(password, largo, esperado):
    # Protege la prueba de un dato mal contado: si el largo no es el que dice, la prueba no vale.
    assert len(password) == largo
    assert validar_password(password) is esperado


# ---------------------------------------------------------------------------
# validar_password: casos válidos variados
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "password",
    [
        "Clave1234",
        "CLAVE1234",
        "1234567A",
        "Cl@ve_1234!",
        "Ñandu12345",
    ],
    ids=[
        "mayuscula_inicial_y_numeros",
        "todo_mayusculas_y_numeros",
        "una_sola_mayuscula_al_final",
        "con_simbolos",
        "mayuscula_con_tilde_cuenta_S7",
    ],
)
def test_validar_password_acepta_contrasenas_que_cumplen_todas_las_reglas(password):
    assert validar_password(password) is True


# ---------------------------------------------------------------------------
# validar_password: casos negativos
# Cada contraseña incumple UNA sola regla (y tiene largo válido),
# para saber exactamente qué regla hace fallar la prueba.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "password",
    [
        "clave12345",
        "1234567890",
        "ClaveSegura",
        "Clave 1234",
        " Clave1234",
        "Clave1234 ",
        "Clave\t1234",
        "Clave\n1234",
    ],
    ids=[
        "sin_mayuscula",
        "solo_numeros_sin_mayuscula",
        "sin_numero",
        "espacio_en_medio",
        "espacio_al_inicio",
        "espacio_al_final",
        "tabulador_S7",
        "salto_de_linea_S7",
    ],
)
def test_validar_password_rechaza_contrasena_que_incumple_una_regla(password):
    assert validar_password(password) is False


@pytest.mark.parametrize(
    "password",
    ["", "        ", None],
    ids=["texto_vacio", "solo_espacios", "none_S6"],
)
def test_validar_password_rechaza_entradas_vacias_o_nulas(password):
    assert validar_password(password) is False


# ---------------------------------------------------------------------------
# calcular_envio: valores límite alrededor de ₡25 000
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    ("subtotal", "envio_esperado"),
    [
        (0, 2500),
        (0.01, 2500),
        (24_999, 2500),
        (24_999.99, 2500),
        (25_000, 0),
        (25_000.0, 0),
        (25_000.01, 0),
        (25_001, 0),
        (1_000_000, 0),
    ],
    ids=[
        "subtotal_0_paga_envio_S8",
        "subtotal_minimo_positivo_paga_envio",
        "24999_justo_debajo_del_umbral_paga_envio",
        "24999_99_decimal_debajo_del_umbral_paga_envio_S8",
        "25000_exacto_envio_gratis",
        "25000_como_float_envio_gratis",
        "25000_01_justo_encima_envio_gratis",
        "25001_envio_gratis",
        "subtotal_muy_alto_envio_gratis",
    ],
)
def test_calcular_envio_aplica_umbral_de_envio_gratis(subtotal, envio_esperado):
    assert calcular_envio(subtotal) == envio_esperado


@pytest.mark.parametrize(
    "subtotal",
    [0, 24_999.99, 25_000, 25_000.5],
    ids=["subtotal_0", "subtotal_float_bajo", "subtotal_umbral", "subtotal_float_alto"],
)
def test_calcular_envio_devuelve_un_entero(subtotal):
    # La firma promete -> int aunque el subtotal sea float.
    # Se usa type(...) is int porque isinstance(True, int) también sería True.
    assert type(calcular_envio(subtotal)) is int


# ---------------------------------------------------------------------------
# calcular_envio: subtotal negativo
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "subtotal",
    [-0.01, -1, -25_000],
    ids=["negativo_minimo", "menos_uno", "negativo_grande"],
)
def test_calcular_envio_con_subtotal_negativo_lanza_value_error(subtotal):
    with pytest.raises(ValueError):
        calcular_envio(subtotal)
