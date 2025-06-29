"""
Main FastAPI application entry point
"""
import logging
from fastapi import FastAPI
from routers.product_router import router as product_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting Product Service...")

app = FastAPI(
    title="E-commerce Product Service", 
    description="Product service that handles product-related queries"
)

# Include routers
app.include_router(product_router)

@app.get("/")
async def root():
    """Root endpoint to check if the service is running."""
    return {"message": "Product Service is running."}

@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)