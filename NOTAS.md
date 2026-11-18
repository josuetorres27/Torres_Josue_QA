# NOTAS

## Entorno

- WSL (Ubuntu) en Windows 11.
- Python 3.15.2 y pytest 9.2.0. Appium-Python-Client 6.1.7.
- También verifiqué con Python 3.10.12 (la versión mínima que pide la prueba) siguiendo el README desde cero. Con ambas versiones pasan las 38 pruebas de la Parte 2, con cobertura del 100 % de `shopgo/validaciones.py`.

## Tiempo invertido

| Actividad | Tiempo |
|---|---|
| Lectura del enunciado y planificación | 20 min |
| Parte 1: casos de prueba | 30 min |
| Parte 2: validaciones y pruebas | 35 min |
| Parte 3: Page Object y pruebas de UI | 55 min |
| Parte 4: reporte de bug | 15 min |
| README, NOTAS, commits y entrega | 30 min |
| **Total** | **≈ 3 h 05 min** |

El trabajo se hizo en dos bloques el mismo día, separados por una clase. Tomó más que los 60 minutos
sugeridos por dos razones:
- No conocía el patrón de Appium (Page Object, fixture del driver y esperas explícitas), así que dediqué tiempo a entenderlo antes de escribir la Parte 3.
- Quería hacer un buen trabajo: revisar cada parte, definir y documentar las suposiciones, y verificar la instalación y las pruebas desde cero con Python 3.10 y 3.15.

## Suposiciones

Los casos y las pruebas que dependen de una suposición la indican: **(S-n)** en los casos de prueba y
`_Sn` al final del id en pytest.

### Parte 1: pantalla de inicio de sesión

- **S-1. Mensajes no definidos.** La especificación solo define "Correo o contraseña incorrectos" y "Bienvenido". Con un correo o una contraseña de formato inválido, o con la cuenta bloqueada, asumo que no se inicia sesión y aparece un mensaje de error. Como su texto no está definido, los casos verifican que no se inicia sesión y no citan un texto exacto.
- **S-2. Campos vacíos.** Si se toca "Iniciar sesión" con un campo vacío, aparece un mensaje en rojo debajo del campo o un toast que indica que hay que completarlo, y no se envía la solicitud.
- **S-3. Bloqueo.** Solo cuentan los intentos que se validan contra la cuenta (correo o contraseña incorrectos), no los de campos vacíos ni los hechos sin conexión. El bloqueo es por cuenta, los 5 minutos cuentan desde el tercer fallo, y un login exitoso reinicia el contador ("seguidos").
- **S-4. Sin conexión.** La app muestra un error de red distinto al de credenciales incorrectas y conserva los datos escritos.
- **S-5. Contraseña de más de 20 caracteres.** El campo permite escribirla y la app la rechaza. Si el campo limitara la entrada a 20, habría que verificar que no recorta en silencio una contraseña pegada.

### Parte 2: `validar_password` y `calcular_envio`

- **S-6.** `validar_password(None)` devuelve `False` en vez de lanzar una excepción.
- **S-7.** Cuenta como mayúscula cualquier letra mayúscula, incluidas `Ñ` y las tildes (`Á`), porque la app es para usuarios hispanohablantes. "Ningún espacio" incluye tabs y saltos de línea.
- **S-8.** Un subtotal de 0 paga envío (₡2 500) y los decimales se comparan tal cual: ₡24 999.99 paga envío. La función siempre devuelve `int`, y solo los negativos lanzan `ValueError`.

### Parte 3: script de UI

- **S-9.** El script no se ejecutó contra una app real, ya que la prueba no lo pide. Es para Android (UiAutomator2); la URL de Appium y la ruta del APK son de ejemplo y se cambian con variables de entorno. Las cuentas de prueba existen y no están bloqueadas al iniciar. Si no hay servidor Appium, las pruebas de UI se omiten en vez de fallar.

### Parte 4: reporte de bug

- **S-10.** El bug viene del reporte de un usuario y no se ha reproducido internamente. No inventé datos del entorno: lo que falta quedó como preguntas abiertas. El precio de ₡9 000 de la camisa es solo un ejemplo para mostrar el efecto en el costo de envío.

## Uso de herramientas de IA

Usé **Claude Code (Claude Opus 5.5)** en todas las partes. Mi forma de trabajo fue escribir primero mi
propio borrador de cada parte y después pedirle que lo revisara, hiciera observaciones y propusiera correcciones. También la usé para mejorar la redacción y el formato de los documentos y del código. Revisé todo el contenido final.

| Parte | Para qué la usé | Qué revisé o cambié yo |
|---|---|---|
| Planificación | Proponer un orden de trabajo y señalar las ambigüedades del enunciado | Decidí la forma de trabajo (mi borrador primero y luego la revisión), el nombre del repo y entregarlo como repo público con release y zip. |
| Parte 1 | Revisar los 10 casos iniciales que yo propuse; generó la versión final de 12 casos con valores límite y casos mobile | Revisé cada caso de la versión final y estoy de acuerdo con ellos. Definí el comportamiento con campos vacíos (S-2). |
| Parte 2 | Corregir los errores de mi código y generar las pruebas con `parametrize` | Corrí las pruebas en mi entorno y confirmé los resultados que indica el README. Decidí que la `Ñ` y las letras con tilde cuentan como mayúscula (S-7). |
| Parte 3 | Revisar mi Page Object, el fixture y las pruebas, y proponer ajustes | Revisé los ajustes y entendí por qué se usa `noReset=False`: para que cada prueba empiece desde la pantalla de login. |
| Parte 4 | Revisar el reporte del bug a partir de mi borrador | Escribí el borrador original; el reporte final es la versión definitiva sobre el bug del enunciado. |
| Entrega | Escribir el README, el `.gitignore` y estas notas a partir de lo que habíamos trabajado | Seguí el README y obtuve los resultados indicados. Realicé cambios en la redacción inicial y completé algunos faltantes. Decidí el formato de los commits y la forma de entregar la prueba. |
