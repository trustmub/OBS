from typing import List

from src import db
from src.models.branch_model import Branch


class BaseRepository:

    @staticmethod
    def get_branches() -> List[Branch]:
        return db.session.execute(db.select(Branch)).scalars()
