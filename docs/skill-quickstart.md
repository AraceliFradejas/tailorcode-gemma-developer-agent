# Primera prueba acompañada: un producto gratuito

Este recorrido permite probar la skill sin Colab. Necesitas Python y una sesión
disponible de Codex o Claude Code. No requiere contratar otra API. La disponibilidad
y los límites del asistente dependen de tu cuenta.

## 1. Preparar un proyecto pequeño

En una terminal situada en la raíz de tAilorCode:

```bash
python3 scripts/repair_lab.py prepare --case zero-price --workspace /tmp/tailorcode-first-demo
python3 scripts/repair_lab.py check --case zero-price --workspace /tmp/tailorcode-first-demo
```

El segundo comando debe fallar: el programa confunde un precio cero con la
falta de precio. Es una reproducción intencionada, no un fallo de instalación.
Si `/tmp/tailorcode-first-demo` ya existe, el preparador no la sobrescribe:
utiliza otro nombre y repítelo en los comandos posteriores.

## 2. Instalar en uno de los asistentes

Para Codex:

```bash
python3 scripts/install_tailorcode_skill.py --target codex --project /tmp/tailorcode-first-demo
```

Para Claude Code:

```bash
python3 scripts/install_tailorcode_skill.py --target claude --project /tmp/tailorcode-first-demo
```

Abre `/tmp/tailorcode-first-demo` como carpeta de proyecto en el asistente elegido.
Inicia una sesión nueva para comprobar que descubre la skill. Instalar archivos
correctamente no garantiza que una sesión ya abierta los haya incorporado.

## 3. Pedir el arreglo

En Codex, envía:

> Usa $tailorcode. El precio puede ser cero: un producto gratuito no debe usar el
> precio de reserva. Solo None significa precio ausente. Conserva también los
> precios negativos. Corrige el fallo y explícame cómo lo has comprobado.

En Claude Code, envía el mismo texto comenzando por `/tailorcode`.

Observa si identifica la causa en `repair_target.py`, reproduce el fallo antes
del cambio, conserva los requisitos y distingue sus comprobaciones de sus
suposiciones. La skill no garantiza que lo haga: precisamente lo estamos probando.

## 4. Comprobar por nuestra cuenta

Desde la raíz de tAilorCode, vuelve a ejecutar:

```bash
python3 scripts/repair_lab.py check --case zero-price --workspace /tmp/tailorcode-first-demo
```

Conserva la salida completa: deben ejecutarse tres tests. El comprobador rechaza
cambios en el archivo original de pruebas. Si falla, guarda el error junto al
parche en lugar de dar la tarea por resuelta.

La carpeta es temporal; copia el diff, la conversación y la salida que quieras
conservar a un destino permanente. Antes de publicarlos, revisa datos personales,
rutas y posibles credenciales.

## 5. Explicarlo con tus palabras

Al terminar deberías poder explicar por qué el programa confundía cero con un
valor ausente, cómo cambió la decisión y qué casos cubren las tres pruebas.
Esa explicación, junto al diff y la salida real, forma una demo del proyecto.

Esto es una prueba de uso individual. Para afirmar que la skill mejora al
asistente hay que realizar la [comparación controlada](skill-evaluation.md).
No rellenes ese registro con esta prueba si has visto antes la solución o recibido
ayuda distinta de la que tendrá la condición sin skill.
