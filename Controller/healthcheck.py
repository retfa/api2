from flask_restx import Resource, Namespace

ns_healthcheck = Namespace('healthcheck', description='健康檢查')


@ns_healthcheck.route('/')
class HealthCheck(Resource):
    def get(self):
        return {
            "status": "Healthy",
            "version": "1.0.0",
            "details": None
        }, 200
