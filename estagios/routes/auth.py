from estagios import db, mail
from estagios.models import User, RoleEnum
from flask import Blueprint, request, jsonify
from flask_mail import Message
import random 
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/cadastro', methods=['POST'])
def cadastro_usuario():
    dados = request.get_json()
    novo_usuario = User(
        email = dados.get('email'),
        senha = dados.get('senha'),
        role = RoleEnum.ESTUDANTE
    )
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({
        'mensagem': 'Usuário criado com sucesso',
        'id': novo_usuario.id
    })

@auth_bp.route('/confirmar-email', methods=['POST'])
def confirmar_email():
    dados = request.get_json()
    id = dados.get('id')
    codigo = ''.join(random.choice('0123456789') for _ in range(6))
    usuario = User.query.get(id)
    msg = Message(
                subject = "Olá, confirme seu email.",
                body = f"Seu código de confirmação: {codigo}",
                sender = ('Estágio Parceiro | IFPE','estagioparceiro@gmail.com'),
                recipients = [usuario.email]
            )
    mail.send(msg)
    return jsonify({'mensagem': 'Email enviado com sucesso.', 'codigo': codigo})

@auth_bp.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    email = dados.get('email')
    senha = dados.get('senha')

    user = User.query.filter_by(email=email).first()

    if not user or user.senha != senha:
        return jsonify({'erro': 'Credenciais inválidas'}), 401

    login_user(user)  
    return jsonify({'mensagem': 'Login bem-sucedido', 'user_id': user.id, 'role': user.role.value})
    
@auth_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({'mensagem': 'Logout efetuado com sucesso'})

@auth_bp.route('/mudar-senha', methods=['POST'])
@login_required
def mudar_senha():
    data = request.get_json()
    
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    if not current_password or not new_password:
        return jsonify({'error': 'Preencha todos os campos'}), 400

    # Verifica se a senha atual está correta
    if not check_password_hash(current_user.password_hash, current_password):
        return jsonify({'error': 'Senha atual incorreta'}), 401

    # Opcional: regras para a nova senha
    if len(new_password) < 6:
        return jsonify({'error': 'A nova senha deve ter pelo menos 6 caracteres'}), 400

    # Atualiza a senha
    current_user.password_hash = generate_password_hash(new_password)
    
    # Salva no banco
    db.session.commit()

    return jsonify({'message': 'Senha alterada com sucesso'}), 200

@app.route('/usuario')
@login_required
def get_logged_in_user():
    return jsonify({'email': current_user.email})
