from flask import Flask, redirect, render_template, request, send_from_directory
from werkzeug.exceptions import abort

from models import ProductModel, db
from user_crud.generate_IDs import generate_id

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
        if request.form['btn_identifier'] == 'newInput':
            product_id = generate_id()
            product_name = request.form['product_name']
            quant = request.form['quantity']
            category = request.form['product_category']
            if product_name and quant and category:
                product = ProductModel(product_id=product_id,
                                       product_name=product_name,
                                       quantity=quant,
                                       product_category=category)
                csv_row = f"{product_name}, {quant}, {category}, {product_id}\n"
                with open('product_info.csv', 'a') as fd:
                    fd.write(csv_row)
                db.session.add(product)
                db.session.commit()
                return redirect('/data')
            else:
                return redirect('/error-h')
        if request.form['btn_identifier'] == 'showData':
            return redirect('/data')


@app.route('/data', methods=['GET', 'POST'])
def RetrieveList():
    if request.method == 'GET':
        products = ProductModel.query.all()
        return render_template('datalist.html', products=products)
    if request.method == 'POST':
        if request.form["btn_identifier"] == 'home':
            return redirect('/')
        if request.form["btn_identifier"] == "edit":
            return redirect(f'/data/{request.form["id"]}/update')
        if request.form["btn_identifier"] == "delete":
            return redirect(f'/data/{request.form["id"]}/delete')


@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory='/user_crud',
                               filename=filename)


@app.route('/data/<int:id_>/update', methods=['GET', 'POST'])
def update(id_):
    product = ProductModel.query.filter_by(product_id=id_).first()
    if request.method == 'POST':
        if request.form["btn_identifier"] == 'back':
            return redirect('/data')
        if request.form["btn_identifier"] == 'submit' and product:
            db.session.delete(product)
            db.session.commit()
            product_name = request.form['product_name']
            quant = request.form['quantity']
            category = request.form['product_category']
            product = ProductModel(product_id=id_, product_name=product_name,
                                   quantity=quant,
                                   product_category=category)
            if id_ and product_name and quant and category:
                db.session.add(product)
                db.session.commit()
                return redirect('/data')
            else:
                return redirect(f'/error-e/{id_}')
    return render_template('update.html', product=product)


@app.route('/data/<int:id_>/delete', methods=['GET', 'POST'])
def delete(id_):
    product = ProductModel.query.filter_by(product_id=id_).first()
    if request.method == 'POST':
        if request.form["btn_identifier"] == "cancel":
            return redirect('/data')
        if request.form["btn_identifier"] == "delete" and product:
            db.session.delete(product)
            db.session.commit()
            return redirect('/data')
        abort(404)

    return render_template('delete.html')


@app.route('/about/', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        return redirect('/')
    return render_template('text.html')


@app.route('/error-h', methods=['GET', 'POST'])
def error1():
    if request.method == 'POST':
        return redirect('/')
    return render_template('error_home.html')


@app.route('/error-e/<int:id_>', methods=['GET', 'POST'])
def error2(id_):
    if request.method == 'POST':
        return redirect(f'/data/{id_}/update')
    return render_template('error_edit.html')


if __name__ == "__main__":
    app.run()
