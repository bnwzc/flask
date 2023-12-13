import secrets
from pathlib import Path

from flask import Flask, render_template, redirect, request, jsonify

from database import db
from models import Player, Score
import random
from datetime import datetime, timedelta

import pprint

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hiscores.db"
app.instance_path = Path(".").resolve()
db.init_app(app)


@app.route("/")
def home():
    # return "<!doctype html><html><body><h1>Example</h1></body></html>"
    return render_template("home.html", name = "ZKD", student_id = "A01329778")


@app.route("/create-players")
def create_players():
    with open("players.txt") as f:
        for name in f.read().splitlines():
            player = Player(name=name)
            player.token = secrets.token_hex(16)
            db.session.add(player)

    db.session.commit()

    return render_template("info.html", message="All players have been created.")


@app.route("/create-tables")
def create_tables():
    db.create_all()
    return render_template("info.html", message="All tables have been created.")

@app.route("/players")
def table_players():
    stmt = db.select(Player).order_by(Player.name)
    data = db.session.execute(stmt)
    results = data.scalars()
    return render_template("table.html", players=results)

@app.route("/player/<int:player_id>/refresh_token")
def refresh_token(player_id):
    stmt = db.select(Player).where(Player.id == player_id)
    data = db.session.execute(stmt)
    this_player = data.scalar()
    db.session.delete(this_player)
    this_player.token = secrets.token_hex(16)
    db.session.add(this_player)
    db.session.commit()

    return redirect("/players")

@app.route("/create-scores")
def create_scores():
    score = Score(score=random.randint(1, 100))
    id = random.randint(1, 13)
    score.player_id = id
    start_date = datetime.now() - timedelta(days=365)
    end_date = datetime.now()
    random_date = start_date + timedelta(days=random.randint(0, 365))
    score.date = random_date
    db.session.add(score)
    db.session.commit()



    return render_template("info.html", message="Score have been created.")

@app.route("/api/player/<int:player_id>")
def single_player(player_id):
    stmt = db.select(Score).where(Score.player_id == player_id)
    data = db.session.execute(stmt)
    scores = data.scalars()

    stmt = db.select(Player).where(Player.id == player_id)
    data = db.session.execute(stmt)
    player = data.scalar()
    return render_template("single.html", scores=scores, player=player)

@app.route("/api/players")
def return_list_player():
    players_join_scores = Player.query.outerjoin(Score).order_by(Player.id)
    player_list = []
    for i in players_join_scores:
        player_list.append({
            "id": i.id,
            "name": i.name,
            "scores":[{"date": j.date.strftime("%a, %w %b %Y %X GMT"), "score": j.score} for j in i.scores]
        })
    return jsonify(player_list)

@app.route("/api/score", methods=["POST"])
def submit_score():
    data = request.get_json()
    if "user_token" not in data.keys() or "score" not in data.keys():
        return "Invalid JSON data", 400
    
    stmt = db.select(Player).where(Player.token == data["user_token"])
    data1 = db.session.execute(stmt)
    user = data1.scalar()
    if not user:
        return "No such a player"
    new_score = Score(score=data["score"], player_id=user.id, date=datetime.now())
    db.session.add(new_score)
    db.session.commit()
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
