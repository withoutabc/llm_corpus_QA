import jwt
import datetime

# 密钥，用于签名和验证令牌
secret_key = "your_secret_key"


# 生成访问令牌
def generate_access_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15),  # 令牌的过期时间
    }
    access_token = jwt.encode(payload, secret_key, algorithm="HS256")
    return access_token


# 生成刷新令牌
def generate_refresh_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),  # 刷新令牌的过期时间
    }
    refresh_token = jwt.encode(payload, secret_key, algorithm="HS256")
    return refresh_token


# 验证访问令牌
def verify_access_token(token):
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        user_id = payload.get("user_id")
        return user_id
    except jwt.ExpiredSignatureError:
        return None  # 令牌过期
    except jwt.InvalidTokenError:
        return None  # 无效令牌


# 验证刷新令牌
# 验证刷新令牌并解析出user_id
def verify_refresh_token(token):
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        user_id = payload.get("user_id")
        return user_id
    except jwt.ExpiredSignatureError:
        return None  # 令牌过期
    except jwt.InvalidTokenError:
        return None  # 无效令牌

# # 示例使用
# user_id = 123
# access_token = generate_access_token(user_id)
# refresh_token = generate_refresh_token(user_id)
#
# # 验证访问令牌
# user_id_from_access_token = verify_access_token(access_token)
# if user_id_from_access_token:
#     print(f"User ID解析成功: {user_id_from_access_token}")
# else:
#     print("Refresh Token验证失败")
#
# # 示例使用
# user_id_from_refresh_token = verify_refresh_token(refresh_token)
# if user_id_from_refresh_token:
#     print(f"User ID解析成功: {user_id_from_refresh_token}")
# else:
#     print("Refresh Token验证失败")
