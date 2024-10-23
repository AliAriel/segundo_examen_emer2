from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.permanent_session_lifetime = timedelta(days=1)

@app.route('/')
def index():
    products = session.get('products', [])
    return render_template('index.html', products=products)

@app.route('/new_product', methods=['GET', 'POST'])
def new_product():
    if request.method == 'POST':
        product = {
            'id': request.form['id'],
            'nombre': request.form['nombre'],
            'cantidad': request.form['cantidad'],
            'precio': request.form['precio'],
            'fecha_vencimiento': request.form['fecha_vencimiento'],
            'categoria': request.form['categoria']
        }
        if 'products' not in session:
            session['products'] = []
        session['products'].append(product)
        session.modified = True
        return redirect(url_for('index'))
    return render_template('new_product.html')

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    products = session.get('products', [])
    product = next((item for item in products if item['id'] == str(product_id)), None)
    
    if request.method == 'POST':
        if product:
            product['nombre'] = request.form['nombre']
            product['cantidad'] = request.form['cantidad']
            product['precio'] = request.form['precio']
            product['fecha_vencimiento'] = request.form['fecha_vencimiento']
            product['categoria'] = request.form['categoria']
            session['products'] = products
            session.modified = True
        return redirect(url_for('index'))
    
    return render_template('edit_product.html', product=product)

@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    products = session.get('products', [])
    product_to_delete = next((item for item in products if item['id'] == str(product_id)), None)
    
    if product_to_delete:
        products.remove(product_to_delete)
        session['products'] = products
        session.modified = True
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
