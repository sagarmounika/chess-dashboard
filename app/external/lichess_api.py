# app/external/lichess_api.py
import berserk

def get_top_players():
    session = berserk.TokenSession("lip_bAMesoZcsGQHunNiTs5D")
    client = berserk.Client(session=session)
    return client.users.get_leaderboard('classical', 50)

def get_rating_history(username):
    session = berserk.TokenSession("lip_bAMesoZcsGQHunNiTs5D")
    client = berserk.Client(session=session)
    return client.users.get_rating_history(username)
