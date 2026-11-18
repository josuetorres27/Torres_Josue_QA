# Torres_Josue_QA

Solución a la prueba técnica de QA Automation Mobile para la app ficticia **ShopGo**.

## Contenido

| Parte | Archivo(s) |
|---|---|
| 1. Casos de prueba del inicio de sesión | [`parte1_casos/casos_login.md`](parte1_casos/casos_login.md) |
| 2. Validaciones y pruebas con pytest | [`shopgo/validaciones.py`](shopgo/validaciones.py), [`tests/test_validaciones.py`](tests/test_validaciones.py) |
| 3. Script de UI mobile (Appium + Page Object) | [`pages/login_page.py`](pages/login_page.py), [`tests/conftest.py`](tests/conftest.py), [`tests/test_login.py`](tests/test_login.py) |
| 4. Reporte de bug | [`parte4_bug/reporte_bug.md`](parte4_bug/reporte_bug.md) |
| Suposiciones, uso de IA y tiempo invertido | [`NOTAS.md`](NOTAS.md) |

```
Torres_Josue_QA/
├── README.md
├── NOTAS.md
├── requirements.txt
├── pytest.ini                  # pythonpath = . y marker "ui"
├── parte1_casos/casos_login.md
├── shopgo/                     # Parte 2
├── pages/                      # Parte 3: Page Object
├── tests/                      # Partes 2 y 3
└── parte4_bug/reporte_bug.md
```

## Requisitos

- Python 3.10 o superior.
- No hace falta Appium Server ni un emulador para las pruebas de la Parte 2.

## 1. Crear el entorno virtual

Linux, macOS o WSL:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

## 2. Instalar las dependencias

```bash
pip install -r requirements.txt
```

## 3. Ejecutar las pruebas

Pruebas de la Parte 2:

```bash
pytest tests/test_validaciones.py
```

Con `-v` se ve el nombre de cada caso, por ejemplo: `test_validar_password_respeta_limites_de_longitud[21_caracteres_invalida]`.

Todas las pruebas:

```bash
pytest
```

Resultado esperado sin servidor Appium: **38 pruebas pasadas y 2 omitidas** (skipped). Las 2 omitidas
son las de UI de la Parte 3, que se saltan solas cuando no hay un servidor Appium disponible.

Para excluir las pruebas de UI de forma explícita:

```bash
pytest -m "not ui"
```

## Pruebas de UI (Parte 3) contra un dispositivo real

La prueba no pide ejecutarlas. Si se quisiera, hace falta un servidor Appium 2 con el driver UiAutomator2 (`appium driver install uiautomator2`) y un emulador o dispositivo Android conectado. Después se indica el APK de ShopGo y, si no es la URL por defecto (`http://127.0.0.1:4723`), la del servidor:

```bash
export SHOPGO_APK=/ruta/a/shopgo.apk
export APPIUM_SERVER_URL=http://127.0.0.1:4723
pytest -m ui -v
```

En PowerShell: `$env:SHOPGO_APK = "C:\ruta\a\shopgo.apk"`.
