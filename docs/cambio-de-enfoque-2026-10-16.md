# De un agente de competición a una skill para aprender corrigiendo

**Fecha:** 16 de octubre de 2026, Europe/Madrid.

**Autora y directora del proyecto:** Araceli Fradejas Muñoz.

## La decisión

Araceli inició tAilorCode para construir con IA un proyecto que pudiera enseñar
en su portfolio y que reflejara su aprendizaje. Tras varios días preparando el
entorno de Kaggle y Colab, consiguió una ejecución real con Gemma: el evaluador
dio por resuelta una incidencia pública de FastAPI. Sin embargo, el trabajo
visible seguía resultando pequeño y abstracto en comparación con la preparación.

Araceli explicó que no iba a presentar el reto de Kaggle. El objetivo dejó de ser
preparar otro envío o ampliar pruebas con GPU. Se decidió transformar lo aprendido
en una herramienta que una persona pudiera usar y comprender.

Primero se planteó una aplicación con Streamlit: pegar código, describir un fallo,
ver una explicación, comparar el cambio y consultar su verificación. Después,
Araceli propuso convertir el flujo en una skill para Claude o Codex y aprobó ese
plan. La skill pasa a ser la primera entrega; la demo visual queda como una
segunda capa para visitantes del portfolio.

## Qué producto queremos

**tAilorCode · Corrige y aprende** ayuda a reparar un error acotado de Python en
un proyecto y explica el arreglo mediante evidencia del código y de sus pruebas.

El usuario describe el fallo desde Codex o Claude Code. El asistente identifica
el comportamiento esperado, busca una reproducción, modifica lo necesario,
comprueba el resultado y explica la causa y el cambio. Puede trabajar solo en
modo diagnóstico cuando eso es lo solicitado. El lenguaje de las explicaciones
se adapta al usuario.

La skill distingue un resultado verificado con pruebas, uno comprobado solo en
sintaxis, una propuesta no verificada y un problema sin resolver. Esta distinción
hace visible qué sabemos realmente, en lugar de equiparar una respuesta convincente
con una solución demostrada.

## Qué reutilizamos y qué cambiamos

| Etapa anterior | Nueva aplicación |
| --- | --- |
| Investigar una incidencia de repositorio | Investigar un fallo en el proyecto del usuario. |
| Crear un parche pequeño | Entregar un diff comprensible y acotado. |
| Verificar con el evaluador | Ejecutar las comprobaciones disponibles y conservar sus resultados. |
| Preservar logs y resultado | Explicar qué se ejecutó y qué sigue sin comprobar. |
| Gemma servido en A100 | Modelo y herramientas del asistente anfitrión. |
| Restricción de competición contra editar tests | En desarrollo normal se permiten nuevos tests de regresión, conservando los criterios de aceptación. |

No hemos convertido los pesos de Gemma ni entrenado un modelo. Una skill es un
paquete de instrucciones y recursos que guía a un asistente existente. Su valor
específico deberá demostrarse con evaluación: esos asistentes ya saben corregir
código sin nuestra skill.

## Primera entrega implementada

- Fuente única en `skills/tailorcode/`, con instrucciones portables y una referencia
  breve para explicar reparaciones. Incluye metadatos de interfaz para Codex.
- Instalador de ámbito de proyecto: copia a `.agents/skills/tailorcode/` para Codex
  o `.claude/skills/tailorcode/` para Claude Code. Conserva instalaciones existentes
  y no cambia configuraciones globales. Claude recibe el contenido portable sin
  los metadatos propios de la interfaz de Codex.
- Tres ejercicios propios de Python, independientes del dataset de Kaggle:
  listas por defecto compartidas, precio cero y extremos inclusivos.
- Laboratorio sin dependencias externas para preparar carpetas nuevas y comprobar
  los tests de aceptación originales después del arreglo.
- Pruebas automatizadas que verifican los ejercicios y el instalador; una corrección
  de referencia valida cada ejercicio sin atribuirla a un asistente.
- Protocolo de comparación con y sin skill y registro de resultados inicialmente
  vacío. No se han inventado métricas de mejora.

La distribución en carpetas sigue las ubicaciones de la documentación oficial de
[Codex](https://learn.chatgpt.com/docs/build-skills) y
[Claude Code](https://code.claude.com/docs/en/skills), consultada el 16 de octubre.
La estructura compartida no demuestra por sí sola compatibilidad en ejecución:
ese punto requiere una sesión nueva real en cada producto.

## Validación y límites

Las comprobaciones estructurales validan el formato. Las pruebas del laboratorio
verifican que cada implementación original falla por aserciones y que una
corrección manual de referencia pasa, sin sustituir las pruebas del ejercicio.
También comprueban que no se sobrescriben carpetas ni skills existentes.

La entrega pasó **31 tests locales**, el validador estructural de skills y las
comprobaciones previas de empaquetado/notebook. La
[guía de primera prueba](skill-quickstart.md) deja preparado el recorrido de uso.

No son evaluaciones de Codex o Claude. Tampoco el resultado previo de Gemma prueba
la calidad de esta skill: corresponde a otra configuración y otro modelo.

El laboratorio ejecuta Python local: sirve para estos ejemplos conocidos y no
constituye aislamiento para código arbitrario de visitantes. La futura web tendrá
que separar el análisis de código del permiso y aislamiento necesarios para
hacerlo ejecutar. No se ha implementado ni desplegado esa web en esta entrega.

## Plan para el fin de semana del 17 y 18 de octubre

1. Abrir el primer ejercicio en una sesión nueva de Codex, comprobar la invocación
   y guardar el diff, explicación y salida de tests. Corregir defectos de la skill
   demostrados por esa prueba.
2. Repetir en Claude Code y completar las parejas con/sin skill descritas en el
   [protocolo de evaluación](skill-evaluation.md). Mantener los fallos en el registro.
3. Preparar una demostración visual de un recorrido real y sus evidencias.
   Decidir entonces si basta una demo grabada/página o si Streamlit aporta valor.
4. Publicar una explicación de lo aprendido y las limitaciones junto con el código.

Una primera versión durante el fin de semana es un objetivo de alcance, no una
promesa de compatibilidad o calidad antes de hacer esas pruebas. No se necesitan
más sesiones de A100 para esta etapa. El uso de cada asistente sigue sujeto a
los límites y costes de su cuenta.

## Cómo contarlo en el portfolio

“Desarrollé un agente de reparación de código con Gemma y lo ejecuté en una A100.
Después transformé el flujo en una skill educativa reutilizable para asistentes
de programación, con ejercicios reproducibles y un protocolo para evaluar tanto
la corrección como las explicaciones.”

El relato conserva el experimento original y explica por qué evolucionó. La
aportación demostrable es el flujo, las herramientas, los tests y la evaluación;
la mejora sobre un asistente sin skill se contará solo si los resultados la apoyan.
