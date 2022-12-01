from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configurações do Aplicativo para o Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'moviepython'
app.config['SQLALCHEMY_DATABASE_URI'] = '{SGBD}://{user}:{password}@{server}/{database}'.format(
    SGBD = 'mysql+mysqlconnector',
    user = 'root',
    password = '12345',
    server = 'localhost',
    database = 'bancofilmes'
)
db = SQLAlchemy(app)

# Importando as Views
from views import *

if __name__ == '__main__':
    app.run(debug=True)