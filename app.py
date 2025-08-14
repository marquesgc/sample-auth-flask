from flask import Flask, request, jsonify

from models.database import db
from models.user import User  
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"  
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")    
      #login
    if username and password:
            user = User.query.filter_by(username=username).first()
            if user.password == password:
                login_user(user)
                print(current_user.is_authenticated)
                return jsonify({"messege": "autenficiação confirmada."})
    return jsonify({"massage": "Credenciais não reconhecidas"}) , 400     

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    
    logout_user()
    return jsonify ({"message": "logout concluído com sucesso"})
@app.route("/user", methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if username and password:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message':'usuário cadastrado'}), 400
    return jsonify({'message':'credenciais inválidas'}), 400

@app.route("/user/<int:id_user>",methods=["GET"])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)
    if user and id_user != current_user.id:
        return {"user": user.username , "pass":user.password}
    return jsonify({"message":"usuário não encontrado."}), 404

@app.route("/user/<int:id_user>",methods=["PUT"])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)
    if user:
        user.password = data.get("password")
        db.session.commit()
        return jsonify({"massage":"Usuário {id_user} foi atualizado com sucesso"})
    return jsonify({"massage": "Credenciais não reconhecidas"}) , 400     

@app.route("/user/<int:user_id>", methods=["DELETE"])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.remove(user)
        db.session.commit()
        return jsonify({"message":''})
        
        
if __name__ == "__main__":
    app.run(debug=True)