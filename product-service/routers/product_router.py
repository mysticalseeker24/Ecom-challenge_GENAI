"""
Router for product-related endpoints
"""
import logging
from fastapi import APIRouter, Depends
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
from typing import Dict, Any, Optional

from services.product_service import ProductService

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/products",
    tags=["products"]
)

class ProductQueryRequest(BaseModel):
    messages: list[Dict[str, str]]
    metadata: Optional[Dict[str, Any]] = None
    customer_id: Optional[str] = None

class ProductQueryResponse(BaseModel):
    response: str
    metadata: Optional[Dict[str, Any]] = None

def get_product_service():
    """Dependency injection for product service"""
    return ProductService()

@router.post("/query", response_model=ProductQueryResponse)
async def handle_product_query(
    request: ProductQueryRequest,
    product_service: ProductService = Depends(get_product_service)
):
    """
    Process product-related queries using RAG and LLM
    """
    try:
        logger.info(f"Received query: {request.messages}")
        
        response = await run_in_threadpool(
            product_service.handle_query,
            request.messages,
            request.customer_id,
            request.metadata
        )
        
        return ProductQueryResponse(
            response=response["answer"],
            metadata={"query": request.messages}
        )
    except Exception as e:
        logger.error(f"Error handling product query: {str(e)}", exc_info=True)
        return ProductQueryResponse(
            response="I'm sorry, I encountered an issue while retrieving product information. Please try again later.",
            metadata={"error": str(e)}
        )