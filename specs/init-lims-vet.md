# Especificaciones: init-lims-vet

## 1. Estructura de Carpetas (Modularidad Estricta)
La estructura sigue un diseño modular para separar las responsabilidades de los distintos perfiles de usuario.

```text
src/
├── core/                # Configuración, Logger, Base de Datos
│   ├── config.py
│   ├── logger.py        # python-json-logger
│   └── database.py      # SQLAlchemy 2.0 engine, Base
├── modules/             # Lógica independiente por perfil
│   ├── admin/           # Gestión de usuarios, roles
│   ├── medico/          # Consultas, solicitudes de examen
│   └── auxiliar/        # Recepción de muestras, carga de resultados
├── infra/               # Infraestructura y Puentes
│   ├── pubsub/          # Definición de eventos y bus
│   └── external/        # Integraciones externas (AnalizaVet)
└── main.py              # Entrypoint Flet (UI Declarativa)
```

## 2. Esquema de Base de Datos (SQLAlchemy 2.0 + UUID)
Se utilizarán `UUID` como clave primaria en todas las entidades. NUNCA se usarán tokens o IDs secuenciales como clave primaria.

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from uuid import UUID, uuid4

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    role: Mapped[str] = mapped_column(String(50)) # admin, medico, auxiliar

class Sample(Base):
    __tablename__ = "samples"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    patient_id: Mapped[UUID] = mapped_column()
    status: Mapped[str] = mapped_column(String(50)) # pendiente, procesando, completado
```

## 3. Especificación de Exportación JSON AnalizaVet
El formato para la integración externa será:

```json
{
  "header": {
    "version": "1.0",
    "timestamp": "ISO8601"
  },
  "sample": {
    "uuid": "UUID",
    "external_id": "STRING"
  },
  "result": {
    "code": "STRING",
    "value": "FLOAT/STRING"
  }
}
```

## 4. Definición de Flujo de Eventos PubSub
*   `event.sample.created`: Disparado cuando el médico solicita un examen.
*   `event.sample.received`: Disparado cuando el auxiliar marca la muestra como recibida.
*   `event.result.entered`: Disparado cuando el auxiliar carga el resultado.

## 5. Escenarios (Given/When/Then)

### Escenario 1: Solicitud de nuevo examen
*   **Given** que el usuario tiene rol 'medico'
*   **When** el médico crea una orden de examen para un paciente
*   **Then** se crea un registro `Sample` con estado 'pendiente' y se emite evento `event.sample.created`

### Escenario 2: Carga de resultado de laboratorio
*   **Given** que existe una `Sample` con estado 'recibido'
*   **When** el usuario con rol 'auxiliar' carga el resultado
*   **Then** se actualiza `Sample` a 'completado', se guarda el resultado y se emite `event.result.entered`
