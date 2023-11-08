from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson import ObjectId  # Importe ObjectId corretamente

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017')  # Corrigido o nome da classe
db = client.veiculo
carros = db.veiculo

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/listar")
def listar():
    tcarros = carros.find()
    return render_template("listar.html",lcarro = tcarros)
    
#cadastrar
@app.route("/cadastrar")
def insere_veiculo():
    return render_template("cadastrar.html")

@app.route("/cadastrar_bd", methods=["POST"])
def cadastrar():
    carro = {
        'urlimg': request.form['urlimg'],
        'carro': request.form['carro'],
        'marca': request.form['marca'],
        'ano': request.form['ano'],
        'preco': request.form['preco'],
         
    }
    carros.insert_one(carro)
    return redirect("listar")

#fim cadastrar

@app.route("/editar/<string:veiculo_id>")
def editar_veiculo(veiculo_id):
    veiculo = carros.find_one({'_id': ObjectId(veiculo_id)})  # Importe o ObjectId da pymongo
    return render_template("editar.html", veiculo=veiculo)


@app.route("/atualizar/<string:veiculo_id>", methods=["POST"])
def atualizar(veiculo_id):
    carro = {
        'urlimg': request.form['urlimg'],
        'carro': request.form['carro'],
        'marca': request.form['marca'],
        'ano': request.form['ano'],
        'preco': request.form['preco'],
    }
    
    carros.update_one({'_id': ObjectId(veiculo_id)}, {'$set': carro})
    
    return redirect("/listar")  # Redirecionar para a página de listagem após a atualização


@app.route("/excluir/<string:veiculo_id>")
def excluir(veiculo_id):
    # Certifique-se de confirmar a exclusão com um pop-up de confirmação ou um token seguro antes de realizar a exclusão.
    # Para simplificar, aqui estamos excluindo diretamente sem confirmação.

    carros.delete_one({'_id': ObjectId(veiculo_id)})
    
    return redirect("/listar")  # Redirecionar para a página de listagem após a exclusão



@app.route("/contato")
def contato():
    return ("<h1>Contato</h1>")

if __name__ == '__main__':
    app.run(debug=True)