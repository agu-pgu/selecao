from flask import Flask, Response, request, render_template
from core.entities.conductor import Conductor
from core.entities.vehicle import Vehicle
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json



app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://bb70a0130dbc04:f3140c45@us-cdbr-east-04.cleardb.com/heroku_b8e8dcc210fc9f8'
db = SQLAlchemy(app)

#read
@app.route("/conductor/read", methods=["GET"])
def read_conductor_page(id):
    conductor_object = Conductor.query.filter_by(id=id).first()
    conductor_json = conductor_object.to_json()

    return response(200, "condutor", conductor_json)

@app.route("/vehicle/read", methods=["GET"])
def read_vehicle_page(id):
    vehicle_object = Vehicle.query.filter_by(id=id).first()
    vehicle_json = vehicle_object.to_json()

    return response(200, "veículo", vehicle_json)

#create
@app.route('/conductor/create', methods=["POST","GET"])
def create_conductor_page():
    if request.method == 'GET':
        return render_template("create_conductor_page.html")
    else:
        return (request.form['name']['telephone']['cnh']['email'])

@app.route('/vehicle/create', methods=["POST","GET"])
def create_vehicle_page():
    if request.method == 'GET':
        return render_template("create_vehicle_page.html")
    else:
        return (request.form['year']['model-year']['model']['manufacturer']['renvan'])

#update
@app.route("/conductor/update", methods=["PUT"])
def update_conductor_page(id):
    conductor_object = Conductor.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if('name' in body):
            conductor_object.name = body['name']
        if('telephone' in body):
            conductor_object.telephone = body['telephone']
        if('cnh' in body):
            conductor_object.cnh = body['cnh']
        if('email' in body):
            conductor_object.email = body['email']
        
        db.session.add(conductor_object)
        db.session.commit()

        return response(200, "condutor", conductor_object.to_json(), "Atualizado com sucesso")
    except Exception as e:
        print('Erro', e)
        return response(400, "condutor", {}, "Erro ao atualizar")

@app.route("/vehicle/update", methods=["PUT"])
def update_vehicle_page(id):
    vehicle_object = Vehicle.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if('nome' in body):
            vehicle_object.year = body['year']
        if('email' in body):
            vehicle_object.model_year = body['model_year']
        if('email' in body):
            vehicle_object.model = body['model']
        if('email' in body):
            vehicle_object.manufacturer = body['manufacturer']
        if('nome' in body):
            vehicle_object.renavan= body['renavan']
        
        db.session.add(vehicle_object)
        db.session.commit()
        return response(200, "veículo", vehicle_object.to_json(), "Atualizado com sucesso")
    except Exception as e:
        print('Erro', e)
        return response(400, "veículo", {}, "Erro ao atualizar")        
#delete
@app.route("/conductor/delete", methods=["DELETE"])
def delete_conductor_page(id):
    conductor_object = Conductor.query.filter_by(id=id).first()

    try:
        db.session.delete(conductor_object)
        db.session.commit()
        return response(200, "condutor", conductor_object.to_json(), "Deletado com sucesso")
    except Exception as e:
        print('Erro', e)
        return response(400, "condutor", {}, "Erro ao deletar")


@app.route("/veículo/delete", methods=["DELETE"])
def delete_vehicle_page(id):
    vehicle_object = Vehicle.query.filter_by(id=id).first()

    try:
        db.session.delete(vehicle_object)
        db.session.commit()
        return response(200, "veículo", vehicle_object.to_json(), "Deletado com sucesso")
    except Exception as e:
        print('Erro', e)
        return response(400, "veículo", {}, "Erro ao deletar")





def response(status, name_of_content, content, message=False):
    body = {}
    body[name_of_content] = content

    if(message):
        body["message"] = message

    return Response(json.dumps(body), status=status, mimetype="application/json")


if __name__ == "__main__":
    app.run("localhost", 3000)