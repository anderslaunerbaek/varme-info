import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from varmeinfo import Config
from varmeinfo.data import HeatUnitType
from varmeinfo.models import Base, HeatUnitModel

config = Config()

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{config.postgres_user}:{config.postgres_password}"
    f"@{config.postgres_host}:{config.postgres_port}"
    f"/{config.postgres_db}"
)

INITIAL_HEAT_UNITS = [
    HeatUnitModel(name="Boiler North", type=HeatUnitType.type1),
    HeatUnitModel(name="Boiler South", type=HeatUnitType.type1),
    HeatUnitModel(name="Heat Pump A", type=HeatUnitType.type2),
    HeatUnitModel(name="Heat Pump B", type=HeatUnitType.type2),
    HeatUnitModel(name="District Main", type=HeatUnitType.type1),
]


def main() -> None:
    engine = create_engine(DATABASE_URL)

    print("Creating tables...")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        existing = session.query(HeatUnitModel).count()
        if existing:
            print(f"Skipping seed — {existing} heat unit(s) already present.")
            return

        session.add_all(INITIAL_HEAT_UNITS)
        session.commit()
        print(f"Inserted {len(INITIAL_HEAT_UNITS)} heat units.")


if __name__ == "__main__":
    main()
