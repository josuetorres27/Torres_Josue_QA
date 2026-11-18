# Parte 1 — Casos de prueba: inicio de sesión de ShopGo

Casos para la pantalla de inicio de sesión de ShopGo (Android e iOS). Las suposiciones de las que dependen
algunos resultados esperados están en `NOTAS.md` y se indican aquí como **(S-n)**.

## Datos de prueba

| Cuenta | Correo | Contraseña | Uso |
|---|---|---|---|
| Principal | `qa.user@shopgo.com` | `Clave1234` | Casos generales |
| Límite inferior | `limite8@shopgo.com` | `Clave123` (8 caracteres) | TC-06 |
| Límite superior | `limite20@shopgo.com` | `ClaveSegura123456789` (20 caracteres) | TC-06 |
| No registrado | `noexiste@shopgo.com` | — | TC-02 |

Todas las cuentas están registradas y activas, salvo la última. Antes de cada caso la cuenta no está
bloqueada y no tiene intentos fallidos previos.

## Casos

| ID | Título | Precondiciones | Pasos | Resultado esperado | Prioridad |
|---|---|---|---|---|---|
| TC-01 | [Positivo] Inicio de sesión con credenciales válidas | Usuario registrado (cuenta principal), app instalada, con conexión | 1. Abrir la app.<br>2. Ingresar `qa.user@shopgo.com` y `Clave1234`.<br>3. Tocar "Iniciar sesión". | Se abre la pantalla principal con el título "Bienvenido". | Alta |
| TC-02 | [Negativo] Correo con formato válido pero no registrado | App instalada, con conexión; `noexiste@shopgo.com` no está registrado | 1. Abrir la app.<br>2. Ingresar `noexiste@shopgo.com` y `Clave1234`.<br>3. Tocar "Iniciar sesión". | Aparece "Correo o contraseña incorrectos". No se abre la pantalla principal. El mensaje es el mismo que en TC-03, así que no revela si el correo existe. | Alta |
| TC-03 | [Negativo] Contraseña con formato válido pero incorrecta | Usuario registrado (cuenta principal), app instalada, con conexión | 1. Abrir la app.<br>2. Ingresar `qa.user@shopgo.com` y `Clave9999`.<br>3. Tocar "Iniciar sesión". | Aparece "Correo o contraseña incorrectos". No se abre la pantalla principal. | Alta |
| TC-04 | [Negativo] Correo con formato inválido | App instalada, con conexión | 1. Abrir la app.<br>2. Ingresar un correo inválido y `Clave1234`. Repetir con cada dato: `qa.usershopgo.com` (sin @), `qa.user@shopgo` (sin dominio), `@shopgo.com` (sin nombre), `qa user@shopgo.com` (con espacio).<br>3. Tocar "Iniciar sesión". | No se inicia sesión en ningún caso. Se muestra un mensaje de error **(S-1)**. | Media |
| TC-05 | [Negativo] Campos obligatorios vacíos | App instalada, con conexión | 1. Abrir la app.<br>2. Dejar vacío el correo e ingresar `Clave1234`; tocar "Iniciar sesión".<br>3. Ingresar `qa.user@shopgo.com`, dejar vacía la contraseña; tocar "Iniciar sesión".<br>4. Dejar ambos vacíos; tocar "Iniciar sesión". | No se inicia sesión en ningún caso. Aparece un mensaje en rojo debajo del campo vacío o un toast que indica que hay que completarlo **(S-2)**. No se cuenta como intento fallido **(S-3)**. | Media |
| TC-06 | [Límite] Contraseña de 8 y de 20 caracteres (límites válidos) | Cuentas "Límite inferior" y "Límite superior" registradas, app instalada, con conexión | 1. Abrir la app.<br>2. Ingresar `limite8@shopgo.com` y `Clave123`.<br>3. Tocar "Iniciar sesión".<br>4. Cerrar sesión y repetir con `limite20@shopgo.com` y `ClaveSegura123456789`. | En ambos intentos se abre la pantalla principal con el título "Bienvenido". | Alta |
| TC-07 | [Límite] Contraseña de 7 y de 21 caracteres (límites inválidos) | Usuario registrado (cuenta principal), app instalada, con conexión | 1. Abrir la app.<br>2. Ingresar `qa.user@shopgo.com` y `Clave12` (7 caracteres).<br>3. Tocar "Iniciar sesión".<br>4. Repetir con `ClaveSegura1234567890` (21 caracteres). | No se inicia sesión en ninguno de los dos intentos. Se muestra un mensaje de error **(S-1)**. El campo no recorta en silencio la contraseña de 21 caracteres a 20 **(S-5)**. | Alta |
| TC-08 | [Negativo] Contraseña que incumple las reglas de composición | Usuario registrado (cuenta principal), app instalada, con conexión | 1. Abrir la app.<br>2. Ingresar `qa.user@shopgo.com` y una contraseña inválida. Repetir con cada dato: `clave1234` (sin mayúscula), `ClaveSegura` (sin número), `Clave 1234` (con espacio).<br>3. Tocar "Iniciar sesión". | No se inicia sesión en ningún caso. Se muestra un mensaje de error **(S-1)**. | Media |
| TC-09 | [Regla de negocio] Bloqueo tras 3 intentos fallidos seguidos | Usuario registrado (cuenta principal), app instalada, con conexión | 1. Abrir la app.<br>2. Ingresar `qa.user@shopgo.com` y `Clave9999`; tocar "Iniciar sesión".<br>3. Repetir el paso 2 dos veces más (3 fallos seguidos).<br>4. Ingresar la contraseña correcta `Clave1234`; tocar "Iniciar sesión". | En los pasos 2 y 3 aparece "Correo o contraseña incorrectos". En el paso 4 **no** se inicia sesión aunque la contraseña sea correcta, porque la cuenta está bloqueada **(S-1)**. | Alta |
| TC-10 | [Límite / Regla de negocio] Desbloqueo después de 5 minutos | Cuenta principal bloqueada por TC-09; se anota la hora del tercer fallo | 1. A los 4 min 50 s del bloqueo, ingresar `qa.user@shopgo.com` y `Clave1234`; tocar "Iniciar sesión".<br>2. Pasados los 5 min, repetir el paso 1. | Paso 1: no se inicia sesión porque la cuenta sigue bloqueada. Paso 2: se abre la pantalla principal con el título "Bienvenido" **(S-3)**. | Media |
| TC-11 | [Mobile] Inicio de sesión sin conexión a internet | Usuario registrado (cuenta principal), app instalada, modo avión activado | 1. Abrir la app.<br>2. Ingresar `qa.user@shopgo.com` y `Clave1234`.<br>3. Tocar "Iniciar sesión".<br>4. Desactivar el modo avión y tocar "Iniciar sesión" otra vez. | Paso 3: la app no se cierra ni se queda cargando sin fin. Indica un problema de conexión (no "Correo o contraseña incorrectos") y conserva los datos escritos **(S-4)**. No cuenta como intento fallido **(S-3)**. Paso 4: se abre la pantalla principal con "Bienvenido". | Media |
| TC-12 | [Mobile] Rotar la pantalla con los datos ya escritos | Usuario registrado (cuenta principal), app instalada, con conexión, rotación automática activada | 1. Abrir la app en vertical.<br>2. Ingresar `qa.user@shopgo.com` y `Clave1234`.<br>3. Girar el teléfono a horizontal y luego otra vez a vertical.<br>4. Tocar "Iniciar sesión". | Después de cada giro se conservan el correo y la contraseña, y la contraseña sigue oculta. El botón "Iniciar sesión" queda visible. En el paso 4 se abre la pantalla principal con "Bienvenido". | Media |

## Resumen de cobertura

| Tipo | Casos |
|---|---|
| Positivos | TC-01, TC-06 |
| Negativos | TC-02, TC-03, TC-04, TC-05, TC-08 |
| Valores límite | TC-06, TC-07, TC-10 |
| Reglas de negocio (bloqueo) | TC-09, TC-10 |
| Propios de mobile | TC-11, TC-12 |
