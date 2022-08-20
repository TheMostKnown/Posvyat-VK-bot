from sqlalchemy.orm import Session

from app.create_db import Orgs


def is_admin(
        session: Session,
        chat_id: int
):
    if session.query(Orgs).filter_by(id=chat_id).first():
        return True
    else:
        return False
