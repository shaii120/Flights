import pandas as pd
import os, json
from datetime import timedelta
from flask import Flask, request

app = Flask(__name__)


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

    def update_flight(self, flight_id: str, arrival, departure):
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

    def is_flight_exist(self, id: str):
        return id in self.data.index

    def save_csv(self):
        copy = self.data.drop("Waiting", axis=1)
        copy["Arrival"] = pd.to_datetime(copy["Arrival"]).dt.strftime("%H:%M")
        copy["Departure"] = pd.to_datetime(copy["Departure"]).dt.strftime("%H:%M")
        copy.to_csv(self.CSV_PATH)


flights = Flights()


@app.get("/")
def index():
    return "Hello! please read the README file"


@app.get("/flight/<id>")
def get_flight(id):
    if not flights.is_flight_exist(id):
        return {"error": "not found"}
    flight = flights.get_flights(id)
    if type(flight) == pd.DataFrame:
        flight = flight.iloc[0]
    flight["Arrival"] = flight["Arrival"].time()
    flight["Departure"] = flight["Departure"].time()
    return json.loads(flight.to_json())


@app.post("/update_flights")
def update_flights():
    for flight in request.json["flights"]:
        flights.update_flight(
            flight["flight ID"], flight["Arrival"], flight["Departure"]
        )
    flights.save_csv()
    return {"message": "success"}


if __name__ == "__main__":
    app.run()
