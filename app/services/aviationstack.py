import httpx

from app.core.config import settings


class AviationStackService:

    def __init__(self):

        self.base_url = settings.AVIATIONSTACK_BASE_URL

        self.api_key = settings.AVIATIONSTACK_API_KEY

    async def get_flights(
        self,
        flight_number: str | None = None,
        flight_status: str | None = None,
        dep_iata: str | None = None,
        arr_iata: str | None = None,
        limit: int = 20
    ):

        if not self.api_key:
            raise ValueError("Aviationstack API key is missing")

        params = {
            "access_key": self.api_key,
            "limit": limit
        }

        if flight_number:
            params["flight_number"] = flight_number
        
        if flight_status:
            params["flight_status"] = flight_status

        if dep_iata:
            params["dep_iata"] = dep_iata

        if arr_iata:
            params["arr_iata"] = arr_iata

        async with httpx.AsyncClient(timeout=30.0) as client:

            response = await client.get(
                f"{self.base_url}/flights",
                params=params
            )

            response.raise_for_status()

            data = response.json()

            if "error" in data:
                raise ValueError(data["error"])

            return data


aviation_service = AviationStackService()