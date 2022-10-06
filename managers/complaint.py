from db import db
from models import ComplaintModel


class ComplaintManager:
    @staticmethod
    def create(data, user):
        data['complainer_id'] = user.id
        complaint = ComplaintModel(**data)
        db.session.add(complaint)
        db.session.commit()
        return complaint
