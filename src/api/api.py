from ninja import NinjaAPI
from api.clients.views import router as cts_router

api = NinjaAPI(
    title="Banking project API",
    description="API for Banking project web application.",
)
api.add_router("/clients", cts_router)
