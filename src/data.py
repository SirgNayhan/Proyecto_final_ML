"""
data.py
Carga y unión de las tablas del dataset nycflights13 (vuelos, clima, aviones,
aeropuertos, aerolíneas) en un único DataFrame listo para exploración/modelado.

El dataset se instala vía pip (paquete `nycflights13`), por lo que no requiere
descargas externas ni credenciales: es 100% reproducible desde cero.
"""

import pandas as pd
import nycflights13 as f

# Columnas que solo se conocen DURANTE o DESPUÉS del vuelo.
# Se excluyen siempre de los features para evitar leakage temporal.
LEAKAGE_COLS = ["dep_time", "dep_delay", "arr_time", "air_time", "arr_delay"]

TARGET_COL = "retraso_15"


def load_raw():
    """Devuelve las 5 tablas crudas del dataset."""
    return {
        "flights": f.flights.copy(),
        "weather": f.weather.copy(),
        "planes": f.planes.copy(),
        "airports": f.airports.copy(),
        "airlines": f.airlines.copy(),
    }


def build_dataset(drop_cancelled=True):
    """
    Construye el dataset unido a nivel de vuelo individual.

    - Une flights + planes (por tailnum) + weather (por origen y hora) +
      airlines (por carrier) + airports (por destino).
    - Define la variable objetivo binaria `retraso_15` = 1 si arr_delay >= 15 min.
    - Los vuelos cancelados (sin arr_delay) se excluyen del target por defecto
      y se documentan como limitación (ver proposal.md, sección "Riesgos técnicos").

    Returns
    -------
    df : pd.DataFrame
        Dataset unido, a nivel de vuelo, con la columna objetivo `retraso_15`.
    """
    raw = load_raw()
    flights, weather, planes, airports, airlines = (
        raw["flights"], raw["weather"], raw["planes"], raw["airports"], raw["airlines"]
    )

    df = flights.copy()
    if drop_cancelled:
        df = df.dropna(subset=["arr_delay"]).copy()

    df[TARGET_COL] = (df["arr_delay"] >= 15).astype(int)

    df = df.merge(
        planes[["tailnum", "year", "manufacturer", "model", "engines", "seats", "engine"]]
        .rename(columns={"year": "plane_year"}),
        on="tailnum", how="left",
    )

    df["time_hour"] = pd.to_datetime(df["time_hour"])
    weather = weather.copy()
    weather["time_hour"] = pd.to_datetime(weather["time_hour"])
    df = df.merge(
        weather.drop(columns=["year", "month", "day", "hour"]),
        on=["origin", "time_hour"], how="left",
    )

    df = df.merge(airlines, on="carrier", how="left")
    df = df.merge(
        airports[["faa", "lat", "lon", "alt"]]
        .rename(columns={"faa": "dest", "lat": "dest_lat", "lon": "dest_lon", "alt": "dest_alt"}),
        on="dest", how="left",
    )

    return df


def feature_columns(df):
    """Columnas utilizables como features: todo excepto target y columnas con leakage."""
    exclude = set(LEAKAGE_COLS) | {TARGET_COL, "year", "flight", "tailnum", "time_hour", "name"}
    return [c for c in df.columns if c not in exclude]


if __name__ == "__main__":
    data = build_dataset()
    print("Shape final:", data.shape)
    print("Balance del target:")
    print(data[TARGET_COL].value_counts(normalize=True))
