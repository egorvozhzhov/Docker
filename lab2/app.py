from flask import Flask, jsonify, request
from lab2 import get_class_volumes
from functools import wraps
import requests
import time
from datetime import datetime
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
def get_lab2():
    course = request.args.get('course')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    date_object1 = datetime.strptime(start_date, "%Y-%m-%d")
    unix_time1 = time.mktime(date_object1.timetuple())/60/60/24
 
    date_object2 = datetime.strptime(end_date, "%Y-%m-%d")
    unix_time2 = time.mktime(date_object2.timetuple())/60/60/24
    d1 = int(unix_time1) + 1
    d2 = int(unix_time2) + 1
    try:
        volumes = get_class_volumes(course, d1, d2)
    except ValueError as err:
        return jsonify({"error": str(err)}), 204
    dict_volumes = [{'class_title':volumes[0][i], 'date':volumes[1][i], 'pair_number':volumes[2][i], 'volume':volumes[3][i]} for i in range(len(volumes[0]))]
    
    return jsonify({'volumes': dict_volumes}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=12000)