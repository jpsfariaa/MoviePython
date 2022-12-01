from iniciar_app import db

# Criando Classes para as Tabelas (SQL Alchemy)
class Filmes(db.Model):
    id_filme = db.Column(db.Integer, primary_key=True, autoincrement = True)
    nome_filme = db.Column(db.String(100))
    data_lancamento = db.Column(db.Date, nullable = False)
    nome_diretor = db.Column(db.String(100))
    nome_ator = db.Column(db.String(100))

    # Gerar uma String "Printável"
    def __repr__(self):
        return self.name

class Plataformas(db.Model):
    id_plataforma = db.Column(db.Integer, primary_key=True, autoincrement = True)
    nome_plataforma = db.Column(db.String(100))

    # Gerar uma String "Printável"
    def __repr__(self):
        return self.name

class Comentarios(db.Model):
    id_comentario = db.Column(db.Integer, primary_key=True, autoincrement = True)
    comentario = db.Column(db.String(500))

    # Gerar uma String "Printável"
    def __repr__(self):
        return self.name

class Usuarios(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement = True)
    nome_usuario = db.Column(db.String(100))
    email = db.Column(db.String(50))
    senha = db.Column(db.String(100))

    # Gerar uma String "Printável"
    def __repr__(self):
        return self.name