from dataclasses import dataclass

from sqlalchemy import Column, Integer, String

from src import db


@dataclass
class ApiUser(db.Model):
    """

    This table is for mobile users access through the API
    """
    __tablename__ = 'api_user'
    user_id: int = Column(Integer, primary_key=True)
    account_number: int = Column(Integer)
    device: str = Column(String(50))
    pin: str = Column(String(100))
    user_number: int = Column(Integer)

    @property
    def serialize(self):
        return {
            'account': self.account_number,
            'user_number': self.user_number,
            'device': str(self.device)
        }
