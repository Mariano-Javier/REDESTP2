from flask import Flask, request, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

# Función para conectar a la BD
def conectar_db():
    return sqlite3.connect('gestion_tareas.db')


# Rutas para la API.

@app.route('/registro', methods=['POST'])
def registro():
    datos = request.get_json()
    usuario = datos.get('usuario')
    contrasena = datos.get('contrasena')
    
    # Hashear la contraseña antes de guardar usando werkzeug.security.
    hash_puntero = generate_password_hash(contrasena)
    
    try:
        db = conectar_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO usuarios (usuario, contrasena_hash) VALUES (?, ?)', (usuario, hash_puntero))
        db.commit()
        return jsonify({"mensaje": "Usuario registrado con éxito"}), 201
    except Exception as e:
        return jsonify({"error": "El usuario ya existe o hubo algun error"}), 400
    finally:
        db.close()

@app.route('/tareas', methods=['GET'])
def tareas():
    # Retorna el HTML de bienvenida.
    return render_template('bienvenida.html')

@app.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    usuario_ingresado = datos.get('usuario')
    contrasena_ingresada = datos.get('contrasena')
    
    db = conectar_db()
    cursor = db.cursor()
    # Se busca al usuario en la BD
    cursor.execute('SELECT id, contrasena_hash FROM usuarios WHERE usuario = ?', (usuario_ingresado,))
    resultado = cursor.fetchone()
    
    if resultado:
        user_id = resultado[0] 
        hash_guardado = resultado[1]
        
	# Usamos werkzeug.security para leer la contraseña hasheada.
        if check_password_hash(hash_guardado, contrasena_ingresada):
        # Buscamos el ID para enviárselo al cliente
            db.close() 
            return jsonify({"mensaje": "Inicio de sesión exitoso", "user_id": user_id}), 200
        else:
            db.close()
            return jsonify({"error": "Contraseña incorrecta"}), 401
    else:
        db.close()
        return jsonify({"error": "Usuario no encontrado"}), 404
  
@app.route('/crear_tarea', methods=['POST'])
def crear_tarea():
    datos = request.get_json()
    titulo = datos.get('titulo')
    usuario_id = datos.get('usuario_id') # El ID del usuario que inició sesión
    
    if not titulo or not usuario_id:
        return jsonify({"error": "Faltan datos obligatorios"}), 400
        
    db = conectar_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO tareas (titulo, usuario_id) VALUES (?, ?)', (titulo, usuario_id))
    db.commit()
    db.close()
    
    return jsonify({"mensaje": "Tarea creada con éxito"}), 201

@app.route('/mis_tareas/<int:user_id>', methods=['GET'])
def mis_tareas(user_id):
    db = conectar_db()
    cursor = db.cursor()
    # Buscamos las tareas que pertenecen al usuario logeado.
    cursor.execute('SELECT id, titulo, completada FROM tareas WHERE usuario_id = ?', (user_id,))
    tareas_db = cursor.fetchall()
    db.close()
    
    # Convertimos el resultado en una lista de diccionarios para que sea un JSON válido.
    lista_tareas = []
    for t in tareas_db:
        lista_tareas.append({
            "id": t[0],
            "titulo": t[1],
            "completada": bool(t[2])
        })
        
    return jsonify(lista_tareas), 200
    
if __name__ == '__main__':
    app.run(debug=True)