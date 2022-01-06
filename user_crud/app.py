import __main__
from flask import Flask, render_template, request, redirect
from werkzeug.exceptions import abort

from models import db, EmployeeModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')

    if request.method == 'POST':
        employee_id = request.form['employee_id']
        name = request.form['name']
        age = request.form['age']
        position = request.form['position']
        employee = EmployeeModel(employee_id=employee_id, name=name, age=age,
                                 position=position)
        db.session.add(employee)
        db.session.commit()
        return redirect('/data')


@app.route('/data')
def RetrieveList():
    employees = EmployeeModel.query.all()
    return render_template('datalist.html', employees=employees)


@app.route('/data/<int:id>')
def RetrieveEmployee(id_):
    employee = EmployeeModel.query.filter_by(employee_id=id_).first()
    if employee:
        return render_template('data.html', employee=employee)
    return f"Employee with id ={id_} Doenst exist"


@app.route('/data/<int:id>/update', methods=['GET', 'POST'])
def update(id_):
    employee = EmployeeModel.query.filter_by(employee_id=id_).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()
            name = request.form['name']
            age = request.form['age']
            position = request.form['position']
            employee = EmployeeModel(employee_id=id_, name=name, age=age,
                                     position=position)
            db.session.add(employee)
            db.session.commit()
            return redirect(f'/data/{id_}')
        return f"Employee with id = {id_} Does not exist"

    return render_template('update.html', employee=employee)


@app.route('/data/<int:id>/delete', methods=['GET', 'POST'])
def delete(id_):
    employee = EmployeeModel.query.filter_by(employee_id=id_).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()
            return redirect('/data')
        abort(404)

    return render_template('delete.html')


@app.route('/about/')
def about():
    return render_template('text.html')


if __name__ == "__main__":
    app.run()
