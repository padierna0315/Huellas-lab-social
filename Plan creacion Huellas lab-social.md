# Plan creacion de aplicacion

**Documento de Requisitos del Producto (PRD): Sistema de Gestión de Información de Laboratorio Veterinario (LIMS)**

## Resumen Ejecutivo y Visión Arquitectónica

La transición de un modelo de gestión clínica fundamentado en transcripciones manuales y registros físicos hacia un Sistema de Gestión de Información de Laboratorio (LIMS) totalmente digital representa una evolución operativa crítica para cualquier entorno veterinario. El presente documento arquitectónico detalla los requisitos, estructuras y algoritmos necesarios para construir una plataforma centralizada y en tiempo real. Esta herramienta está diseñada para erradicar los errores de transcripción, garantizar la trazabilidad absoluta de las muestras biológicas, aplicar controles de acceso granulares basados en roles (RBAC) y automatizar el enrutamiento de resultados diagnósticos mediante el análisis sintáctico de archivos.

El ecosistema veterinario en cuestión posee una topología de personal específica: un administrador general (Santiago), un cuerpo médico principal (Aura, Giovanni, Marcela, Mariana, Yhon), personal administrativo (La Mona, Cristi) y personal clínico auxiliar (Daniel). La arquitectura debe modelar estas jerarquías, asegurando que las interfaces gráficas se adapten dinámicamente a la sesión autenticada. La plataforma será programable enteramente en Python, utilizando Flet 1.0 (Interfaz Declarativa) para la UI, SQLAlchemy 2.0 para la persistencia de datos y FastAPI/Uvicorn para el despliegue web asíncrono.

## Refactorización de la Lógica de Negocio y Mitigación de Vulnerabilidades

### Autenticación y Criptografía
La arquitectura implementa Control de Acceso Basado en Roles (RBAC) gestionado a nivel de base de datos. Las contraseñas se almacenarán utilizando bcrypt (hash unidireccional + salt). El administrador poseerá una interfaz dedicada para gestionar usuarios.

### Gestión de Identificadores Visuales (Fichos)
Se desacopla la clave primaria (UUID inmutable) del identificador visual (Ficho A1, G3). El Ficho es una propiedad visual transitoria calculada en tiempo real. Se utilizará el número entero más bajo disponible en estado PENDING, evitando la colisión física de muestras.

### Integración con AnalizaVet (Automatización de Datos)
Para integrar la herramienta con "AnalizaVet", se habilitará en el Panel de Administrador un botón de "Descargar Lista de Exámenes" que generará un archivo **JSON** estructurado con los pacientes pendientes.

### Enrutamiento Automático y Procesamiento de Resultados
La automatización de resultados se realiza mediante el análisis de PDFs. Se implementará:
1. **Motor Regex:** Para extraer metadatos de archivos nombrados como `Mascota - Tutor - Medico.pdf`.
2. **Desbloqueo Automático:** Al subir los PDFs finales, el sistema identifica automáticamente el paciente, adjunta el PDF, marca el examen como PROCESSED y libera el Ficho correspondiente automáticamente.

## Interfaz de Usuario y Experiencia del Médico

### Visor de Resultados del Médico
La interfaz médica presentará un diseño de pantalla dividida:
1. **Visor de PDF Nativo:** Visualización directa del PDF original (sin OCR intermedio) para garantizar integridad médica, permitiendo zoom e inspección.
2. **Panel de Feedback/Observaciones:** Un panel interactivo lateral donde el médico puede enviar notas, sugerencias o alertas directamente al laboratorio/administración, gestionado mediante el sistema de mensajería interno (tipo ALERT o FEEDBACK).

## Pila Tecnológica y Arquitectura

- **Framework UI:** Flet 1.0 (Paradigma Declarativo).
- **ORM:** SQLAlchemy 2.0 con mapeo tipado.
- **Backend:** FastAPI + Uvicorn (ASGI).
- **Telemetría:** Logs estructurados en JSON (python-json-logger).

## Estructura de la Base de Datos (SQLAlchemy)

- **Users:** id, username, password_hash, full_name, role, prefix, is_active.
- **Samples:** id, display_token, medico_id, created_by_id, pet_name, owner_name, species, exam_type, priority_weight, status, created_at.
- **Messages:** id, recipient_id, message_type (RESULT, ALERT, FEEDBACK), content, related_sample_id, is_read, created_at.

## Topología de Directorios Modular

- `lims_vet/`
  - `main.py`
  - `config.py`
  - `core/` (security.py, database.py, pubsub_manager.py)
  - `models/` (base.py, user.py, sample.py, message.py)
  - `views/` (auth_view.py, admin/, medico/, auxiliar/, compartido/)
  - `components/` (tokens_visuales.py, navegacion.py)
