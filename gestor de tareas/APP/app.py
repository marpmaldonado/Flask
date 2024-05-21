from flask import Flask,render_template, request,redirect,url_for,session
import mysql.connector
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature


#NOMBRE DE LA APP
app=Flask(__name__)
app.config['SECRET_KEY'] = '123456789'
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
#configurar la conexion a la bbdd
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "gestiontareas"    
)

#CONFIGURAR SERVIDOR DE GMAIL
curso=db.cursor()
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
##CONFIGURAR EL USUARIO CON EL QUE VAMOS A TRABAJAR
app.config['MAIL_USERNAME'] = 'cielopaulis1@gmail.com'
app.config['MAIL_PASSWORD'] = 'jxle ztlf qmho zanu'
app.config['MAIL_USE_TILS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = ('Recupera tu contraseña! :D', 'cielopaulis1@gmail.com')

###CREAR OBJETO PARA LA CONFIGURACION DE LA APP
mail = Mail(app)
def enviar_correo(email):
   ####SE GENERA UN TOKEN PARA EL CORREO
   token = serializer.dumps(email,salt='restablecimiento de contraseña')
   ####SE CREA LA URL
   enlace= url_for('restablecer_contraseña',token=token, _external=True)
   #SE CREA EL MENSAJE DEL CORREO ENVIADO
   mensaje = Message(subject='¡Hola!Restablece tu contraseña',recipients=[email], body=f'Para restablecer contraseña, haz clic en el siguiente enlace:{enlace}')
   mail.send(mensaje)   
@app.route('/restablecer_contraseña/<token>',methods=['GET','POST'])
def restablecer_contraseña(token):
   #####VERIFICAR CORREO DEL TOKEN
   if request.form == 'POST':
      nueva_contraseña = request.form['nueva_contraseña']
      confirmar_contraseña = request.form['confirmar_contraseña']
      ###VERIFICAR QUE LAS CONTRASEÑAS SEAN IGUALES
      if nueva_contraseña != confirmar_contraseña:
         return print('las contraseñas no son iguales')
      passwordnuevo = generate_password_hash(nueva_contraseña)
      #ACTUALIZAR CONTRASEÑA EN LA BASE DE DATOS
      cursor = db.cursor()
      email = serializer.loads(token, salt ='restablecimiento-contrsaseña', max_age=3600)
      query = "UPDATE usuarios SET contraseña = %s WHERE email = %s"
      cursor.execute(query, (passwordnuevo, email))
      db.commit()
      return redirect(url_for('login'))
   return render_template('restablecer_contraseña.html')
####RECUPERAR CONTRASEÑA
@app.route('/recuperar_contraseña', methods=['GET','POST'])
def recuperar_contraseña():
   if request.method == 'POST':
      email = request.form['email']
      enviar_correo(email)
      return redirect(url_for('login'))
   return render_template('recuperar_contraseña.html')

#VERIFICACION DE CREDENCIALES DEACUERDO AL ROL
@app.route('/',methods=['GET','POST'])
def login():   
   usuario = request.form.get('usuario')
   contraseña = request.form.get('contraseña')
   cursor= db.cursor(dictionary=True)
   query = "SELECT usuario, contraseña, rol FROM usuarios WHERE usuario = %s"
   cursor.execute(query,(usuario,))
   usuarios= cursor.fetchone()
   if(usuarios and check_password_hash(usuarios['contraseña'],contraseña)):
      #CREAR LA SESION
      session['usuario']= usuarios['usuario']
      session['rol'] = usuarios['rol']
      if usuarios['rol']== 'admin':
         return redirect(url_for('listar'))
      else:
         return redirect(url_for('listarTar'))
   else:
      print('usuario invalido o credenciales incorrectas')
      return render_template("index.html")
   return render_template('index.html')

 #CERRAR SESION
@app.route('/salir')
def salir():
   session.pop('usuario',None)
   ###EL 'LOGIN' ES EL NOMBRE DE LA FUNCION
   return redirect(url_for('login'))
#FUNCION PARA NO ALMACENAR EL CACHE DE LA PAGINA
@app.after_request
def add_header(response):
   response.headers['Cache-Control'] =  'no-cache,no-store,must-revalidate'
   response.headers['Pragma'] = 'no-cache'
   response.headers['Expires'] = 0
   return response

#RUTA PARA ABRIR LA PAGINA PRINCIPAL DEL ADMINISTRADOR
@app.route('/PrincipalAdmin',methods=['GET','POST'])
def PrincipalAdmin():
   return render_template('PrincipalAdmin.html')
#RUTA PARA ABRIR LA PAGINA PRINCIPAL DEL USUARIO
@app.route('/PrincipalUsu',methods=['GET','POST'])
def PrincipalUsua():
   return render_template('PrincipalUsua.html')

###############################################################
############CONFIGURACION DEL USUARIO##########################
###############################################################

#REGISTRO DE TAREAS DEL USUARIO
@app.route('/RegistroTarUsu',methods=['GET','POST'])
def RegisTarUsu():
   return render_template('RegistroTareasU.html')
#RUTA PARA REGISTRARSE DESDE EL INDEX
@app.route('/Registrarse',methods=['GET','POST'])
def Registrarse():
    if request.method == 'POST':
     nombreusuario = request.form.get('nombre')
     apellido = request.form.get('apellido')
     email = request.form.get('email')
     usuario = request.form.get('usuario')
     contraseña = request.form.get('contraseña')
     rol = request.form.get('rol')
     contraencriptar = generate_password_hash(contraseña)
     #ENCRIPTACIÓN DE CONTRASEÑA
     cursor = db.cursor()
     #VERIFICAR SI YA EXISTE EL USUARIO Y EL EMAIL
     cursor.execute("SELECT * FROM usuarios WHERE usuario=%s OR email=%s",(usuario,email))
     resultado = cursor.fetchone()
     if resultado:
        print("ya existe este usuario o este email ya esta siendo utilizado")
        return render_template('index.html')
     ###INSERTAR USUARIO
     else:
        cursor.execute("INSERT INTO usuarios(nombre,apellido,email,usuario,contraseña,rol) VALUES (%s,%s,%s,%s,%s,%s)",(nombreusuario,apellido,email,usuario,contraencriptar,rol))
        db.commit()
        Warning("datos insertados correctamente")
        return redirect(url_for('Registrarse'))
     ##RENDER TEMPLATE CARGA UNA VISTA DE TIPO HTML
    return render_template('Registrarme.html')

#REGISTRO DE TAREAS USUARIO
@app.route('/RegistroTareasU', methods=['GET', 'POST'])
def RegistrarTareaU():
    if request.method == 'POST':
        nombretarea = request.form.get('nombretar')
        fechaI = request.form.get('fechainicio')
        fechaF = request.form.get('fechafin')
        EstadoTar = request.form.get('estado')        
        if 'usuario' not in session:
            #SI EL USUARIO NO ESTA AUTENTICADO LO REDIRECCIONA LA PAGINA DE INICIO
            return redirect(url_for('login'))           
        Usuario = session['usuario']
        cursor = db.cursor()
        cursor.execute('SELECT idUsuarios FROM usuarios WHERE usuario=%s', (Usuario,))
        usuario = cursor.fetchone()        
        if usuario is None:
            return "Usuario no encontrado en la base de datos"        
        id_usuario = usuario[0]
        cursor.execute('INSERT INTO Tareas (nombretar, fechainicio, fechafin, estado, Id_Usuario1) '
                       'VALUES (%s, %s, %s, %s, %s)', (nombretarea, fechaI, fechaF, EstadoTar, id_usuario))
        db.commit()
        print('Tarea registrada exitosamente')        
    return render_template('RegistroTareasU.html')

#ELIMINAR TAREA DESDE USUARIO
@app.route('/eliminartarusu/<int:idt>',methods=['GET'])
def eliminar_tarea_usuario(idt):
   cursor = db.cursor()
   cursor.execute('DELETE FROM tareas WHERE IDtarea = %s',(idt,))
   db.commit()
   print('tarea eliminado')
   return redirect(url_for('listarTar'))

##
@app.route('/listaTar',methods=['GET','POST'])
def listarTar():
   if 'usuario' in session:
      nombre_usuario = session['usuario']
      cursor = db.cursor()
      cursor.execute('SELECT idUsuarios FROM usuarios WHERE usuario = %s', (nombre_usuario,))
      id_usuario = cursor.fetchone()[0]
      query = 'SELECT * FROM tareas WHERE Id_Usuario1 = %s'
      cursor.execute(query,(id_usuario,))
      lis_tareas = cursor.fetchall()
      return render_template('PrincipalUsua.html',tareas=lis_tareas)


#REGISTRO DE TAREAS DESDE EL USUARIO
@app.route('/RegistroTareas',methods=['GET','POST'])
def RegistrarTarea():
   if request.method == 'POST':
     nombretarea = request.form.get('nombretar')
     fechaI = request.form.get('fechainicio')
     fechaF = request.form.get('fechafin')
     EstadoTar = request.form.get('estado')
     cursor = db.cursor()
     if 'usuario' not in session:
            return redirect(url_for('login'))
      ###REDIRIGIR AL USUARIO AL INICIO DE SESION SI NO ESTA AUTENTICADO
     Usuario = session['usuario']
     cursor = db.cursor()
     cursor.execute('SELECT idUsuarios FROM usuarios WHERE usuario=%s', (Usuario,))
     usuario = cursor.fetchone()
     if usuario is None:
            return "Usuario no encontrado en la base de datos"             
     id_usuario = usuario[0]
     cursor.execute('INSERT INTO Tareas (nombretar, fechainicio, fechafin, estado, Id_Usuario1)''VALUES (%s, %s, %s, %s, %s)', (nombretarea, fechaI, fechaF, EstadoTar, id_usuario))
     db.commit()
     print('REGISTRO EXITOSO DE LA TAREA')
     #EL RENDER TEMPLATE HACE QUE CARGUE UNA VISTA DE TIPO HTML 
   return render_template('RegistroTareas.html')

#CREACION DE RUTA PARA EL FORMULARIO DE REGISTRO DE USUARIOS
@app.route('/RegistroUsuarios',methods=['GET','POST'])
def registrarUsuarios():
    if request.method == 'POST':
     nombreusuario = request.form.get('nombre')
     apellido = request.form.get('apellido')
     email = request.form.get('email')
     usuario = request.form.get('usuario')
     contraseña = request.form.get('contraseña')
     rol = request.form.get('rol')
     #GENERATE_PASSWORD_HASH ENCRIPTA LA CONTRASEÑA
     contraencriptar = generate_password_hash(contraseña)
     cursor = db.cursor()
     #VERIFICA SI EL USUARIO YA EXISTE Y EL EMAIL
     cursor.execute("SELECT * FROM usuarios WHERE usuario=%s OR email=%s",(usuario,email))
     resultado = cursor.fetchone()
     if resultado:
        print("ya existe este usuario o este email ya esta siendo utilizado")
        return render_template('RegistroUsuario.html')
     #INSERTA USUARIOS
     else:
        cursor.execute("INSERT INTO usuarios(nombre,apellido,email,usuario,contraseña,rol) VALUES (%s,%s,%s,%s,%s,%s)",(nombreusuario,apellido,email,usuario,contraencriptar,rol))
        db.commit()
        Warning("DATOS CORRECTAMENTE INGRESADOS")
        return redirect(url_for('registrarUsuarios'))
    return render_template('RegistroUsuario.html')



#ELIMINAR TAREA
@app.route('/eliminartar/<int:idt>',methods=['GET'])
def eliminartar_usuario(idt):
   cursor = db.cursor()
   cursor.execute('DELETE FROM tareas WHERE IDtarea = %s',(idt,))
   db.commit()
   print('tarea eliminado')
   return redirect(url_for('listar'))

#RUTA DE BUSCAR TAREA
@app.route('/buscar_tarea',methods=['POST'])
def buscar_tarea():
   busqueda =request.form.get('busqueda')
   #REALIZAR BUSQUEDA EN LA BASE DE DATOS
   cursor = db.cursor(dictionary=True)
   consulta = "SELECT * FROM tareas WHERE idtar=%s OR nombretar LIKE %s"
   cursor.execute(consulta,(busqueda, f"%busqueda%"))
   tareas= cursor.fetchall()
   return render_template ('resultadobusqueda.html')

#EDITAR TAREAS
   
@app.route('/editar/<int:id>',methods=['GET','POST'])
def editar_tarea(id):    
     if request.method == 'POST':
       nombretar = request.form['nombretar']
       fechainicio = request.form['fechainicio']
       fechatermino = request.form['fechafin']
       estadotar = request.form['estado']

     #ACTUALIZAR LOS DATOS DEL FORMULARIO
       cursor = db.cursor()
       sql = "UPDATE tareas SET nombretar=%s, fechainicio=%s, fechafin=%s, estado=%s WHERE IDtarea=%s"
       cursor.execute(sql,(nombretar,fechainicio,fechatermino,estadotar,id))
       db.commit()
       return redirect(url_for('listar'))
     else:
       cursor = db.cursor()
       cursor.execute('SELECT * FROM tareas WHERE IDtarea = %s',(id,))
       data=cursor.fetchall()
       cursor.close() 
       return render_template('Modaltareas.html', tareas=data[0])




@app.route('/editar/<int:id>',methods=['GET','POST'])
def editar_usuario(id):
   print
if __name__ =='__main__':
    app.run(debug=True)
    app.add_url_rule('/', view_func=login)
 #llama al index.html


 ###############################################################
############CONFIGURACION DEL ADMINISTRADOR##########################
###############################################################


#mostrar usuarios
@app.route('/lista',methods=['GET','POST'])
def listar():
   cursor = db.cursor()
   cursor.execute("SELECT * FROM usuarios")
   usuario = cursor.fetchall()
   cursor.execute("SELECT * FROM tareas")
   ltareas = cursor.fetchall()
   return render_template('PrincipalAdmin.html',usuarios=usuario,tareas=ltareas)

#FUNCION PARA ELIMINAR USUARIOS
@app.route('/eliminar/<int:id>',methods=['GET'])
def eliminar_usuario(id):
   cursor = db.cursor()
   cursor.execute('DELETE FROM tareas WHERE Id_Usuario1 = %s',(id,))
   db.commit()
   cursor.execute('DELETE FROM usuarios WHERE idUsuarios = %s',(id,))
   db.commit()
   print('usuario eliminado')
   return redirect(url_for('listar'))

#EDITAR USUARIOS
@app.route('/actualizar_usuario/<int:id>', methods=["GET","POST"])
def editar_datos_usuario(id):
    
   if request.method == 'POST':
      nombre = request.form['nombre']
      apellido = request.form['apellido']
      email = request.form['email']
      usuario = request.form['usuario']
      contraseña = request.form['contraseña']
      contraencriptar = generate_password_hash(contraseña) 
      rol = request.form['rol']
   #ACTUALIZAR LOS DATOS DEL FORMULARIO
      cursor = db.cursor()
      sql = "UPDATE usuarios SET nombre=%s, apellido=%s, email=%s, usuario=%s, contraseña=%s, rol=%s WHERE idUsuarios=%s"
      cursor.execute(sql,(nombre, apellido, email, usuario, contraencriptar, rol, id))
      db.commit()
      return redirect(url_for('listar'))
   else:
       cursor = db.cursor()
       cursor.execute('SELECT * FROM usuarios WHERE idUsuarios = %s',(id,))
       data=cursor.fetchall()
       cursor.close() 
       return render_template('Modalusuario.html', usuarios=data[0])
   




