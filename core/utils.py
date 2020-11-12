import python_jwt as jwt
import datetime

#Helper functions

def generateToken(email, password, key):
    user_info = {"email": email, "password": password }
    return jwt.generate_jwt(user_info, key, 'HS256', datetime.timedelta(minutes=10))
    
