from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.flights import router as flight_router
from app.api.flights.live.live import router as live_flight_router


app = FastAPI(
    title="AeroVision API",
    description="Global Flight Tracking and Aviation Intelligence Platform",
    version="1.0.0"
)


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
        "https://backend-zeta-mocha-62.vercel.app/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(flight_router)
app.include_router(live_flight_router)


@app.get("/")
async def root():

    return {
        "project": "AeroVision",
        "status": "running"
    }


@app.get("/api/health")
async def health():

    return {
        "status": "healthy"
    }