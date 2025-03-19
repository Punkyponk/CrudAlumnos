from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Alumno  # Importamos db y el modelo Alumno desde models.py

# Crear la app Flask
app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://samvela2_user:q53B7DTCFKb0NBXeTuFp0mYCj8hi3VPA@dpg-cv8vf3hu0jms73edrqg0-a.oregon-postgres.render.com/samvela2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la extensión SQLAlchemy con la app
db.init_app(app)

# Rutas del CRUD

# Mostrar todos los alumnos
@app.route('/')
def index():
    alumnos = Alumno.query.all()
    return render_template('index.html', alumnos=alumnos)

# Crear un nuevo alumno - Método POST
@app.route('/alumno', methods=['POST'])
def create_alumno():
    # Obtener datos enviados en el cuerpo de la solicitud en formato JSON
    data = request.get_json()

    # Validar que los datos contengan los campos necesarios
    if 'nombre' not in data or 'edad' not in data or 'carrera' not in data:
        return jsonify({'error': 'Datos incompletos'}), 400

    # Crear un nuevo objeto Alumno con los datos recibidos
    nuevo_alumno = Alumno(nombre=data['nombre'], edad=data['edad'], carrera=data['carrera'])
    
    # Agregar el nuevo alumno a la base de datos
    db.session.add(nuevo_alumno)
    db.session.commit()

    # Responder con el alumno recién creado
    return jsonify({'id': nuevo_alumno.id, 'nombre': nuevo_alumno.nombre, 'edad': nuevo_alumno.edad, 'carrera': nuevo_alumno.carrera}), 201

# Crear un nuevo alumno (Vista)
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        carrera = request.form['carrera']
        
        nuevo_alumno = Alumno(nombre=nombre, edad=edad, carrera=carrera)
        db.session.add(nuevo_alumno)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('create.html')

# Actualizar un alumno
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    alumno = Alumno.query.get_or_404(id)

    if request.method == 'POST':
        alumno.nombre = request.form['nombre']
        alumno.edad = request.form['edad']
        alumno.carrera = request.form['carrera']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('update.html', alumno=alumno)

# Eliminar un alumno
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    alumno = Alumno.query.get_or_404(id)

    if request.method == 'POST':
        db.session.delete(alumno)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('delete.html', alumno=alumno)

if __name__ == "__main__":
    app.run(debug=True)
