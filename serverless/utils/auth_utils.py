import jwt


def get_user_id_from_auth(authorization: str):
    token = authorization.split(" ")[1]
    decoded_token = jwt.decode(token, options={"verify_signature": False})
    user_id = decoded_token.get("id")
    return user_id
