from __future__ import annotations

from flask import session

from src import db
from src.models.system_user_model import SystemUser


class UserRepository:

    @staticmethod
    def query_system_user(email: str | None = None) -> SystemUser:
        if email is None:
            return db.session.execute(db.select(SystemUser).filter_by(email=session["username"])).scalar_one()
        else:
            return db.session.execute(db.select(SystemUser).filter_by(email=email)).scalar_one()

    @staticmethod
    def query_system_user_by_id(id: int) -> SystemUser:
        return db.session.execute(db.select(SystemUser).filter_by(id=id)).scalar_one()

    @staticmethod
    def query_all_users() -> list[SystemUser]:
        return db.session.execute(db.select(SystemUser)).scalars().all()

    @staticmethod
    def query_all_users_by_role(role: str) -> list[SystemUser]:
        return db.session.execute(db.select(SystemUser).filter_by(role=role)).scalars().all()

    @staticmethod
    def query_all_users_by_branch(branch: str) -> list[SystemUser]:
        return db.session.execute(db.select(SystemUser).filter_by(branch=branch)).scalars().all()

    @staticmethod
    def query_all_users_by_branch_and_role(branch: str, role: str) -> list[SystemUser]:
        return db.session.execute(db.select(SystemUser).filter_by(branch=branch, role=role)).scalars().all()

    @staticmethod
    def query_all_users_by_branch_and_role_and_status(branch: str, role: str, status: str) -> list[SystemUser]:
        return db.session.execute(db.select(SystemUser).filter_by(branch=branch, role=role, status=status)).scalars().all()

    @staticmethod
    def query_all_users_by_branch_and_status(branch: str, status: str) -> list[SystemUser]:
        return db.session.execute(db.select(SystemUser).filter_by(branch=branch, status=status)).scalars().all()

    @staticmethod
    def query_all_users_by_role_and_status(role: str, status: str) -> list[SystemUser]:
        return db.session.execute(db.select(SystemUser).filter_by(role=role, status=status)).scalars().all()

    @staticmethod
    def query_all_users_by_status(status: str) -> list[SystemUser]:
        return db.session.execute(db.select(SystemUser).filter_by(status=status)).scalars().all()

    @staticmethod
    def query_all_users_by_branch_and_role_and_status_and_name(branch: str, role: str, status: str, name: str) -> list[SystemUser]:
        return db.session.execute(db.select(SystemUser).filter_by(branch=branch, role=role, status=status, name=name)).scalars().all()

    @staticmethod
    def query_all_users_by_branch_and_role_and_name(branch: str, role: str, name: str) -> list[SystemUser]:
        return db.session.execute(db.select(SystemUser).filter_by(branch=branch, role=role, name=name)).scalars().all()

    @staticmethod
    def update_system_user(user: SystemUser):
        db.session.add(user)
        db.session.commit()
