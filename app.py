import os

# Limpiar la consola
os.system('cls' if os.name == 'nt' else 'clear')


#Importa las bibliotecas necesarias:
from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#Crea una credencial para acceder a Firebase:
cred = credentials.Certificate('D:\Workspace_git\Python\pipe_python_crud_flask_firebase\sdk.json')

firebase_admin.initialize_app(cred)
db = firestore.client()

#Crea las rutas para CRUD:
app = Flask(__name__)

@app.route('/')
def index():
    books = []
    docs = db.collection('books').get()
    for doc in docs:
        books.append(doc.to_dict())
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        price = request.form['price']
        db.collection('books').add({
            'title': title,
            'author': author,
            'genre': genre,
            'price': price
        })
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit(id):
    book_ref = db.collection('books').document(id)
    book = book_ref.get().to_dict()
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        price = request.form['price']
        book_ref.update({
            'title': title,
            'author': author,
            'genre': genre,
            'price': price
        })
        return redirect(url_for('index'))
    return render_template('edit.html', book=book)

@app.route('/delete/<string:id>')
def delete(id):
    db.collection('books').document(id).delete()
    return redirect(url_for('index'))


app.run()