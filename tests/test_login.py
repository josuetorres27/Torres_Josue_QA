"""Pruebas de UI de la pantalla de inicio de sesión (Parte 3).

Requieren un servidor Appium y un dispositivo o emulador con ShopGo. Si no hay servidor,
se omiten (skip). Para excluirlas: pytest -m "not ui".
"""

import pytest

from pages.login_page import LoginPage

pytestmark = pytest.mark.ui

# Mismos datos que en parte1_casos/casos_login.md.
CORREO_REGISTRADO = "qa.user@shopgo.com"
PASSWORD_CORRECTA = "Clave1234"
# Tiene formato válido (mayúscula, número, 9 caracteres) pero no es la de la cuenta, así que
# se prueba el rechazo por credenciales y no una validación de formato (ver S-1 en NOTAS.md).
PASSWORD_INCORRECTA = "Clave9999"

TITULO_BIENVENIDA = "Bienvenido"
MENSAJE_CREDENCIALES_INCORRECTAS = "Correo o contraseña incorrectos"


def test_login_exitoso_muestra_titulo_bienvenido(driver):
    """TC-01: con credenciales válidas se abre la pantalla principal con 'Bienvenido'."""
    login = LoginPage(driver)

    login.iniciar_sesion(CORREO_REGISTRADO, PASSWORD_CORRECTA)

    assert login.obtener_titulo_bienvenida() == TITULO_BIENVENIDA


def test_login_con_password_incorrecta_muestra_mensaje_de_error(driver):
    """TC-03: con una contraseña incorrecta aparece el error y no se sale del login."""
    login = LoginPage(driver)

    login.iniciar_sesion(CORREO_REGISTRADO, PASSWORD_INCORRECTA)

    assert login.obtener_mensaje_error() == MENSAJE_CREDENCIALES_INCORRECTAS
    assert login.esta_en_pantalla_de_login()
