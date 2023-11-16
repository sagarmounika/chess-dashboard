from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.players import PlayersScheme, PlayerWithRatingHistory, RatingHistoryEntry
from app.models.players import Players, RatingHistory
from typing import List
import berserk
from datetime import datetime, timedelta
# from app.security import oauth2_scheme, get_current_user
from app.utils import JWTBearer
router = APIRouter()

@router.get("/top-players", response_model=List[PlayersScheme])
async def get_top_players(
    db: Session = Depends(get_db),
    current_user: str = Depends(JWTBearer())

):
    session = berserk.TokenSession("lip_bAMesoZcsGQHunNiTs5D")
    client = berserk.Client(session=session)
    top_players_data = client.users.get_leaderboard('classical', 50)

    players = []
    for player_data in top_players_data:
        username = player_data['username']
        rating = player_data['perfs']['classical']['rating']

        db_player = db.query(Players).filter(Players.username == username).first()
        if db_player:
            db_player.rating = rating
        else:
            db_player = Players(username=username, rating=rating)
            db.add(db_player)
        db.commit()
        db.refresh(db_player)

        players.append(PlayersScheme(id=db_player.id, username=username, rating=rating))

    return players

@router.get("/player/{username}/rating-history", response_model=PlayerWithRatingHistory)
async def get_rating_history(
    username: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(JWTBearer())
):
    session = berserk.TokenSession("lip_bAMesoZcsGQHunNiTs5D")
    client = berserk.Client(session=session)
    rating_history_data = client.users.get_rating_history(username)

    rating_history = []

    today = datetime.utcnow()
    thirty_days_ago = today - timedelta(days=30)
    db_player = db.query(Players).filter(Players.username == username).first()

    for rating_data in rating_history_data:
        try:
            if rating_data.get('points'):
                name = rating_data['name']
                points = []

                for point_entry in rating_data['points']:
                    point_date = datetime(point_entry[0], point_entry[1] + 1, point_entry[2])
                    rating_value = point_entry[3]
                    points.append({"date": f"{point_entry[0]}-{point_entry[1] + 1}-{point_entry[2]}", "value": rating_value})

                rating_history.append({"name": name, "points": points})
        except Exception as e:
            print(f"Error processing rating data: {e}")

    if rating_history:
        db_player.rating = rating_history[0]["points"][0]["value"]

    db.commit()
    db.refresh(db_player)

    player = PlayerWithRatingHistory(id=db_player.id, username=username, rating=db_player.rating, rating_history=rating_history)
    return player
