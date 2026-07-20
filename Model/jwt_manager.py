from flask import current_app, request
import jwt
import json
import os
import uuid
from datetime import datetime, timedelta, timezone
import logging
from Model.user import UserDto


class JwtManager:
    def __init__(self):
        try:
            logging.info('jwt_manager.py')
            json_path_app = os.path.join(current_app.config['folders']['exe'], 'appsettings.json')
            json_path_security = os.path.join(current_app.config['folders']['temproot'], 'security.json')
            logging.info(f'json_path_app: {json_path_app}')
            logging.info(f'json_path_security: {json_path_security}')
            with open(json_path_app, 'r') as file1:
                data = json.load(file1)
                self.expiration_seconds = data["Expiration"]["Jwt"]

            with open(json_path_security, 'r') as file2:
                data = json.load(file2)
                self.key = data["Jwt"]["Key"]
                self.issuer = data["Jwt"]["Issuer"]
        except Exception as e:
            return {'message': f'jwt_manager.py |An error occurred: {str(e)}'}, 500

    def generate_jwt(self, user: UserDto.user_signedIn):
        utcnow = datetime.utcnow()
        payload = {
            "FTASn": user.FTASn,
            "FTAId": user.FTAId,
            "YFYId": user.YFYId,
            "Name": user.Name,
            "exp": utcnow + timedelta(seconds=self.expiration_seconds),
            "iat": str(int(datetime.timestamp(utcnow.replace(microsecond=0, tzinfo=timezone.utc)))),
            "nbf": utcnow,
            "jti":str(uuid.uuid4()),
            "iss":self.issuer,
            "aud":self.issuer
        }
        jwt_token = jwt.encode(payload, self.key, algorithm='HS256')
        return jwt_token

    def _get_jwt_token_from_request(self) -> str:
        token = request.cookies.get('jwt')
        if not token:
            auth_header = request.headers.get('Authorization')
            if auth_header:
                parts = auth_header.split()
                if len(parts) == 2 and parts[0].lower() == 'bearer':
                    token = parts[1]

        if not token:
            raise PermissionError("JWT not found in cookie or Authorization header")

        return token

    def decode_jwt_from_request(self) -> dict:
        """從 request 的 cookie 或 Authorization header 解析並驗證 JWT。"""
        token = self._get_jwt_token_from_request()

        try:
            payload = jwt.decode(
                token,
                self.key,
                algorithms=["HS256"],
                issuer=self.issuer,
                audience=self.issuer
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise PermissionError("JWT expired")
        except jwt.InvalidTokenError as e:
            raise PermissionError(f"Invalid JWT: {str(e)}")

    def decode_jwt_from_cookie(self) -> dict:
        return self.decode_jwt_from_request()
