from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    number = db.Column(db.Integer, unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.number} - {self.description}"


@app.route('/')
def index():
    return 'Hello World!'

@app.route('/students')
def get_students():
    students = Student.query.all()
    output = []
    for student in students:
        data = {'name': student.name, 'number': student.number, 'description': student.description}
        output.append(data)

    return {'students': output}

@app.route('/students/<id>')
def get_student(id):
    student = Student.query.get_or_404(id)
    return {'name': student.name, 'number': student.number, 'description': student.description}

@app.route('/students', methods=['POST'])
def add_student():
    student = Student(name=request.json['name'], number=request.json['number'], description=request.json['description'])
    db.session.add(student)
    db.session.commit()
    return {'id': student.id}

@app.route('/students/<id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if student is None:
        return {'message': 'error'}
    db.session.delete(student)
    db.session.commit()
    return {'message': 'ok'}
