from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from varmeinfo import Config
from varmeinfo.models import HeatUnitModel, UserHeatUnitModel, UserModel

config = Config()


def main() -> None:
    engine = create_engine(config.database_url)

    with Session(engine) as session:
        existing = session.query(UserHeatUnitModel).count()
        if existing:
            print(f"Skipping seed — {existing} relationship(s) already present.")
            return

        heat_units = session.query(HeatUnitModel).all()[0:3]

        user = (
            session.query(UserModel)
            .filter(UserModel.email == "anbae@launer.dk")
            .first()
        )

        recs = [
            UserHeatUnitModel(user_id=user.id, heat_unit_id=hu.id) for hu in heat_units
        ]
        session.add_all(recs)
        session.commit()


if __name__ == "__main__":
    main()
