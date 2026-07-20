import json
from flask import Response, jsonify, make_response, request, current_app
from flask_restx import Resource, Namespace, fields
import logging
from Model.jwt_manager import JwtManager
from Model.user import UserDto
from BLL.auth import Authentication

ns_authenticate = Namespace('authentication', description='帳號驗證 相關')

login_model = ns_authenticate.model('login', {
    'acc': fields.String(required=True, description='Username'),
    'pwd': fields.String(required=True, description='Password')
})


@ns_authenticate.route('/authenticate')
class Authenticate(Resource):
    @ns_authenticate.expect(login_model)
    @ns_authenticate.doc(description='Accept Post to log user in.',
                         responses={200: 'OK',
                                    400: 'Bad Request'})
    def post(self):
        try:
            logging.info('login.py')
            data = request.get_json()
            usr = UserDto.user_login(data['acc'], data['pwd'])
            user = authenticate_user(usr)  # 自行实现用户验证函数

            if user:
                jwt_manager = JwtManager()
                jwt_token = jwt_manager.generate_jwt(user)
                logging.info(jwt_token)
                response = make_response({'jwt': jwt_token})
                response.headers['Authorization'] = 'Bearer ' + jwt_token
                response.set_cookie('jwt', jwt_token, httponly=True)
                # response.set_cookie('jwt', jwt_token, httponly=True, samesite='None')
                return response

            return {'message': 'Authentication failed'}, 401
        except Exception as e:
            return {'message': f'login.py |An error occurred: {str(e)}'}, 500


def authenticate_user(data: UserDto.user_login):
    auth = Authentication(current_app.config['folders'])
    user = auth.Auth(data)
    return user


@ns_authenticate.route('/refreshtoken')
class RefreshToken(Resource):
    # @ns_login.expect(login_model)
    @ns_authenticate.hide
    @ns_authenticate.doc(description='Generate refresh token',
                         responses={200: 'OK',
                                    400: 'Bad Request'})
    def post(self):
        pass


@ns_authenticate.route('/revokerefreshtoken')
class RevokeRefreshToken(Resource):
    # @ns_login.expect(login_model)
    @ns_authenticate.hide
    @ns_authenticate.doc(description='Revoke refresh token',
                         responses={200: 'OK',
                                    400: 'Bad Request'})
    def post(self):
        pass

@ns_authenticate.route('/whoami')
class WhoAmI(Resource):
    @ns_authenticate.doc(description='Get login user data',
                         responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    def get(self):
        try:
            jwt_manager = JwtManager()
            payload = jwt_manager.decode_jwt_from_request()

            response_data = {
                'FTAId': payload.get('FTAId'),
                'YFYId': payload.get('YFYId'),
                'Name': payload.get('Name'),
            }

            return self._build_response(response_data, 200)

        except PermissionError as e:
            return self._build_response({'message': str(e)}, 401)
        except Exception as e:
            return self._build_response({'message': f'Unexpected error: {str(e)}'}, 500)

    def _build_response(self, data: dict, status_code: int):
        """ 統一建構response，強制加防cache header """
        # response = make_response(jsonify(data), status_code)
        payload = json.dumps(data, ensure_ascii=False)  # 關鍵：ensure_ascii=False
        response = make_response(Response(payload, status=status_code, mimetype='application/json'))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, private'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        response.headers['Vary'] = 'Cookie, Authorization'
        return response

