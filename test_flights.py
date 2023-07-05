import unittest
import flights
import pandas as pd
import shutil, os


class TestFlights(unittest.TestCase):
    def setUp(self):
        self.flights = flights.Flights()
        shutil.copyfile(self.flights.CSV_PATH, f"{self.flights.CSV_PATH}.backup")

    def tearDown(self) -> None:
        os.remove(self.flights.CSV_PATH)
        os.rename(f"{self.flights.CSV_PATH}.backup", self.flights.CSV_PATH)

    def flight_series(self, flight_id, arrival, departure, success):
        flight = pd.Series(
            data={
                "Arrival": pd.to_datetime(arrival, format="%H:%M"),
                "Departure": pd.to_datetime(departure, format="%H:%M"),
                "success": success,
            },
            name=flight_id,
        )
        return flight

    def test_insert_flight(self):
        flight_id = "TST1"
        arrival = "12:34"
        departure = "23:45"
        flight = self.flight_series(flight_id, arrival, departure, "success")
        self.flights.update_flight(flight_id, arrival, departure)

        pd.testing.assert_series_equal(self.flights.get_flights(flight_id), flight)

    def test_get_flights(self):
        flight_id = "C26"
        arrival = "08:00"
        departure = "17:00"
        flight = self.flight_series(flight_id, arrival, departure, "’’")

        pd.testing.assert_series_equal(self.flights.get_flights(flight_id), flight)

    def test_anlayze_success_flights(self):
        flight_id = "TST1"
        arrival = "08:00"
        departure = "17:00"

        self.assertEqual(self.flights.get_flights("A19")["success"], "’’")
        self.flights.anlayze_success_flights()
        self.assertEqual(self.flights.get_flights("A19")["success"], "fail")
        self.assertEqual(self.flights.get_flights("B35")["success"], "success")
        self.flights.update_flight(flight_id, arrival, departure)
        self.assertEqual(self.flights.get_flights(flight_id)["success"], "success")

    def test_api_index(self):
        tester = flights.app.test_client(self)
        response = tester.get("/")
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_api_get_flight(self):
        tester = flights.app.test_client(self)
        response = tester.get("/flight/B39")
        self.assertTrue(b"Arrival" in response.data)

    def test_api_update_flights(self):
        tester = flights.app.test_client(self)
        flight = {
            "flights": [{"flight ID": "A123", "Arrival": "12:34", "Departure": "23:45"}]
        }
        response = tester.post("/update_flights", json=flight)
        self.assertTrue(b"message" in response.data)


if __name__ == "__main__":
    unittest.main()
