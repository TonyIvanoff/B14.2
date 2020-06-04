import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class Athlete(Base):
    __tablename__ = 'athelete'
    id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    age = sa.Column(sa.INTEGER)
    birthdate = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    height = sa.Column(sa.REAL)
    name = sa.Column(sa.TEXT)
    weight = sa.Column(sa.INTEGER)
    gold_medals = sa.Column(sa.INTEGER)
    silver_medals = sa.Column(sa.INTEGER)
    bronze_medals = sa.Column(sa.INTEGER)
    total_medals = sa.Column(sa.INTEGER)
    sport = sa.Column(sa.TEXT)
    country = sa.Column(sa.TEXT)

class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.TEXT)
    last_name = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    email = sa.Column(sa.TEXT)
    birthdate = sa.Column(sa.TEXT)
    height = sa.Column(sa.REAL)

# connection to database
def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def date_convert(date_str):
    date_split = date_str.split("-")
    date_conv = map(int, date_split)
    date = datetime.date(*date_conv)
    return date
def request_userdata():
    user_id = input("Enter user ID: ")
    return int(user_id)

def find_ath_bd(user, session):
    
    athletes = session.query(Athlete).all()
    ath_bdates = {}
    for ath in athletes:
        a_bd = date_convert(ath.birthdate)
        ath_bdates[ath.id] = a_bd

    user_bd = date_convert(user.birthdate)
    min_dist = None
    athlete_id = None
    athlete_bd = None

    for a_id, a_bd in ath_bdates.items():
        diff = abs(user_bd - a_bd)
        if not min_dist or diff < min_dist:
           min_dist = diff
           athlete_id = a_id
           athlete_bd = a_bd
    
    return athlete_id, athlete_bd

def find_ath_h(user, session):
    athletes = session.query(Athlete.height != None).all()
    atlhete_h = {athlete.id: athlete.height for athlete in athletes}

    user_height = user.height
    min_dist = None
    athlete_id = None
    athlete_height = None

    for a_id, a_h in atlhete_h.items():
        if a_h is None:
            continue

        diff = abs(user_height - a_h)
        if not min_dist or diff < min_dist:
            min_dist = diff
            athlete_id = a_id
            athlete_height = a_h
    
    return athlete_id, athlete_height


def main():
    session = connect_db()
    user_id = request_userdata()
    user = session.query(User).filter(User.id == user_id)
    if user:
        
        athlete_bd, a_bd = find_ath_bd(user, session)
        athlete_height, a_h = find_ath_h(user, session)
        print("Nearest athlete by b-day: {} - {}".format(athlete_bd, a_bd))
        print("Nearest athlete by height: {} - {}".format(athlete_height, a_h))
    else:
        print("No User found")
        
    
if __name__ == "__main__":
    main()