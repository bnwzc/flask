from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import mapped_column, relationship

from database import db


class Player(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    token = mapped_column(String)
    scores = relationship("Score", back_populates="player")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "token": self.token,
        }


class Score(db.Model):
    id = mapped_column(Integer, primary_key=True)
    score = mapped_column(Integer)
    date = mapped_column(DateTime, insert_default=func.now())
    player_id = mapped_column(ForeignKey("player.id"))
    player = relationship("Player", back_populates="scores")

    def to_dict(self):
        return {
            "id": self.id,
            "score": self.score,
            "date": self.date,
            "player": self.player.name,
        }

