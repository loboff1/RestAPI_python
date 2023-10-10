from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/mydatabase'
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    employee = db.relationship('Employee', backref=db.backref('positions', lazy=True))

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    position = db.Column(db.String(50), unique=True)
    last_name = db.Column(db.String(50))

@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    result = []
    for employee in employees:
        result.append({
            'id': employee.id,
            'first_name': employee.first_name,
            'last_name': employee.last_name
        })
    return jsonify(result)

@app.route('/positions', methods=['GET'])
def get_positions():
    positions = Position.query.all()
    result = []
    for position in positions:
        result.append({
            'id': position.id,
            'name': position.name
        })
    return jsonify(result)

@app.route('/departments', methods=['GET'])
def get_departments():
    departments = Department.query.all()
    result = []
    for department in departments:
        result.append({
            'id': department.id,
            'name': department.name
        })
    return jsonify(result)

@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get(id)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404
    result = {
        'id': employee.id,
        'first_name': employee.first_name,
        'last_name': employee.last_name
    }
    positions = []
    for position in employee.positions:
        positions.append(position.name)
    result['position'] = positions
    department = Department.query.filter_by(position=positions[0], last_name=employee.last_name).first()
    result['department'] = department.name if department else None
    return jsonify(result)

@app.route('/employees/all', methods=['GET'])
def get_all_employees():
    employees = Employee.query.all()
    result = []
    for employee in employees:
        positions = []
        for position in employee.positions:
            positions.append(position.name)
        department = Department.query.filter_by(position=positions[0], last_name=employee.last_name).first()
        result.append({
            'id': employee.id,
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'position': positions,
            'department': department.name if department else None
        })
    return jsonify(result)

@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    position_id = data.get('position_id')
    department_id = data.get('department_id')

    employee = Employee(first_name=first_name, last_name=last_name)
    db.session.add(employee)
    db.session.commit()

    position = Position.query.get(position_id)
    if not position:
        return jsonify({'error': 'Position not found'}), 404
    position.employee = employee
    db.session.commit()

    department = Department.query.get(department_id)
    if not department:
        return jsonify({'error': 'Department not found'}), 404
    department.position = position.name
    department.last_name = last_name
    db.session.commit()

    return jsonify({'message': 'Employee added successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
