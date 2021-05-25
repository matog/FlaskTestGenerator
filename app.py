from flask import Flask, render_template, request, redirect, flash, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import DataRequired, Email, InputRequired
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import random
import os

# Definimos base de datos
dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "Mi clave super secreta"
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)

## DEFINICION DEL MODELO
# Creamos tabla accesoria que vincule test y question
preg = db.Table('preg',
    db.Column('test_id', db.Integer, db.ForeignKey('test.test_id')),
    db.Column('question_id', db.Integer, db.ForeignKey('question.question_id'))
    )

class Test(db.Model):
    test_id = db.Column(db.Integer, primary_key = True)
    month = db.Column(db.String(50), nullable = False)
    preguntas  = db.relationship('Question', secondary =preg, backref=db.backref('preguntas', lazy='dynamic'))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key= True)
    question_text = db.Column(db.String(20))
    question_option1 = db.Column(db.Integer, nullable = False)
    question_option2 = db.Column(db.Integer, nullable = False)
    question_option3 = db.Column(db.Integer, nullable = False)
    question_option4 = db.Column(db.Integer, nullable = False)
    question_ok = db.Column(db.Integer, nullable = False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True)
    password = db.Column(db.String(80))

## USUARIOS, LOGIN y LOGOUT
# Ruta para gestionar usuarios
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/create_user/<string:user>")
def create_user(user):
    password = generate_password_hash(user, method = "sha256")
    new_user = User(username = user, password = password)
    db.session.add(new_user)
    db.session.commit()
    return(password)

# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = User.query.filter_by(username = request.form["username"]).first()
        stored_password = user.password
        result = check_password_hash(stored_password, request.form["password"])
        if request.form["username"] != user.username or result == False:
            error = 'Invalid Credentials. Please try again.'
        else:
            login_user(user)
            return redirect(url_for('show'))
    return render_template('login.html', error=error)

# Ruta de logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "Logged out!"

## EXAMENES
# Ruta para mostrar un examen
@app.route("/test/<int:id>")
@login_required
def show_test(id):
    test = Test.query.with_entities(Test).get(id)
    mes = test.month
    pregunta = Question.query.filter(Question.preguntas.any(test_id=test.test_id)).all()
    return render_template("show_test.html", pregunta = pregunta, test = test, mes = mes)

# Ruta para listar todos los examenes
@app.route("/")
@app.route("/test/")
@login_required
def show():
    test = Test.query.with_entities(Test).all()
    return render_template("show.html", test = test)

# Ruta para generar examenes
@app.route("/test/gen", methods = ["GET","POST"])
@login_required
def gen_test():
    if request.method == "POST":
        try:
            # Generamos las preguntas para el examenes
            # Primero obtenemos la query de los id
            result = Question.query.with_entities(Question.question_id).all()
            preguntas_id = [r for r, in result] # Las pasamos a un a lista
            # Ponemos en cero la lista y el contador
            pregunta_elegida=[]
            count = 0
            # Obtenemos al azar 4 preguntas.
            # Primero pasamos la cantidad de de preguntas que hay en la base
            while (count < 4):
                longitud = len(preguntas_id)
                # Rand es un numero aleatorio, en el rango de la cantidad de preguntas
                rand = random.randrange(0, len(preguntas_id)-1)
                # Obtenemos el Id de la pregunta del número aleatorio generado
                row = Question.query.with_entities(Question.question_id).all()[rand]
                # chequeamos que no se repita
                if row not in pregunta_elegida:
                    pregunta_elegida.append(row)
                    count = count + 1
            pregunta_elegida = [r for r, in pregunta_elegida] # Pasamos a lista
            #  Cargamos en la base el llamado
            month = request.form["llamado"]
            new_test = Test(month = month)
            db.session.add(new_test)
            db.session.commit()
            # Pasamos los ID de las preguntas elegidas a la base
            for question in pregunta_elegida:
                # new_question = Question.query.filter_by(Question.question_id == question).first()
                new_question = db.session.query(Question).get(question)
                # new_question = result[question]
                new_question.preguntas.append(new_test)
                db.session.commit()
            flash("Examen generado exitosamente", "alert alert-success")
            return redirect(url_for("show"))
        except Exception as e:
            flash("Something went wrong...","alert alert-danger")
            return ("ERROR")
    return render_template("gen.html", date = datetime.utcnow())

# Ruta para agregar PreguntaMC
@app.route("/question/add", methods = ["GET","POST"])
@login_required
def add_question():
    if request.method == "POST":
        try:
            question = request.form["question"]
            option1 = request.form["option1"]
            option2 = request.form["option2"]
            option3 = request.form["option3"]
            option4 = request.form["option4"]
            correct = request.form["correct"]
            # created_on = datetime.utcnow()
            new_question = Question(question_text = question,
                                    question_option1 = option1,
                                    question_option2 = option2,
                                    question_option3 = option3,
                                    question_option4 = option4,
                                    question_ok = correct,
                                    )
            db.session.add(new_question)
            db.session.commit()
            flash("Pregunta agregada exitosamente", "alert alert-success")
            return redirect(url_for("question_list"))
        except Exception as e:
            flash("Something went wrong...","alert alert-danger")
            return ("ERROR")
    return render_template("add.html", date = datetime.utcnow())

# Listado de preguntas
@app.route("/question/list")
@login_required
def question_list():
    question = Question.query.order_by(desc(Question.created_on)).all()
    return render_template("list_question.html", question=question)

#  Borra examen (también de la tabla 'preg')
@app.route("/delete/<int:id>")
@login_required
def delete_test(id):
    try:
        test = Test.query.with_entities(Test).get(id)
        db.session.delete(test)
        db.session.commit()
        flash("Examen eliminado exitosamente", "alert alert-success")
        return redirect(url_for("show"))
    except Exception as e:
        flash("Something went wrong...","alert alert-danger")
        return redirect(url_for("show"))

# Borra Pregunta
@app.route("/delete_question/<int:id>")
@login_required
def delete_question(id):
    try:
        question = Question.query.with_entities(Question).get(id)
        db.session.delete(question)
        db.session.commit()
        flash("Pregunta eliminada exitosamente", "alert alert-success")
        return redirect(url_for("question_list"))
    except Exception as e:
        flash("Something went wrong...","alert alert-danger")
        return redirect(url_for("question_list"))

@app.route("/question/update",methods=["POST"])
@login_required
def update():
    try:
        question_id = request.form["id"]
        question = Question.query.filter_by(question_id=question_id).one()
        question.question_text = request.form["question_text"]
        question.question_option1 = request.form["question_option1"]
        question.question_option2 = request.form["question_option2"]
        question.question_option3 = request.form["question_option3"]
        question.question_option4 = request.form["question_option4"]
        question.question_ok = request.form["question_ok"]
        db.session.commit()
        flash("Pregunta actualizada exitosamente", "alert alert-success")
        return redirect(url_for("question_list"))
    except Exception as e:
        flash("Something went wrong...","alert alert-danger")
        # return render_template("update0.html", id=id)
        return redirect(url_for("question_list"))

@app.route("/question/update/<int:id>")
@login_required
def update_question(id):
    question = Question.query.filter_by(question_id=id).one()
    return render_template("update.html", question=question)

@app.route("/db/create")
def index():
    db.create_all()
    return "GOL"

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
