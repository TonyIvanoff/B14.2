
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_PATH = "sqlite:///sochi_athletes.sqlite3"

Base = declarative_base()

# build a table
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

# request of the user data via user input
def request_data():
    print("Hi! I will collect your data!")
    first_name = input("Enter your first name: ")
    last_name =input("Enter your last name: ")
    gender = input("Are you Male or Female?: ")
    email = input("Enter your e-mail address: ")
    birthdate = input("Enter your birthdate (example, yyyy-mm-dd): ")
    height = input("Enter your height (example, 1.75): ")

    user = User(
        
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )
    return user

def main():
    session = connect_db()
    user = request_data()
    session.add(user)
    session.commit()
    print("Data is stored! Thank you!")

if __name__ == "__main__":
    main()



