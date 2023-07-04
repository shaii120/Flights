import pandas as pd
import os
from datetime import timedelta


class Flights:
    def __init__(self) -> None:
        self.CSV_PATH = os.path.join(".", "data.csv")
        self.MIN_WAITING_TIME = timedelta(minutes=180)
        self.MAX_SUCCESS_FLIGHTS = 20
        self.data = pd.read_csv(
            self.CSV_PATH, sep="\s*,\s*", index_col="flight ID", engine="python"
        )
        data = data.sort_values(by="Arrival")
        data["Arrival"] = pd.to_datetime(data["Arrival"], format="%H:%M")
        data["Departure"] = pd.to_datetime(data["Departure"], format="%H:%M")

    def anlayze_success_flights(self):
        self.data["Waiting"] = self.data["Departure"] - self.data["Arrival"]

        flights_status = self.data["Waiting"] >= self.MIN_WAITING_TIME
        success_flights = flights_status[flights_status == True].index
        overload_success_flights = flights_status.index.isin(
            success_flights[self.MAX_SUCCESS_FLIGHTS :]
        )
        flights_status[overload_success_flights] = False

        self.data["success"] = "fail"
        self.data.loc[flights_status, "success"] = "success"
