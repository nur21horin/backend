from fastapi import APIRouter, HTTPException, Query

from app.services.aviationstack import aviation_service

router = APIRouter(
    prefix="/api/flights",
    tags=["Flights"]
)


@router.get("/")
async def get_flights(
    
    flight_number: str | None = None,
    dep_iata: str | None = None,
    arr_iata: str | None = None,
    flight_status: str | None = Query(
        default=None,
        pattern="^(active|scheduled|landed|cancelled|incident|diverted)$"
    ),
    limit: int = Query(default=20, ge=1, le=100)
):

    try:

        data = await aviation_service.get_flights(
            flight_number=flight_number,
            dep_iata=dep_iata,
            arr_iata=arr_iata,
            flight_status=flight_status,
            limit=limit
        )

        return {
            "success": True,
            "pagination": data.get("pagination"),
            "data": data.get("data", [])
        }

    except Exception as error:

        raise HTTPException(
            status_code=502,
            detail=str(error)
        )