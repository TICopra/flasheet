import os
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import pandas as pd
from . import db
from .models import User
from .forms import LoginForm, UploadForm
from .models import Upload


main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("main.dashboard"))
        flash("Usuário ou senha inválidos.")
    return render_template("login.html", form=form)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))

@main.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = UploadForm()
    data = None

    if form.validate_on_submit():
        # Obtem o arquivo
        file = form.file.data
        original_filename = secure_filename(file.filename)
        extension = original_filename.rsplit(".", 1)[-1].lower()

        # ✅ Verifica a extensão permitida
        if extension not in ["xls", "xlsx"]:
            flash("Tipo de arquivo não suportado. Envie .xls ou .xlsx")
            return redirect(request.url)

        # Monta o caminho da pasta do usuário
        user_folder = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            f"user_{current_user.id}",
            form.layout.data,
            form.periodo.data
        )
        os.makedirs(user_folder, exist_ok=True)

        # 🔁 Renomeia o arquivo para: nome_id-usuario_(tipo-layout).xlsx
        nome_base = os.path.splitext(original_filename)[0]
        new_filename = f"{nome_base}_{current_user.id}-{current_user.username}_({form.layout.data}).{extension}"
        save_path = os.path.join(user_folder, new_filename)

        # Salva o arquivo
        file.save(save_path)
        flash("Arquivo enviado com sucesso!")
        upload = Upload(
            original_filename=original_filename,
            saved_filename=new_filename,
            filepath=save_path,
            layout=form.layout.data,
            periodo=form.periodo.data,
            user_id=current_user.id
            )
        db.session.add(upload)
        db.session.commit()

        # Tenta ler a planilha
        try:
            df = pd.read_excel(save_path)
            data = df.head(20).to_html(classes='table table-striped text-end', index=False)
        except Exception as e:
            flash(f"Erro ao ler a planilha: {e}")

    return render_template("dashboard.html", form=form, data=data)