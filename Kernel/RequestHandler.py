import logging
from flask import Flask
import flask_restx
import jwt
from common import GetJwtPayload, set_security


class RequestHandler:
    @staticmethod
    def handle_get_request(self, current_app: Flask, msg: str, request, parser: flask_restx.reqparse.RequestParser = None) -> flask_restx.reqparse.ParseResult:
        print(msg)
        logging.info(msg)
        try:
            set_security(self, current_app)
        except Exception as e:
            raise e

        data = {}
        if parser is not None:
            data = parser.parse_args()

        try:
            data['jwt'] = GetJwtPayload(self.security, request)
        except Exception as e:
            raise e
        return data

    # @staticmethod
    # def handle_post_request(self, current_app: Flask, msg: str, request, namespace) -> flask_restx.reqparse.ParseResult:
    #     print(msg)
    #     logging.info(msg)
    #     try:
    #         set_security(self, current_app)
    #     except Exception as e:
    #         raise e

    #     data = {}
    #     if namespace is not None:
    #         data['content'] = namespace.payload

    #     try:
    #         data['jwt'] = GetJwtPayload(self.security, request)
    #     except Exception as e:
    #         raise e
    #     return data

