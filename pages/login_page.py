"""Page Object de la pantalla de inicio de sesión de ShopGo (Parte 3)."""

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TIMEOUT_SEGUNDOS = 10


class LoginPage:
    # Locators: cómo Appium encuentra cada elemento (accessibility id).
    EMAIL_INPUT = (AppiumBy.ACCESSIBILITY_ID, "input_email")
    PASSWORD_INPUT = (AppiumBy.ACCESSIBILITY_ID, "input_password")
    LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "btn_login")
    ERROR_MESSAGE = (AppiumBy.ACCESSIBILITY_ID, "txt_error")
    # El título pertenece a la pantalla principal. Se deja aquí porque la prueba pide un solo
    # Page Object; en un proyecto real iría en un HomePage.
    HOME_TITLE = (AppiumBy.ACCESSIBILITY_ID, "home_title")

    def __init__(self, driver, timeout: int = TIMEOUT_SEGUNDOS):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)  # espera explícita, nunca time.sleep

    # --- Acciones -----------------------------------------------------------

    def ingresar_correo(self, correo: str) -> None:
        campo = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        campo.clear()
        campo.send_keys(correo)

    def ingresar_password(self, password: str) -> None:
        campo = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        campo.clear()
        campo.send_keys(password)

    def tocar_iniciar_sesion(self) -> None:
        # En mobile el teclado puede tapar el botón: se oculta antes de tocarlo.
        if self.driver.is_keyboard_shown():
            self.driver.hide_keyboard()
        boton = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        boton.click()

    def iniciar_sesion(self, correo: str, password: str) -> None:
        """Flujo completo: escribir correo y contraseña, y tocar "Iniciar sesión"."""
        self.ingresar_correo(correo)
        self.ingresar_password(password)
        self.tocar_iniciar_sesion()

    # --- Lecturas para las aserciones ----------------------------------------

    def obtener_titulo_bienvenida(self) -> str:
        titulo = self.wait.until(EC.visibility_of_element_located(self.HOME_TITLE))
        return titulo.text

    def obtener_mensaje_error(self) -> str:
        mensaje = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
        return mensaje.text

    def esta_en_pantalla_de_login(self) -> bool:
        return self.wait.until(EC.visibility_of_element_located(self.LOGIN_BUTTON)).is_displayed()
