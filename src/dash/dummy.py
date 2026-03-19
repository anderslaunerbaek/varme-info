import random
import uuid
from datetime import datetime, timedelta

import pandas as pd

from ..data import HeatUnit, HeatUnitType, SensorRecord, SensorRecordType


def generate_sample_data() -> tuple[list[HeatUnit], list[SensorRecord]]:
    heat_units = [
        HeatUnit(name="Unit A", type=HeatUnitType.type1),
        HeatUnit(name="Unit B", type=HeatUnitType.type1),
        HeatUnit(name="Unit C", type=HeatUnitType.type2),
        HeatUnit(name="Unit D", type=HeatUnitType.type2),
    ]

    records: list[SensorRecord] = []
    base_time = datetime(2024, 1, 1)
    rng = random.Random(42)

    for unit in heat_units:
        for i in range(120):
            ts = (base_time + timedelta(hours=i * 2)).isoformat()
            for record_type in SensorRecordType:
                records.append(
                    SensorRecord(
                        type=record_type,
                        value=round(
                            rng.gauss(
                                20 if record_type == SensorRecordType.type1 else 50, 5
                            ),
                            2,
                        ),
                        heat_unit_id=unit.id,
                        correlation_id=str(uuid.uuid4()),
                        time_stamp=ts,
                    )
                )

    return heat_units, records


def build_dataframe(
    heat_units: list[HeatUnit], records: list[SensorRecord]
) -> pd.DataFrame:
    unit_map = {u.id: u for u in heat_units}
    rows = []
    for r in records:
        unit = unit_map.get(r.heat_unit_id)
        rows.append(
            {
                "time_stamp": r.time_stamp,
                "value": r.value,
                "sensor_type": str(r.type),
                "heat_unit_id": r.heat_unit_id,
                "heat_unit_name": unit.name if unit else "Unknown",
                "heat_unit_type": str(unit.type) if unit else "Unknown",
            }
        )
    df = pd.DataFrame(rows)
    df["time_stamp"] = pd.to_datetime(df["time_stamp"])
    return df
