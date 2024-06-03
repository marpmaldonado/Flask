from flask import Flask,render_template, request,redirect,url_for,session
import mysql.connector
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_mail import Mail,Message
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature


###############################################################
############CONFIGURACION GENERAL##########################
###############################################################


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
def enviar_correo_restablecimiento(email):
   ####SE GENERA UN TOKEN PARA EL CORREO
   token = serializer.dumps(email,salt='restablecimiento-contraseña')
   ####SE CREA LA URL
   enlace= url_for('restablecer_contraseña',token=token, _external=True)
   #SE CREA EL MENSAJE DEL CORREO ENVIADO
   mensaje = Message(subject='¡Hola!Restablece tu contraseña',recipients=[email], body=f'Para restablecer contraseña, haz clic en el siguiente enlace:{enlace}')
   mail.send(mensaje)

   
@app.route('/restablecer_contraseña/<token>',methods=['GET','POST'])
def restablecer_contraseña(token):
   #verificar correo del token
   
   
   if request.method == 'POST':
      nueva_contraseña = request.form['nueva_contraseña']
      confirmar_contraseña = request.form['confirmar_contraseña']

      if nueva_contraseña != confirmar_contraseña:
         return 'las contraseñas no coinciden. Intentalo de nuevo'
      
      passwordnuevo = generate_password_hash(nueva_contraseña)
      #actualizar contraseña a la base de datos 
      cursor = db.cursor()
      email = serializer.loads(token, salt='restablecimiento-contraseña', max_age=3600)
      query = "UPDATE usuarios SET contraseña = %s WHERE email = %s"
      cursor.execute(query,(passwordnuevo,email))
      db.commit()

      return redirect(url_for('login'))

   return render_template('restablecer_contraseña.html', token=token)

@app.route('/recuperar_contraseña', methods=['GET','POST'])
def recuperar_contraseña():
   if request.method == 'POST':
      email = request.form['email']
      enviar_correo_restablecimiento(email)

      return redirect(url_for('login'))


   return render_template('recuperar_contraseña.html')



cursor = db.cursor()
#crear las url



@app.route('/',methods=['GET','POST'])
def login():
   #verificacion de credenciales de ingreso de acuerdo al rol
   usuario = request.form.get('usuario')
   contraseña = request.form.get('contraseña')


   cursor= db.cursor(dictionary=True)
   query = "SELECT usuario, contraseña, rol FROM usuarios WHERE usuario = %s"
   cursor.execute(query,(usuario,))

   usuarios= cursor.fetchone()
   if(usuarios and check_password_hash(usuarios['contraseña'],contraseña)):
      #crear la sesion
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

 #codigo para cerrar sesion
@app.route('/salir')
def salir():
   session.pop('usuario',None)
   return redirect(url_for('login'))#el login es el nobre de la funcion
#funcion para no almacenar el cache de la pagina
@app.after_request
def add_header(response):
   response.headers['Cache-Control'] =  'no-cache,no-store,must-revalidate'
   response.headers['Pragma'] = 'no-cache'
   response.headers['Expires'] = 0
   return response



#ruta para registrarse desde el index
@app.route('/Registrarse',methods=['GET','POST'])
def Registrarse():
    if request.method == 'POST':
     nombreusuario = request.form.get('nombre')
     apellido = request.form.get('apellido')
     email = request.form.get('email')
     usuario = request.form.get('usuario')
     contraseña = request.form.get('contraseña')
     rol = request.form.get('rol')
     contraencriptar = generate_password_hash(contraseña) #encriptar contraseña
     cursor = db.cursor()
     #verificar si ya existe usuario y email
     cursor.execute("SELECT * FROM usuarios WHERE usuario=%s OR email=%s",(usuario,email))
     resultado = cursor.fetchone()
     if resultado:
        print("ya existe este usuario o este email ya esta siendo utilizado")
        return render_template('index.html')
     #insertar los usuarios
     else:
        cursor.execute("INSERT INTO usuarios(nombre,apellido,email,usuario,contraseña,rol) VALUES (%s,%s,%s,%s,%s,%s)",(nombreusuario,apellido,email,usuario,contraencriptar,rol))
        db.commit()
        Warning("datos insertados correctamente")
        return redirect(url_for('Registrarse'))
    return render_template('Registrarme.html') #render template: carga una vista de tipo html


###############################################################
############CONFIGURACION DEL ADMINISTRADOR##########################
###############################################################




#ruta para abrir la pagina principal de admin
@app.route('/PrincipalAdmin',methods=['GET','POST'])
def PrincipalAdmin():
   return render_template('PrincipalAdmin.html')




@app.route('/RegistroTareasU', methods=['GET', 'POST'])
def RegistrarTareaU():
    if request.method == 'POST':
        nombretarea = request.form.get('nombretar')
        fechaI = request.form.get('fechainicio')
        fechaF = request.form.get('fechafin')
        EstadoTar = request.form.get('estado')
        
        if 'usuario' not in session:
            return redirect(url_for('login'))  # Redirigir al usuario al inicio de sesión si no está autenticado
        
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

#mostrar usuarios
@app.route('/lista',methods=['GET','POST'])
def listar():
   cursor = db.cursor()
   cursor.execute("SELECT * FROM usuarios")
   usuario = cursor.fetchall()
   cursor.execute("SELECT * FROM tareas")
   ltareas = cursor.fetchall()
   return render_template('PrincipalAdmin.html',usuarios=usuario,tareas=ltareas)

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


#crear ruta
@app.route('/RegistroTareas',methods=['GET','POST'])
def RegistrarTarea():
   if request.method == 'POST':
     nombretarea = request.form.get('nombretar')
     fechaI = request.form.get('fechainicio')
     fechaF = request.form.get('fechafin')
     EstadoTar = request.form.get('estado')
     cursor = db.cursor()
     if 'usuario' not in session:
            return redirect(url_for('login'))  # Redirigir al usuario al inicio de sesión si no está autenticado
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
   return render_template('RegistroTareas.html')#render template: carga una vista de tipo html
#crear una ruta para cargar el formulario de registro de usuarios
@app.route('/RegistroUsuarios',methods=['GET','POST'])
def registrarUsuarios():
    if request.method == 'POST':
     nombreusuario = request.form.get('nombre')
     apellido = request.form.get('apellido')
     email = request.form.get('email')
     usuario = request.form.get('usuario')
     contraseña = request.form.get('contraseña')
     rol = request.form.get('rol')
     contraencriptar = generate_password_hash(contraseña) #encriptar contraseña
     cursor = db.cursor()
     #verificar si ya existe usuario y email
     cursor.execute("SELECT * FROM usuarios WHERE usuario=%s OR email=%s",(usuario,email))
     resultado = cursor.fetchone()
     if resultado:
        print("ya existe este usuario o este email ya esta siendo utilizado")
        return render_template('RegistroUsuario.html')
     #insertar los usuarios
     else:
        cursor.execute("INSERT INTO usuarios(nombre,apellido,email,usuario,contraseña,rol) VALUES (%s,%s,%s,%s,%s,%s)",(nombreusuario,apellido,email,usuario,contraencriptar,rol))
        db.commit()
        Warning("datos insertados correctamente")
        return redirect(url_for('registrarUsuarios'))
    return render_template('RegistroUsuario.html') #render template: carga una vista de tipo html
#corre el archivo

#funcion para eliminar usuario
@app.route('/eliminar/<int:id>',methods=['GET'])
def eliminar_usuario(id):
   cursor = db.cursor()
   cursor.execute('DELETE FROM tareas WHERE Id_Usuario1 = %s',(id,))
   db.commit()
   cursor.execute('DELETE FROM usuarios WHERE idUsuarios = %s',(id,))
   db.commit()
   print('usuario eliminado')
   return redirect(url_for('listar'))

#Eliminar tarea desde admin
@app.route('/eliminartar/<int:idt>',methods=['GET'])
def eliminartar_usuario(idt):
   cursor = db.cursor()
   cursor.execute('DELETE FROM tareas WHERE IDtarea = %s',(idt,))
   db.commit()
   print('tarea eliminado')
   return redirect(url_for('listar'))

#Eliminar tarea desde usuario

@app.route('/eliminartarusu/<int:idt>',methods=['GET'])
def eliminar_tarea_usuario(idt):
   cursor = db.cursor()
   cursor.execute('DELETE FROM tareas WHERE IDtarea = %s',(idt,))
   db.commit()
   print('tarea eliminada')
   return redirect(url_for('listarTar'))

@app.route('/buscar_tarea', methods=['POST'])
def buscar_tarea():
   busqueda = request.form.get('busqueda')
   # Realizar la busqueda en la bbdd

   cursor = db.cursor(dictionary=True)
   consulta = "SELECT * FROM tareas WHERE IDtarea= %s OR nombretar LIKE %s"
   cursor.execute(consulta,(busqueda,"%"+ busqueda +"%"))
   tareas= cursor.fetchall()

   return render_template('Resultadobusqueda.html', tareas=tareas, busqueda=busqueda)

@app.route('/buscar_usuario', methods=['POST'])
def buscar_usuario():
   busqueda = request.form.get('busqueda')
   # Realizar la busqueda en la bbdd

   cursor = db.cursor(dictionary=True)
   consulta = "SELECT * FROM usuarios WHERE idUsuarios= %s OR nombre LIKE %s"
   cursor.execute(consulta,(busqueda,"%"+ busqueda +"%"))
   usuario= cursor.fetchall()

   return render_template('Resultadobusquedausuario.html', usuarios=usuario, busqueda=busqueda)





#Editar tarea desde admin
@app.route('/editar/<int:id>',methods=['GET','POST'])
def editar_tarea(id):
     
     
     if request.method == 'POST':
       nombretar = request.form['nombretar']
       fechainicio = request.form['fechainicio']
       fechatermino = request.form['fechafin']
       estadotar = request.form['estado']

     #actualizar los datos del formulario
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
     


       
      
#EDITAR USUARIOS
@app.route('/actualizar_usuario/<int:id>', methods=["GET","POST"])
def editar_datos_usuario(id):
    
   if request.method == 'POST':
      nombre = request.form['nombre']
      apellido = request.form['apellido']
      email = request.form['email']
      usuario = request.form['usuario']
      contraseña = request.form['contraseña']
      contraencriptar = generate_password_hash(contraseña) #encriptar contraseña
      rol = request.form['rol']
   #actualizar los datos del formulario
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

@app.route('/editar/<int:id>',methods=['GET','POST'])
def editar_usuario(id):
   print
if __name__ =='__main__':
    app.run(debug=True)#correr en funcion de bugeo
    app.add_url_rule('/', view_func=login)
 #llama al index.html

 

 ###############################################################
############CONFIGURACION DEL USUARIO##########################
###############################################################

 #ruta para abrir la principal de usuario
@app.route('/PrincipalUsu',methods=['GET','POST'])
def PrincipalUsua():
   return render_template('PrincipalUsua.html')

@app.route('/RegistroTarUsu',methods=['GET','POST'])
def RegisTarUsu():
   return render_template('RegistroTareasU.html')


#Editar tarea desde usuario
@app.route('/editardesusu/<int:id>',methods=['GET','POST'])
def editar_tarea_usuario(id):
     
     
     if request.method == 'POST':
       nombretar = request.form['nombretar']
       fechainicio = request.form['fechainicio']
       fechatermino = request.form['fechafin']
       estadotar = request.form['estado']

     #actualizar los datos del formulario
       cursor = db.cursor()
       sql = "UPDATE tareas SET nombretar=%s, fechainicio=%s, fechafin=%s, estado=%s WHERE IDtarea=%s"
       cursor.execute(sql,(nombretar,fechainicio,fechatermino,estadotar,id))
       db.commit()
       return redirect(url_for('listarTar'))
     else:
       cursor = db.cursor()
       cursor.execute('SELECT * FROM tareas WHERE IDtarea = %s',(id,))
       data=cursor.fetchall()
       cursor.close() 
       return render_template('Modaltareas.html', tareas=data[0])

