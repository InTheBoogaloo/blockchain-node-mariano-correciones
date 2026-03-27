# 🔗 Blockchain Node — Red Distribuida de Grados Académicos

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge\&logo=flask\&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=for-the-badge\&logo=supabase\&logoColor=white)
![Swagger](https://img.shields.io/badge/API-OpenAPI%203.0-85EA2D?style=for-the-badge\&logo=swagger\&logoColor=black)

### ⚡ Nodo blockchain autónomo para validación de grados académicos

Sistema distribuido que permite registrar, validar y verificar grados académicos utilizando principios de **blockchain**, con comunicación entre nodos independientes.

</div>

---

## 🚀 Características

* 🔗 Red blockchain distribuida entre múltiples nodos
* 🔐 Integridad de datos mediante **hash SHA-256**
* ⛏ Sistema de **Proof of Work (PoW)**
* 🤝 Algoritmo de consenso (**Longest Chain Rule**)
* 🌐 Comunicación entre nodos vía HTTP (REST)
* 📡 API documentada con **Swagger / OpenAPI**
* 🗄 Persistencia en **Supabase (PostgreSQL)**

---

## 🏗 Arquitectura del Sistema

```
     ┌─────────────────┐
     │   NODO MARIANO  │  :8001
     │   (Flask API)   │
     └────────┬────────┘
              │  Propaga datos
    ┌─────────┼──────────┐
    ▼         ▼          ▼

   Nodo :8002  Nodo :8003  Nodo :XXXX
   (Laravel)  (Next.js)   (Express)

Cada nodo:
✔ Es independiente
✔ Tiene su propia base de datos
✔ Mantiene su propia copia de la blockchain
```

> 💡 La red continúa funcionando incluso si uno o varios nodos fallan.

---

## 🛠 Stack Tecnológico

| Capa          | Tecnología              |
| :------------ | :---------------------- |
| Backend       | Python 3.11 + Flask     |
| Base de Datos | Supabase (PostgreSQL)   |
| Blockchain    | SHA-256 + Proof of Work |
| API           | REST + Swagger          |
| Comunicación  | requests                |
| Configuración | python-dotenv           |

---

## ✅ Requisitos

* Python 3.11+
* pip + venv
* Cuenta en Supabase
* Compilador C (para dependencias)

```bash
# Fedora / RHEL
sudo dnf install gcc gcc-c++ python3-devel make -y

# Ubuntu / Debian
sudo apt install build-essential python3-dev -y
```

---

## ⚙️ Instalación

```bash
git clone https://github.com/msleazy/blockchain-node.git
cd blockchain-node

python3 -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

---

## 🔧 Configuración

Crear archivo `.env`:

```env
SUPABASE_URL=https://xxxxxxxx.supabase.co
SUPABASE_KEY=tu_key

NODE_ID=nodo-mariano
NODE_PORT=8001
```

> ⚠️ Nunca subas este archivo a GitHub.

---

## 🗄 Base de Datos

Ejecuta el script SQL en Supabase para crear:

* Personas
* Instituciones
* Programas
* Grados (Blockchain)
* Nodos
* Transacciones pendientes

👉 Incluye campos blockchain como:

* `hash_actual`
* `hash_anterior`
* `nonce`

---

## ▶️ Ejecución

```bash
source venv/bin/activate
python run.py
```

Salida esperada:

```
╔══════════════════════════════════════╗
║   🔗 Blockchain Node iniciado        ║
║   ID:     nodo-mariano               ║
║   Puerto: 8001                       ║
║   Docs:   http://localhost:8001/docs ║
╚══════════════════════════════════════╝
```

---

## 📡 API Endpoints

| Método | Endpoint        | Descripción         |
| :----- | :-------------- | :------------------ |
| GET    | /health         | Estado del nodo     |
| GET    | /chain          | Blockchain completa |
| POST   | /transactions   | Nueva transacción   |
| POST   | /mine           | Minar bloque        |
| POST   | /blocks/receive | Recibir bloque      |
| POST   | /nodes/register | Registrar nodo      |
| GET    | /nodes          | Listar nodos        |
| GET    | /nodes/resolve  | Consenso            |
| GET    | /docs           | Swagger UI          |

---

## 🧪 Ejemplo de Uso

```bash
# Health check
curl http://localhost:8001/health

# Crear transacción
curl -X POST http://localhost:8001/transactions \
-H "Content-Type: application/json" \
-d '{
  "persona_id": "uuid",
  "institucion_id": "uuid",
  "programa_id": "uuid",
  "titulo_obtenido": "Ingeniero en Sistemas",
  "fecha_fin": "2024-06-01"
}'
```

---

## ⛓ Cómo Funciona la Blockchain

### 🔐 Hash

Cada bloque genera un hash único:

```
SHA256(
  persona_id +
  institucion_id +
  titulo +
  fecha +
  hash_anterior +
  nonce
)
```

---

### ⛏ Proof of Work

```
DIFFICULTY = "000"

while hash no cumple:
    nonce++
```

---

### 🤝 Consenso

Se adopta la cadena más larga válida:

```
Nodo A: [G] → [B1] → [B2] → [B3]   ✅
Nodo B: [G] → [B1] → [B2]           ❌
```

---

## 🗺 Roadmap

* ✅ Fase 1 — Nodo funcional
* ✅ Fase 2 — Comunicación entre nodos
* 🔄 Fase 3 — Propagación en red
* 🔄 Fase 4 — Consenso distribuido

---

## 📁 Estructura del Proyecto

```
blockchain-node/
├── app/
│   ├── __init__.py
│   ├── blockchain.py
│   ├── database.py
│   └── routes/
│       ├── chain.py
│       ├── transactions.py
│       ├── mine.py
│       └── nodes.py
├── .env
├── openapi.yaml
├── requirements.txt
└── run.py
```

---

## 👨‍💻 Autor

**Mariano Morales**
💻 Desarrollador | Blockchain & Backend

📚 *Tópicos Avanzados de Desarrollo Web y Móvil*

---

## 🧠 Reflexión

Este proyecto demuestra cómo aplicar conceptos de blockchain en un entorno real:

* Sistemas distribuidos
* Consistencia eventual
* Seguridad de datos
* Arquitectura desacoplada

---

## 🔒 Nota Final

> Este nodo es completamente autónomo.
> La red sigue operando incluso si este nodo deja de estar disponible.

---

⭐ Si te gusta el proyecto, dale una estrella en GitHub.

