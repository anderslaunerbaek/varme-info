from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from varmeinfo import Config
from varmeinfo.functions import create_user
from varmeinfo.models import Base, UserModel

config = Config()


def main() -> None:
    engine = create_engine(config.database_url)

    print("Creating tables...")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        existing = session.query(UserModel).count()
        if existing:
            print(f"Skipping seed — {existing} user(s) already present.")
            return
        user = create_user(email="anbae@launer.dk", password="password")
        session.add(user)
        session.commit()
        session.refresh(user)
        print(user.id, user.created_at)


if __name__ == "__main__":
    main()
