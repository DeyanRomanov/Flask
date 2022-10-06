from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.complaint import ComplaintManager
from models import UserRole
from schemas.responses.complaint import ComplaintSchemaResponse
from utils.decorators import permission_required


class ComplaintResource(Resource):
    @auth.login_required
    @permission_required(UserRole.complainer)
    def post(self):
        data = request.get_json()
        current_user = auth.current_user()
        new_complain = ComplaintManager.create(data, current_user)
        return ComplaintSchemaResponse().dump(new_complain), 201
