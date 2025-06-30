"""
Main FastAPI application entry point
"""

import logging
from fastapi import FastAPI, Request
from routers.product_router import router as product_router
from fastapi.responses import JSONResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting Product Service...")

app = FastAPI(
    title="E-commerce Product Service",
    description="Product service that handles product-related queries",
)

# Include routers
app.include_router(product_router, prefix="/v1/api")


@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        logger.exception("Unhandled exception occurred")
        return JSONResponse(
            status_code=500, content={"detail": str(exc), "status_code": 500}
        )


@app.get("/")
async def root():
    """Root endpoint to check if the service is running."""
    return {"message": "Product Service is running."}


@app.get("/v1/health")
@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "ok"}


@app.get("/health/ready")
async def readiness():
    return {"status": "ready"}


@app.get("/health/live")
async def liveness():
    return {"status": "live"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
