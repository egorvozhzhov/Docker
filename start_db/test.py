import jwt
from datetime import datetime, timezone
received_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ2b3poemhvdi5hdXRoIiwiZXhwIjoxNzAzMjQzODg1fQ.ikXF7iSfW-J3k6ENIzNmND01nTVj-bvA9yoPkiUFLYo'
secret = '8h2j9KlP4n6Qr7tYu3vAx1zCc5Ee6Rg7Ht9i0Jk2Lm4Np1q3Rs5Uu8Vx0yA'

try:
    decoded = jwt.decode(received_token, secret, algorithms=['HS256'])
    print(decoded)
    exp = decoded['exp']
    current_time = datetime.now(timezone.utc).timestamp()

   
    if current_time > exp:
        print('Время срока действия токена истекло')
    else:
        print('Токен действителен')
except jwt.InvalidTokenError:
    print('Токен недействителен')


try:
    decoded = jwt.decode(received_token, secret, algorithms=['HS256'])
    
except jwt.InvalidTokenError:
    print('Токен недействителен')
