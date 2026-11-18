# Parte 4 — Reporte de bug

## BUG-001 · [Android] Carrito: la cantidad de un producto vuelve a 1 al rotar la pantalla

| Campo | Valor |
|---|---|
| Origen | Reporte de un usuario |
| Estado | Nuevo, **pendiente de reproducir internamente** |
| Módulo | Carrito de compras |
| Plataforma | Android (sin confirmar si también pasa en iOS) |

## Entorno

| Dato | Valor |
|---|---|
| Dispositivo | Samsung, modelo exacto **por confirmar** (pregunta 1) |
| Sistema operativo | Android 13 (capa One UI **por confirmar**) |
| Versión de la app | **Por confirmar** (pregunta 2) |
| Orientación | Cambio de vertical a horizontal (rotación automática activada) |

## Precondiciones

- ShopGo instalada en un dispositivo Android 13 con la rotación automática activada.
- Usuario con sesión iniciada.
- Carrito vacío al empezar.

## Pasos para reproducir

1. Abrir ShopGo con el teléfono en vertical.
2. Agregar una camisa al carrito (cantidad inicial: 1).
3. Abrir el carrito y cambiar la cantidad de la camisa a **3**.
4. Verificar que el carrito muestra cantidad 3 y el subtotal correspondiente.
5. Girar el teléfono a horizontal.
6. Observar la cantidad y el subtotal de la camisa.

## Resultado esperado

La cantidad sigue siendo **3** después de rotar. El subtotal y el costo de envío no cambian.

## Resultado actual (según el usuario)

La cantidad vuelve a **1** después de rotar.

Además, hay que confirmar si cambian también el subtotal y el envío. Por ejemplo, con una camisa de
₡9 000, 3 unidades suman ₡27 000 (envío gratis) y 1 unidad suma ₡9 000 (envío de ₡2 500). El cambio de
cantidad puede cambiar lo que el usuario paga.

## Severidad: Alta

Se pierden en silencio datos que el usuario ya ingresó en el carrito, y eso cambia el monto del pedido:
podría comprar menos unidades de las que quería o pagar un envío que no le correspondía. No es crítica
porque la app no se cierra y hay una forma de evitarlo: volver a poner la cantidad o no rotar.

## Prioridad: Alta

Rotar el teléfono es una acción muy común, y el error está en el flujo de compra, que afecta directamente
las ventas. Además, Samsung con Android 13 es una combinación con muchos usuarios.

## Evidencia que adjuntaría

- **Video** de la pantalla (grabación nativa o `adb shell screenrecord`) con todo el flujo: cantidad 3, rotación y cantidad 1.
- **Capturas** del carrito antes y después de rotar, con la cantidad y el subtotal visibles.
- **Logs** de `adb logcat` filtrados por el paquete de ShopGo durante la rotación (para ver si la Activity se recrea o si hay errores).
- **Estado del carrito en el backend** (respuesta de la API del carrito) antes y después de rotar, para saber si la cantidad se pierde solo en pantalla o también en el servidor.
- Datos del dispositivo: modelo (`adb shell getprop ro.product.model`) y versión de la app (Ajustes → Aplicaciones → ShopGo).

## Preguntas abiertas (información que falta)

1. ¿Cuál es el modelo exacto del Samsung y la versión de One UI?
2. ¿Qué versión de ShopGo tiene instalada?
3. ¿Cómo cambió la cantidad a 3: con los botones +/−, escribiendo el número o agregando la camisa tres veces?
4. ¿Pasa con otros productos y con otras cantidades, o solo con camisas?
5. Si vuelve a girar a vertical, ¿se recupera la cantidad 3?
6. Si sale del carrito y vuelve a entrar, ¿qué cantidad aparece? Si llegó a pagar, ¿cuántas unidades se cobraron?
7. ¿Pasa también en otros dispositivos o versiones de Android, y en iOS?
8. ¿Estaba usando pantalla dividida o ventana flotante?

## Notas para la reproducción y el análisis (QA)

- Reproducir primero en un Samsung con Android 13 y después en un emulador Pixel con Android 13 y 14, para separar un problema de Samsung de uno general de Android.
- Activar la opción de desarrollador **"No mantener actividades"** para forzar la recreación de la pantalla y comprobar si el estado del carrito se pierde.
- **Hipótesis técnica (sin confirmar):** al rotar, Android recrea la Activity o el Fragment por un cambio de configuración. Si la cantidad solo vive en la vista y no se guarda en un `ViewModel`, en `onSaveInstanceState` o en el backend, vuelve a su valor inicial.
- Cuando se corrija, agregar un caso de regresión: rotar la pantalla en el carrito con cantidades distintas de 1, incluida una que cruce el umbral de envío gratis.
