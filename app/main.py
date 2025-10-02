from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.db.init_db import initialize_database
from app.exercises.ex1.router import router as ex1_router
from app.exercises.ex2.router import router as ex2_router
from app.exercises.ex3.router import router as ex3_router
from app.exercises.ex4.router import router as ex4_router
from app.exercises.ex5.router import router as ex5_router
from app.exercises.ex6.router import router as ex6_router
from app.exercises.ex7.router import router as ex7_router
from app.exercises.ex8.router import router as ex8_router
from app.exercises.ex9.router import router as ex9_router
from app.exercises.ex10.router_v1 import router as ex10_v1_router
from app.exercises.ex10.router_v2 import router as ex10_v2_router
from app.exercises.ex11.router import router as ex11_router
from app.exercises.ex12.router import router as ex12_router

app = FastAPI(title="API Security Exercises", version="0.1.0")


@app.on_event("startup")
def on_startup() -> None:
    initialize_database()


@app.get("/")
def read_root() -> JSONResponse:
    return JSONResponse({
        "message": "Welcome to API Security Exercises",
        "routes": [
            {"exercise": "ex1", "path": "/ex1"},
            {"exercise": "ex2", "path": "/ex2"},
            {"exercise": "ex3", "path": "/ex3"},
            {"exercise": "ex4", "path": "/ex4"},
            {"exercise": "ex5", "path": "/ex5"},
            {"exercise": "ex6", "path": "/ex6"},
            {"exercise": "ex7", "path": "/ex7"},
            {"exercise": "ex8", "path": "/ex8"},
            {"exercise": "ex9", "path": "/ex9"},
            {"exercise": "ex10 v1", "path": "/ex10/v1"},
            {"exercise": "ex10 v2", "path": "/ex10/v2"},
            {"exercise": "ex11", "path": "/ex11"},
            {"exercise": "ex12", "path": "/ex12"},
        ],
        "docs": "/docs",
    })


# Mount separate routers under a single server
app.include_router(ex1_router, prefix="/ex1", tags=["exercise-1"])
app.include_router(ex2_router, prefix="/ex2", tags=["exercise-2"])
app.include_router(ex3_router, prefix="/ex3", tags=["exercise-3"])
app.include_router(ex4_router, prefix="/ex4", tags=["exercise-4"])
app.include_router(ex5_router, prefix="/ex5", tags=["exercise-5"])
app.include_router(ex6_router, prefix="/ex6", tags=["exercise-6"])
app.include_router(ex7_router, prefix="/ex7", tags=["exercise-7"])
app.include_router(ex8_router, prefix="/ex8", tags=["exercise-8"])
app.include_router(ex9_router, prefix="/ex9", tags=["exercise-9"])
app.include_router(ex10_v1_router, prefix="/ex10/v1", tags=["exercise-10-v1"])
app.include_router(ex10_v2_router, prefix="/ex10/v2", tags=["exercise-10-v2"])
app.include_router(ex11_router, prefix="/ex11", tags=["exercise-11"])
app.include_router(ex12_router, prefix="/ex12", tags=["exercise-12"])
