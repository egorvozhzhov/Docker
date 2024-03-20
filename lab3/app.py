from flask import Flask, jsonify, request
from lab3 import get_volume_of_listened_hours
from functools import wraps
import requests

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify(success=True)

def token_valid(f):
    @wraps(f)
    def decorate(*args, **kwargs):
        access_token = request.headers.get('Authorization')
    
        if access_token and access_token.startswith('Bearer '):
            access_token = access_token.split(" ")[1]
            auth_service_url = "http://auth:10000/validate"
            headers = {"Authorization": f"Bearer {access_token}"}
            
            response = requests.post(auth_service_url, headers=headers)
            
            if response.status_code == 200:
                return f(*args, **kwargs)
            else:
                return jsonify({'message': 'Токен недействителен, пройдите авторизацию заново'}), 401
        else:
            return jsonify({'message': 'Пожалуйста, предоставьте действительный токен (токен неверного формата)'}), 401
        
    return decorate


@app.route('/', methods=['GET'])
@token_valid
def get_lab3():
    group = request.args.get('group')

    courses = get_volume_of_listened_hours(group)
    return jsonify({'group': group, "courses": courses}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=13000)