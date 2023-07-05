import unittest
import flights
import pandas as pd


class TestFlights(unittest.TestCase):
    def setUp(self):
        self.flights = flights.Flights()

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
        self.flights.insert_flight(flight_id, arrival, departure)

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
        self.flights.insert_flight(flight_id, arrival, departure)
        self.assertEqual(self.flights.get_flights(flight_id)["success"], "success")
