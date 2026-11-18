"""Fixtures compartidas. El fixture `driver` crea la sesión de Appium (Parte 3)."""

import os
import socket
from urllib.parse import urlparse

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

# Se pueden cambiar con variables de entorno sin tocar el código.
APPIUM_SERVER_URL = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")
SHOPGO_APK = os.getenv("SHOPGO_APK", "/ruta/a/shopgo.apk")  # ruta de ejemplo


def _appium_disponible(url: str) -> bool:
    """Revisa si hay un servidor escuchando en la URL de Appium."""
    destino = urlparse(url)
    try:
        with socket.create_connection((destino.hostname, destino.port or 4723), timeout=1):
            return True
    except OSError:
        return False


def _capabilities() -> UiAutomator2Options:
    """Capabilities de ejemplo: qué app abrir y en qué dispositivo Android."""
    options = UiAutomator2Options()  # ya define platformName=Android y automationName=UiAutomator2
    options.device_name = "emulator-5554"
    options.app = SHOPGO_APK
    # Cada prueba empieza con la app limpia. Con no_reset=True la sesión de la prueba anterior
    # podría seguir abierta y la siguiente prueba no vería la pantalla de login.
    options.no_reset = False
    return options


@pytest.fixture
def driver():
    if not _appium_disponible(APPIUM_SERVER_URL):
        pytest.skip(f"No hay servidor Appium en {APPIUM_SERVER_URL}; se omiten las pruebas de UI.")

    drv = webdriver.Remote(APPIUM_SERVER_URL, options=_capabilities())
    yield drv  # la prueba usa el driver
    drv.quit()  # se cierra la sesión aunque la prueba falle
