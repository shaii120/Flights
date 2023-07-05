# bondIT Test

## Guide
1. Run the following command to activate the server:
`flask --app flights run`

2. To get an information about a flight go to the following path:
/flight/*\<flight_id>*
3. To update a flight use POST at the path: 
/update_flights \
Use the following JSON structre:
```
{
    "flights" : [
        {
            "flight_id": id,
            "arrival": "HH:MM",
            "departure": "HH:MM"
        },
        ...
    ]
}
```
example:
```
{
    "flights" : [
        {
            "flight_id": "A123",
            "arrival": "12:34",
            "departure": "23:45"
        }
    ]
}
```