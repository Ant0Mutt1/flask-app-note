from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import re

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        usuario = User.query.filter_by(email=email).first()
        if usuario:
            if check_password_hash(usuario.password, password):
                flash('La contraseña es correcta', category='success')
                login_user(usuario, remember = True)
                return redirect(url_for('views.home'))
            else:
                flash('la contraseña no es correcta', category='error')

        else:
            flash('El email no está registrado', category='error')
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name  = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        usuario = User.query.filter_by(email=email).first()

        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        email_regex = re.compile(email_pattern)

        if usuario:
            flash('Este email ya está registrado', category='error')
        elif not bool(email_regex.match(email)):
            flash('Ingresa una dirección de mail válida', category='error')
        elif len(name)<6:
            flash('El nombre debe ser mayor a 6 caracteres', category='error')
        elif password1 != password2:
            flash('La contraseña ingresada no coincide', category='error')
        elif len(password1)<8:
            flash('La contraseña debe tener más de 8 caracteres', category='error')

        else:
            nuevo_usuario = User(email=email, 
                                 name=name,
                                 password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('la cuanta se creo exitosamente', category='success')
            
            login_user(usuario, remember = True)
            return redirect(url_for('views.home'))
    return render_template('sign_up.html', user=current_user)