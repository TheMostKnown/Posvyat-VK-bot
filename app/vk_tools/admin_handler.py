import re

from sqlalchemy.orm import Session

from app.create_db import Info


def admin_add_info(session: Session, text: str) -> True:
    correct = re.search(r"/add_info\b\s*\((.{1,100})\)\s*(.{1,500})\s*", text)
    if not correct:
        return False
    question = correct[1]
    answer = correct[2]

    session.add(
        Info(
            question=question,
            answer=answer
        )
    )
    session.commit()
    return True

