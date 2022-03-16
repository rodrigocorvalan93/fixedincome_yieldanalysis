from flask import Blueprint, render_template

views = Blueprint('views', __name__)


#define a view @name view in rute url. en funcion home pongo html-
@views.route('/')
def home():
    return render_template("home.html")