import os

from flask import Flask, current_app, render_template, request, redirect, \
    send_file, send_from_directory
from werkzeug.exceptions import abort

from models import db, ProductModel

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
            product_id = request.form['product_id']
            product_name = request.form['product_name']
            quant = request.form['quantity']
            category = request.form['product_category']
            product = ProductModel(product_id=product_id,
                                   product_name=product_name,
                                   quantity=quant,
                                   product_category=category)
            csv_row = f"{product_name}, {quant}, {category}, {product_id}"
            with open('product_info.csv', 'a') as fd:
                fd.write(csv_row)
            db.session.add(product)
            db.session.commit()
            return redirect('/data')
        if request.form['btn_identifier'] == 'showData':
            return redirect('/data')
        if request.form['btn_identifier'] == 'getCSV':
            return redirect('/download')


@app.route('/data', methods=['GET', 'POST'])
def RetrieveList():
    if request.method == 'GET':
        products = ProductModel.query.all()
        return render_template('datalist.html', products=products)
    if request.method == 'POST':
        return redirect('/')


@app.route('/data/<int:id>')
def RetrieveProduct(id_):
    product = ProductModel.query.filter_b(product_id=id_).first()
    if product:
        return render_template('data.html', product=product)
    return f"Product with id ={id_} Doesnt exist"


@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    # Appending app path to upload folder path within app root folder
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    # Returning file from appended path
    return send_from_directory(directory=uploads, filename=filename)


@app.route('/data/<int:id>/update', methods=['GET', 'POST'])
def update(id_):
    product = ProductModel.query.filter_by(product_id=id_).first()
    if request.method == 'POST':
        if product:
            db.session.delete(product)
            db.session.commit()
            product_name = request.form['product_name']
            quant = request.form['quantity']
            category = request.form['product_category']
            product = ProductModel(product_id=id_, product_name=product_name,
                                   quantity=quant,
                                   product_category=category)
            db.session.add(product)
            db.session.commit()
            return redirect(f'/data/{id_}')
        return f"Product with id = {id_} Does not exist"

    return render_template('update.html', product=product)


@app.route('/data/<int:id>/delete', methods=['GET', 'POST'])
def delete(id_):
    product = ProductModel.query.filter_b(product_id=id_).first()
    if request.method == 'POST':
        if product:
            db.session.delete(product)
            db.session.commit()
            return redirect('/data')
        abort(404)

    return render_template('delete.html')


@app.route('/about/')
def about():
    return render_template('text.html')


if __name__ == "__main__":
    app.run()
