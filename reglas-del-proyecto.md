# Reglas del Proyecto Huellas Lab Social

## Identidad y Contexto

- **Dueño del Proyecto:** Santiago (Veterinario de profesión).
- **Conocimiento de Programación de Santiago:** Nulo (0 conocimiento). Todo el
  código se genera mediante IA a través de prompts.
- **Objetivo:** Crear un Sistema de Gestión de Información de Laboratorio
  Veterinario (LIMS) digital, seguro, escalable y en tiempo real.

## Reglas de Arquitectura y Código (¡NO TOCAR SIN AUTORIZACIÓN!)

1.  **Independencia y Modularidad Estricta (Anti-Monolito):**
- La lógica de cada tipo de usuario (Admin, Médico, Auxiliar) DEBE estar
  completamente separada en sus propios módulos y archivos.
- Si modificas la vista de los doctores, NO debe afectar la vista de los
  auxiliares.
- El enrutamiento, la base de datos y la interfaz gráfica deben estar
  desacoplados.
2.  **Base de Datos y Fichos (Tokens):**
- **NUNCA** usar el "Ficho" (Ej: A1, G2) como clave primaria (Primary Key) en la
  base de datos.
- **SIEMPRE** usar `UUID` (Identificadores Únicos Universales) para guardar la
  información.
- El Ficho es solo una "Fachada visual" que se calcula dinámicamente para
  evitar colisiones de muestras físicas.
- ORM a usar: `SQLAlchemy 2.0`.
3.  **Interfaz de Usuario:**
- Framework: `Flet 1.0` (UI Declarativa en Python).
- Nada de JS, HTML o CSS en el lado del cliente. Todo en Python.
4.  **Comentarios Obligatorios:**
- Si modificas, agregas o eliminas código, **DEBES** dejar un comentario
  explicando qué hiciste y por qué en términos sencillos.
- Ejemplo: `\\# Modificado por IA: Cambié esta consulta para evitar que choquen
  los fichos de los doctores.`
- Para partes críticas, agrega: `\\# ESTO ES LA BASE FUNDAMENTAL DE LA
  APLICACIÓN - NO TOCAR`.
5.  **Telemetría y Errores:**
- No usar `print()`. Usar formateo estructurado con JSON (ej. `
  python-json-logger`) para que la IA pueda leer los errores fácilmente en el
  futuro.

## Protocolo de IA

- Habla en términos claros. Santiago es veterinario, usa analogías clínicas o
  de construcción si es necesario para explicar conceptos de arquitectura de
  software.
- Antes de proponer un cambio masivo, asegúrate de que no rompe la modularidad
  establecida.
- Lee siempre este documento antes de hacer modificaciones estructurales.
