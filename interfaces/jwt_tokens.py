import jwt
SECRET_KEY="mysecret"

class JWTManagement():
    def __init__(self) -> None:
        pass


    def encode_payload(self, payload):
        try:
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        except Exception as e:
            return "Cannot Generate Token"
        return token
    
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except Exception as e:
            print(e)
            return "Invalid Token"
        return payload