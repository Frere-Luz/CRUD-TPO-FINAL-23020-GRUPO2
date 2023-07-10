from flask import Flask ,jsonify ,request

from flask_cors import CORS       
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app=Flask(__name__)  
CORS(app) 
#CORS(
#    app, supports_credentials=True, origins="*"
#)  
# modulo cors es para que me permita acceder desde el frontend al backend
# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://luzf:1234root@luzf.mysql.pythonanywhere-services.com/luzf$personaldb'
#'mysql+pymysql://luzf:1234root@luzf.mysql.pythonanywhere-services.com/luzf$personaldb'                     
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow


# defino la tabla de Empleados y sus campos
class Empleado(db.Model):       
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(100))
    apellido=db.Column(db.String(100))
    puesto=db.Column(db.String(100))
    sueldo=db.Column(db.Integer)
    imagen=db.Column(db.String(400))

#creo el constructor de la tabla Empleados

    def __init__(self,nombre,apellido,puesto,sueldo,imagen):    
                                                               
        self.nombre=nombre   
        self.apellido=apellido
        self.puesto=puesto
        self.sueldo=sueldo
        self.imagen=imagen

#defino la tabla de Login

class User (db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(50))
    password=db.Column(db.Integer(50))


#crea el constructor de la tabla de Login

    def __init__(self, username, password):
        self.username=username
        self.password=password

    def is_authenticated(self):
        return True      

    def is_anonymous(self):
        return False          

  #  def get_id(self):         
  #      return str(self.id)



#crea todas las tablas


with app.app_context():
    db.create_all()  


#  ************************************************************

#arma los objetos Marshmallow con los campos indicados para Empleado y User
class EmpleadoSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','apellido','puesto','sueldo','imagen')


empleado_schema=EmpleadoSchema()            
empleados_schema=EmpleadoSchema(many=True)  

class UserSchema (ma.Schema):
    class Meta:
        fields=('id', 'username', 'password')

user_schema=UserSchema() #para un usuario
users_schema=UserSchema(many=True) #para muchos usuarios

#------------endpoints/rutas/decoradores------------------------------

#endpoints/rutas empleados

@app.route('/empleados',methods=['GET'])
def get_Empleados():
    all_empleados=Empleado.query.all()           # busca a TODOS los registros
    result=empleados_schema.dump(all_empleados)  # 
                                                 # trae todos los registros de la tabla
    return jsonify(result)                       # retorna un JSON de todos los registros de la tabla


@app.route('/empleados/<id>',methods=['GET'])
def get_empleado(id):
    empleado=Empleado.query.get(id)
    return empleado_schema.jsonify(empleado)   # retorna el JSON de UN empleado recibido como parametro



@app.route('/empleados/<id>',methods=['DELETE'])
def delete_empleado(id):
    empleado=Empleado.query.get(id)             #busca UN registro por ID
    db.session.delete(empleado)                 #borra dicho registro
    db.session.commit()
    return empleado_schema.jsonify(empleado)   # me devuelve un json con el registro eliminado


@app.route('/empleados', methods=['POST']) # crea ruta o endpoint
def create_empleado():
     
    nombre=request.json['nombre']           # request.json --> los datos que envio el cliente
    apellido=request.json['apellido']
    puesto=request.json['puesto']
    sueldo=request.json['sueldo']
    imagen=request.json['imagen']
    new_empleado=Empleado(nombre,apellido,puesto,sueldo,imagen)
    db.session.add(new_empleado)
    db.session.commit()
    return empleado_schema.jsonify(new_empleado) #arma el nuevo registro


@app.route('/empleados/<id>' ,methods=['PUT'])
def update_empleado(id):
    empleado=Empleado.query.get(id)             #realiza una modificacion por ID de un registro
 
    nombre=request.json['nombre']
    apellido=request.json['apellido']
    puesto=request.json['puesto']
    sueldo=request.json['sueldo']
    imagen=request.json['imagen']


    empleado.nombre=nombre
    empleado.apellido=apellido
    empleado.puesto=puesto
    empleado.sueldo=sueldo
    empleado.imagen=imagen


    db.session.commit()
    return empleado_schema.jsonify(empleado)    #devuelve el regigstro modificado
 

#--------------------------------------------------------------------------

#endpoints/rutas users

@app.route('/users/<id>',methods=['GET'])       #busca por ID a UN usuario
def user(id):
    user=User.query.get(id)
    return user_schema.jsonify(user)  
    
@app.route('/users',methods=['GET'])
def get_User():
    all_users=User.query.all()           # busca a TODOS los registros
    result=users_schema.dump(all_users)  # trae todos los registros de la tabla
    return jsonify(result)               # retorna un JSON de todos los registros de la tabla

@app.route('/users/<id>',methods=['DELETE'])    #borra un usuario por ID
def delete_user(id):
    user=User.query.get(id)
    db.session.delete(user)                     #lo retira
    db.session.commit()                         #aplica los cambios
    return user_schema.jsonify(user)            #devuelve el usuario quitado como json


@app.route('/users', methods=['POST'])         #crea el usuario nuevo
def create_user():
    username=request.json['username']
    password=request.json['password']    
    new_user=User(username,password)
    db.session.add(new_user)                    #lo agrega a la base
    db.session.commit()                         #lo guarda
    return user_schema.jsonify(new_user)        #lo devuelve como json


@app.route('/users/<id>' ,methods=['PUT'])      #modifica los datos de un usuario
def update_user(id):                            #busca por id
    user=User.query.get(id)
 
    username=request.json['username']           #revisa los datos
    password=request.json['password']
    
    user.username=username                      #verifica los cambios
    user.password=password
    
    db.session.commit()                         #guarda los cambios
    return user_schema.jsonify(user)            #los devuelve como json







# programa principal *******************************
if __name__=='__main__':  
    app.run(debug=True, port=5000)    # ejecuta el servidor Flask en el puerto 5000