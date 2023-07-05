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
        self.data = self.data.sort_values(by="Arrival")
        self.data["Arrival"] = pd.to_datetime(self.data["Arrival"], format="%H:%M")
        self.data["Departure"] = pd.to_datetime(self.data["Departure"], format="%H:%M")
        self.data["Waiting"] = self.data["Departure"] - self.data["Arrival"]

    def anlayze_success_flights(self):
        flights_status = self.data["Waiting"] >= self.MIN_WAITING_TIME
        success_flights = flights_status[flights_status == True].index
        overload_success_flights = flights_status.index.isin(
            success_flights[self.MAX_SUCCESS_FLIGHTS :]
        )
        flights_status[overload_success_flights] = False

        self.data["success"] = "fail"
        self.data.loc[flights_status, "success"] = "success"

    def get_flights(self, flights_id):
        return self.data.drop("Waiting", axis=1).loc[flights_id]

    def insert_flight(self, flight_id: str, arrival, departure):
        arrival = pd.to_datetime(arrival, format="%H:%M")
        departure = pd.to_datetime(departure, format="%H:%M")
        waiting = departure - arrival
        row = {
            "Arrival": arrival,
            "Departure": departure,
            "success": "",
            "Waiting": waiting,
        }
        self.data.loc[flight_id] = row
        self.anlayze_success_flights()
