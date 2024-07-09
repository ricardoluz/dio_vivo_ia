from fastapi import FastAPI
from fastapi_pagination import LimitOffsetPage, add_pagination,paginate
from workout_api.routers import api_router

app = FastAPI(title='WorkoutApi')
app.include_router(api_router)
add_pagination(app)
