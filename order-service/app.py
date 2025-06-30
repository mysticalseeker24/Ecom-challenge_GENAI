from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import uvicorn
import logging.config
import config
from routers import order_router


logging.config.dictConfig(config=config.LOGGING_CONFIG)
logger = logging.getLogger(__name__)

logger.info("Starting order service")

app = FastAPI(
    title="E-Commerce Order Service",
    description="Order service that uses mockapi to provide order related user responses",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        logger.exception("Unhandled exception occurred")
        return JSONResponse(status_code=500, content={"detail": str(exc), "status_code": 500})

app.include_router(order_router.router, prefix="/v1/api")

@app.get("/")
async def root():
    """Root endpoint for order service"""
    return {
        "services":"E-Commerce Order Service",
        "version":"1.0.0",
        "status":"operational"
    }

@app.get("/v1/health")
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status":"healthy"}

@app.get("/health/ready")
async def readiness():
    return {"status": "ready"}

@app.get("/health/live")
async def liveness():
    return {"status": "live"}

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0", port="8002")