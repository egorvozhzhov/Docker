from flask import Flask, request, jsonify
import redis
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone

app = Flask(__name__)
app.config['ISS'] = 'vozhzhov.auth'
app.config['SECRET_KEY'] = '8h2j9KlP4n6Qr7tYu3vAx1zCc5Ee6Rg7Ht9i0Jk2Lm4Np1q3Rs5Uu8Vx0yA'

r1 = redis.StrictRedis(host='redis', port=6379, db=1)
r2 = redis.StrictRedis(host='redis', port=6379, db=2)

@app.route('/register', methods=['POST'])
def register_user():
    username = request.args.get('username')
    password = request.args.get('password')
    
    
    if r1.exists(username):
        return jsonify({'message': 'Такой пользователь уже зарегистрирован'}), 401
    
    hash_pass = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

    r1.set(username, hash_pass)

    return jsonify({'message': 'Succsefull registration: Now you need to sigh in'}), 200

@app.route('/login', methods=['POST'])
def login_user():
    username = request.args.get('username')
    password = request.args.get('password')

    if not r1.exists(username):
            return jsonify({'message': 'Пользователь с такими данными не найден'}), 4
    
    saved_pass = r1.get(username)
    saved_pass = saved_pass.decode('utf-8')
    if check_password_hash(saved_pass, password):
        expireat= datetime.utcnow() + timedelta(minutes=30)
        token = jwt.encode(payload={'iss':app.config['ISS'], 'exp': expireat}, key=app.config['SECRET_KEY'], algorithm="HS256")
        r2.set(token, username)
        r2.expire(token, 1800)
        return jsonify({'token': token}), 200
    
    return jsonify({'message': 'Пользователь с такими данными не найден'}), 401 

@app.route('/validate', methods=['POST'])
def validate_token():
    token = request.headers.get('Authorization')
    if not token or len(token.split(" ")) != 2:
        return jsonify({'message': 'Токен неправильного формата'}), 401

    token = token.split(" ")[1]

    if r2.ttl(token) == -2:
        r2.delete(token)
        return jsonify({'message': 'Недействительный токен. Войдите снова'}), 401
    else:
        return jsonify({'message': 'Действительный токен'}), 200
    

@app.route('/validate2', methods=['POST'])
def validate_token2():
    token = request.headers.get('Authorization')
    if not token or len(token.split(" ")) != 2:
        return jsonify({'message': 'Токен неправильного формата'}), 401

    token = token.split(" ")[1]
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': 'Действительный токен'}), 200
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Недействительный токен. Войдите снова'}), 401
    
    
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)