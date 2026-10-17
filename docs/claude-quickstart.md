# Primera prueba en Claude Code

La skill fuente es la misma que para Codex: `skills/tailorcode/SKILL.md`.
El instalador copia las instrucciones y la referencia portable a
`.claude/skills/tailorcode/`, sin los metadatos exclusivos de la interfaz de Codex.
No hay una segunda skill distinta que deba mantenerse en paralelo.

El 17 de octubre se preparó una carpeta de ejercicio sin reparar, con la skill
ya instalada, en `deliverables/session-20261017/claude-first-demo/` (local y excluida
de Git). Contiene el ejemplo `independent-lists`. No se ha abierto una sesión de
Claude ni se ha medido su resultado.

## Usar la carpeta preparada

Abre **esa carpeta** como proyecto en Claude Code e inicia una conversación nueva.
Si utilizas la terminal, desde la raíz del repositorio:

```bash
cd deliverables/session-20261017/claude-first-demo
claude
```

Envía:

> /tailorcode Dos llamadas para añadir etiquetas sin proporcionar lista deben
> producir listas independientes. Si paso una lista, se debe añadir a esa misma
> lista. Corrige el fallo y explícame cómo lo has comprobado.

La demo presenta estas listas como cestas; el ejercicio usa nombres genéricos.
Guarda la respuesta y los comandos ejecutados. Después, desde la raíz del
repositorio, comprueba el resultado independientemente:

```bash
python3 scripts/repair_lab.py check --case independent-lists --workspace deliverables/session-20261017/claude-first-demo
```

## Crear otra carpeta desde un clon nuevo

La carpeta local no se distribuye con Git. Puedes recrear el ejercicio en una
ruta que no exista:

```bash
python3 scripts/repair_lab.py prepare --case independent-lists --workspace /tmp/tailorcode-claude-demo
python3 scripts/install_tailorcode_skill.py --target claude --project /tmp/tailorcode-claude-demo
```

Instalar archivos no demuestra su descubrimiento ni su lectura en Claude Code.
Solo después de la prueba real registraremos esos resultados. Los permisos y
el consumo siguen siendo los de la cuenta de Claude; no se necesita Colab.
