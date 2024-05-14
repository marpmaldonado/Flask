from flask import Flask
from app import db #el pbjeto que se creo en app.py
import datetime
#no se pa que  sirve esta monda pero esta bien pq no da errores
class Tareas(db.Model):
    id = db.Column(db.Integer, Primary_key=True)
    nombretar = db.Column(db.String(200), nullable=False)
    fechainicio = db.Column(db.DateTime,default=datetime.utcnow)
    fechafin = db.Column(db.DateTime)
    estado = db.Column(db.String(20,default='por asignar'))
    

class Usuario(db.Model):
    id = db.Column(db.Integer, Primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    apellido = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    usuario = db.Column(db.String(255), nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20, default='usuario'))