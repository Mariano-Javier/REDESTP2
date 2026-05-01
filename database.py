import sqlite3

def crear_tablas():
    # Conexión al archivo de base de datos (se crea si no existe)
    conexion = sqlite3.connect('gestion_tareas.db')
    cursor = conexion.cursor()
    
    # Tabla de usuarios con el campo para la contraseña hasheada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena_hash TEXT NOT NULL
        )
    ''')

    # Tabla de tareas para los usuarios.
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tareas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        completada INTEGER DEFAULT 0,
        usuario_id INTEGER,
        FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
    )
''')
    
    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    crear_tablas()