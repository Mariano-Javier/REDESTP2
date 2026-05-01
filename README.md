#  Sistema de Gestión de Tareas

Aplicación basada en arquitectura **Cliente-Servidor** con una API REST desarrollada en Flask y persistencia en SQLite.

---

##  Tecnologías

* Python 3.10+
* Flask
* SQLite3
* Requests

---

##  Estructura del Proyecto

Organización de los archivos para garantizar **modularidad y separación de responsabilidades**:

```bash
REDESTP2/
├── venv/                  # Entorno virtual (Aislamiento de recursos)
├── img/                   # Imágenes del proyecto
├── templates/             # Plantillas HTML (Capa de presentación)
│   └── bienvenida.html    # Documentación y guía de uso
├── cliente.py             # Cliente de Consola (Interactúa con la API)
├── servidor.py            # Servidor Flask (Backend y lógica de negocio)
├── database.py            # Script para inicializar tablas en SQLite
├── gestion_tareas.db      # Base de datos persistente
└── requirements.txt       # Librerías necesarias (Flask, Requests)
```

---

## Interoperabilidad del Sistema

Una de las ventajas de esta arquitectura es que el **Servidor Flask** expone una interfaz estandarizada (**API REST**). Esto permite obtener el mismo resultado utilizando diferentes clientes:

### Cliente de Consola (Python)

* Uso mediante menú en terminal
* Utiliza `requests` para comunicarse automáticamente

###  Herramientas de API (Thunder Client / Postman)

* Permiten testear endpoints manualmente
* Envío de paquetes JSON

 **Conclusión técnica:**
Independientemente del cliente utilizado, la **lógica de negocio** y la **persistencia en SQLite** ocurren siempre en el servidor.
Esto garantiza consistencia: un usuario creado desde Thunder Client puede iniciar sesión desde el cliente de consola.

---

##  Guía de Ejecución

### 1. Preparación del entorno

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

### 2. Inicialización de la base de datos

```bash
python database.py
```

---

### 3. Lanzamiento del sistema

**Terminal 1 (Backend):**

```bash
python servidor.py
```

**Terminal 2 (Cliente):**

```bash
python cliente.py
```

---

## 📡 Referencia de la API

---

###  Registro

**POST** `http://127.0.0.1:5000/registro`

 Petición:
![Registro](https://github.com/Mariano-Javier/REDESTP2/blob/main/static/img/login_usuario_01.png)

 Respuesta:
![Registro OK](https://github.com/Mariano-Javier/REDESTP2/blob/main/static/img/login_usuario_02.png)

```json
{
  "usuario": "nombre_usuario",
  "contrasena": "tu_clave"
}
```

 Respuesta: `201 Usuario registrado con éxito`

---

###  Login

**POST** `http://127.0.0.1:5000/login`

 Petición:
![Login](img/login_usuario_01.png)

 Respuesta:
![Login OK](img/login_usuario_02.png)

```json
{
  "usuario": "nombre_usuario",
  "contrasena": "tu_clave"
}
```

 Respuesta: `200 OK` (Devuelve `user_id`)

---

###  Crear tarea

**POST** `http://127.0.0.1:5000/crear_tarea`

 Petición:
![Crear tarea](img/crear_tarea01.png)

 Respuesta:
![Crear tarea OK](img/crear_tarea02.png)

```json
{
  "titulo": "Descripción de la tarea",
  "usuario_id": 1
}
```

---

###  Obtener tareas

**GET** `http://127.0.0.1:5000/mis_tareas/<user_id>`

 Petición:
![Tareas](img/tareas01.png)

 Respuesta:
![Tareas OK](img/tareas02.png)

 Respuesta: `200 OK` (Lista JSON)

---

##  Manual del Cliente (cliente.py)

 Menú interactivo:
![Cliente](img/cliente01.png)

### Funcionalidades:

1. **Registrarse**

   * Solicita usuario y contraseña
   * El servidor genera un hash seguro

2. **Iniciar sesión**

   * Valida credenciales
   * Devuelve `user_id`

3. **Visualización automática**

   * Luego del login, se ejecuta automáticamente `mostrar_tareas(user_id)`
   * Se realiza una petición GET al servidor

4. **Salir**

   * Finaliza la ejecución del cliente

---

##  Flujo de Comunicación

El sistema opera bajo un modelo distribuido:

*  **Seguridad:** contraseñas hasheadas (Werkzeug)
*  **Autenticación:** validación y retorno de `user_id`
*  **Recursos:** comunicación vía HTTP (GET / POST)

---

##  Respuestas Conceptuales

###  ¿Por qué hashear contraseñas?

Es una medida crítica de seguridad. Al aplicar hashing:

*  **Privacidad:** la contraseña real nunca se almacena
*  **Seguridad:** si la base se filtra, solo hay hashes irreversibles
*  **Protección:** incluso administradores no pueden ver claves

---

###  Ventajas de SQLite

SQLite es ideal para este tipo de proyecto:

*  **Persistencia:** datos almacenados en disco
*  **Portabilidad:** archivo único `.db`
*  **Sin configuración:** no requiere servidor
*  **Ligereza:** bajo consumo de recursos

---

##  Ficha Técnica

| Característica | Detalle          |
| -------------- | ---------------- |
| Arquitectura   | Cliente-Servidor |
| API            | REST             |
| Backend        | Flask            |
| Base de Datos  | SQLite           |
| Seguridad      | PBKDF2 + salt    |

---
