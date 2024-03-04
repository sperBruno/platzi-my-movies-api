from jwt import encode, decode
#read secret from env
def create_token(data:dict):
    token = encode(payload=data, key="",algorithm="HS256")
    return token

def validate_token(token):
    data = decode(token, key="",algorithms=["HS256"])
    print(data)
    return data