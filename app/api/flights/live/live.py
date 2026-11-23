from fastapi import APIRouter, HTTPException, Query

from app.services.aviationstack import aviation_service

router = APIRouter(
    prefix="/api/flights",
    tags=["Live Flight Tracking"]
)


@router.get("/live")
async def get_live_flights(
    limit: int = Query(default=100, ge=1, le=100)
):
    try:
        response = await aviation_service.get_flights(
            flight_status="active",
            limit=limit
        )

        flights = response.get("data", [])
        live_flights = []
        seen_aircraft = set()

        for flight in flights:

            live = flight.get("live")

            if not live:
                continue

            latitude = live.get("latitude")
            longitude = live.get("longitude")

            if latitude is None or longitude is None:
                continue

            if not (-90 <= latitude <= 90):
                continue

            if not (-180 <= longitude <= 180):
                continue

            aircraft = flight.get("aircraft") or {}

            registration = aircraft.get("registration")
            icao24 = aircraft.get("icao24")

            # Avoid duplicate aircraft caused by codeshare flights
            aircraft_key = icao24 or registration

            if aircraft_key and aircraft_key in seen_aircraft:
                continue

            if aircraft_key:
                seen_aircraft.add(aircraft_key)

            departure = flight.get("departure") or {}
            arrival = flight.get("arrival") or {}
            airline = flight.get("airline") or {}

            live_flights.append({
                "flight_number": (
                    flight.get("flight") or {}
                ).get("iata"),

                "airline": airline.get("name"),

                "departure": departure.get("iata"),
                "arrival": arrival.get("iata"),

                "latitude": latitude,
                "longitude": longitude,

                "altitude": live.get("altitude"),
                "speed": live.get("speed_horizontal"),
                "direction": live.get("direction"),

                "registration": registration,
                "icao24": icao24,

                "updated": live.get("updated")
            })

        return {
            "success": True,
            "total_fetched": len(flights),
            "live_count": len(live_flights),
            "data": live_flights
        }

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=str(error)
        )