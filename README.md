# 🔗 Blockchain Node — Red de Grados Académicos

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-OpenAPI-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)

*Nodo independiente de una red blockchain distribuida para la gestión y validación de grados académicos.*

</div>

---

## 📋 Tabla de Contenidos

- [🏗 Arquitectura](#-arquitectura)
- [🛠 Tecnologías](#-tecnologías)
- [✅ Requisitos Previos](#-requisitos-previos)
- [🚀 Instalación](#-instalación)
- [⚙️ Configuración](#️-configuración)
- [🗄 Base de Datos](#-base-de-datos)
- [▶️ Ejecución](#️-ejecución)
- [📡 API Endpoints](#-api-endpoints)
- [⛓ Lógica Blockchain](#-lógica-blockchain)
- [🗺 Fases del Proyecto](#-fases-del-proyecto)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [👤 Autor](#-autor)

---

## 🏗 Arquitectura

     ┌─────────────────┐
     │   NODO MARIANO  │  :8001
     │   (Flask API)   │
     └────────┬────────┘
              │  Comunica y propaga
    ┌─────────┼──────────┐
    ▼         ▼          ▼

   Nodo :8002  Nodo :8003  Nodo :XXXX
   (Laravel)  (Next.js)   (Express)
   Todos conectados a su propia instancia de Supabase

> Cada nodo es **autónomo e independiente**. La red sigue funcionando aunque uno o más nodos fallen.

---

## 🛠 Tecnologías

| Capa | Tecnología |
|:---|:---|
| Backend | Python 3.11+ / Flask 3.x |
| Base de Datos | Supabase (PostgreSQL) |
| Proof of Work | SHA-256 |
| Documentación | Swagger UI / OpenAPI 3.0 |
| Comunicación | HTTP REST (requests) |
| Variables de Entorno | python-dotenv |

---

## ✅ Requisitos Previos

- Python **3.11+**
- `pip` / `venv`
- Cuenta en [Supabase](https://supabase.com)
- GCC instalado (para compilar dependencias nativas)

# Fedora / RHEL
sudo dnf install gcc gcc-c++ python3-devel make -y

# Ubuntu / Debian
sudo apt install build-essential python3-dev -y


🚀 Instalación
# 1. Clonar el repositorio
git clone https://github.com/msleazy/blockchain-node.git
cd blockchain-node

# 2. Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

# 3. Instalar dependencias
pip install -r requirements.txt


⚙️ Configuración
Crea un archivo .env en la raíz del proyecto con tus credenciales:
# Supabase (Project Settings → API)
SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
SUPABASE_KEY=tu_anon_key_aqui

# Identidad de este nodo
NODE_ID=nodo-mariano
NODE_PORT=8001


⚠️ Nunca subas el .env a GitHub. Ya está incluido en el .gitignore.


🗄 Base de Datos
Ejecuta el siguiente SQL completo en el SQL Editor de Supabase:
-- ─────────────────────────────────────────
-- TABLAS DE CATÁLOGO
-- ─────────────────────────────────────────

CREATE TABLE personas (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre          VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100),
    curp            VARCHAR(18) UNIQUE,
    correo          VARCHAR(150),
    creado_en       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE instituciones (
    id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre    VARCHAR(255) NOT NULL,
    pais      VARCHAR(100),
    estado    VARCHAR(100),
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE niveles_grado (
    id     SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

INSERT INTO niveles_grado (nombre) VALUES
    ('Técnico'), ('Licenciatura'), ('Maestría'),
    ('Doctorado'), ('Especialidad');

CREATE TABLE programas (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre         VARCHAR(255) NOT NULL,
    nivel_grado_id INT REFERENCES niveles_grado(id),
    creado_en      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ─────────────────────────────────────────
-- TABLA PRINCIPAL — BLOQUES BLOCKCHAIN
-- ─────────────────────────────────────────

CREATE TABLE grados (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    persona_id      UUID REFERENCES personas(id) ON DELETE CASCADE,
    institucion_id  UUID REFERENCES instituciones(id),
    programa_id     UUID REFERENCES programas(id),
    fecha_inicio    DATE,
    fecha_fin       DATE,
    titulo_obtenido VARCHAR(255),
    numero_cedula   VARCHAR(50),
    titulo_tesis    TEXT,
    menciones       VARCHAR(100),
    -- Campos blockchain
    hash_actual     TEXT NOT NULL,
    hash_anterior   TEXT,
    nonce           INTEGER,
    firmado_por     VARCHAR(255),
    creado_en       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ─────────────────────────────────────────
-- TABLAS DE RED
-- ─────────────────────────────────────────

CREATE TABLE nodos (
    id            SERIAL PRIMARY KEY,
    url           VARCHAR(255) UNIQUE NOT NULL,
    registrado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transacciones_pendientes (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    persona_id      UUID,
    institucion_id  UUID,
    programa_id     UUID,
    fecha_inicio    DATE,
    fecha_fin       DATE,
    titulo_obtenido VARCHAR(255),
    numero_cedula   VARCHAR(50),
    titulo_tesis    TEXT,
    menciones       VARCHAR(100),
    creado_en       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


▶️ Ejecución
# 1. Activar entorno virtual
source venv/bin/activate

# 2. Iniciar el nodo
python run.py

Salida esperada en consola:
╔══════════════════════════════════════╗
║   🔗 Blockchain Node iniciado        ║
║   ID:     nodo-mariano               ║
║   Puerto: 8001                       ║
║   Docs:   http://localhost:8001/docs ║
╚══════════════════════════════════════╝

📖 Documentación Swagger disponible en: http://localhost:8001/docs

📡 API Endpoints



Método
Endpoint
Descripción



GET
/health
Estado del nodo


GET
/chain
Retorna la cadena completa


POST
/transactions
Crear transacción y propagarla


POST
/mine
Minar bloque y propagarlo


POST
/blocks/receive
Recibir bloque de otro nodo


POST
/nodes/register
Registrar un nodo en la red


GET
/nodes
Listar nodos registrados


GET
/nodes/resolve
Ejecutar algoritmo de consenso


GET
/docs
Swagger UI


🧪 Ejemplos de uso con cURL
# ── Health check ───────────────────────────────────────
curl http://localhost:8001/health

# ── Ver la cadena completa ─────────────────────────────
curl http://localhost:8001/chain

# ── Crear una transacción ──────────────────────────────
curl -X POST http://localhost:8001/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "persona_id":      "uuid-persona",
    "institucion_id":  "uuid-institucion",
    "programa_id":     "uuid-programa",
    "titulo_obtenido": "Ingeniero en Sistemas",
    "fecha_fin":       "2024-06-01"
  }'

# ── Minar un bloque ────────────────────────────────────
curl -X POST http://localhost:8001/mine

# ── Registrar otro nodo ────────────────────────────────
curl -X POST http://localhost:8001/nodes/register \
  -H "Content-Type: application/json" \
  -d '{"url": "http://localhost:8002"}'

# ── Resolver conflictos (consenso) ─────────────────────
curl http://localhost:8001/nodes/resolve


⛓ Lógica Blockchain
🔐 Cálculo del Hash
Cada bloque genera su huella digital con SHA-256 concatenando sus campos clave:
hash_actual = SHA256(
    persona_id      +
    institucion_id  +
    titulo_obtenido +
    fecha_fin       +
    hash_anterior   +
    nonce
)

⛏ Proof of Work
El nonce se incrementa hasta encontrar un hash que cumpla la dificultad establecida:
DIFFICULTY = "000"

while not hash_resultado.startswith(DIFFICULTY):
    nonce += 1
    hash_resultado = calcular_hash(..., nonce)

🤝 Algoritmo de Consenso — Longest Chain Rule
Cuando dos nodos minan simultáneamente, GET /nodes/resolve consulta
todos los nodos registrados y adopta la cadena válida más larga:
Nodo A: [G] → [B1] → [B2] → [B3]   ✅ GANA (longitud 4)
Nodo B: [G] → [B1] → [B2]           ❌ Reemplazada


🗺 Fases del Proyecto

 Fase 1 — Setup: API funcional en puerto :8001
 Fase 2 — Registro: Endpoints de comunicación inter-nodos
 Fase 3 — Pruebas de Red: Propagación de transacciones y bloques
 Fase 4 — Consenso: Resolución de conflictos distribuida


📁 Estructura del Proyecto
blockchain-node/
├── app/
│   ├── __init__.py          # Factory de la app Flask
│   ├── blockchain.py        # Lógica core (hash, PoW, consenso)
│   ├── database.py          # Cliente Supabase
│   └── routes/
│       ├── __init__.py
│       ├── chain.py         # GET  /chain
│       ├── transactions.py  # POST /transactions
│       ├── mine.py          # POST /mine
│       └── nodes.py         # POST /nodes/register | GET /nodes/resolve
├── .env                     # Variables de entorno (⚠️ no commitear)
├── .gitignore
├── openapi.yaml             # Especificación OpenAPI / Swagger
├── requirements.txt
└── run.py                   # Entry point


👤 Autor
Mariano — Nodo independiente dentro de la Red Blockchain📚 Materia: Tópicos Avanzados de Desarrollo Web y Móvil



🔒 Este nodo es autónomo. La red continúa operando aunque este nodo esté offline.
