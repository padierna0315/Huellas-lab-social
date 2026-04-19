# Agent Skills Registry

This project uses SDD (Spec-Driven Development) and adheres to specific architectural guidelines.

## Project Standards (auto-resolved)
- **Independencia y Modularidad Estricta:** Lógica de admin, médico y auxiliar separadas.
- **Fichos (Tokens):** NUNCA usar como Primary Key, siempre usar UUID.
- **UI Declarativa:** Flet 1.0 (No HTML/JS/CSS).
- **ORM:** SQLAlchemy 2.0.
- **Logs Estructurados:** python-json-logger, nunca print().
- **Comentarios:** Explicaciones claras sobre los cambios realizados.

## User Skills
- `reglas-del-proyecto` (Loaded automatically for all agents touching this project)