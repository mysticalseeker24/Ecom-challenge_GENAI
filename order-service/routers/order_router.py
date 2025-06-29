from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from services.prompt_helper_service import PromptHelperService
from services.llm_service import LLMService
from services.order_service import OrderService

router = APIRouter(
    prefix="/orders",
    tags=["order"],
    responses={404:{"description":"Not found"}}
)

class MessageItem(BaseModel):
    role: str  # "user" or "assistant"
    message: str

class OrderQueryRequest(BaseModel):
    messages: List[MessageItem] 
    conversation_id: Optional[str] = None
    customer_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class OrderQueryResponse(BaseModel):
    response: str
    requires_customer_id: bool = False
    conversation_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    source_type: Optional[str] = "general" 

def get_order_service():
    return OrderService()


@router.post("/query", response_model=OrderQueryResponse)
async def handle_order_query(
    request: OrderQueryRequest,
    order_service: OrderService = Depends(get_order_service)
):
    """Processes order-related queries and fetch data from the mock API"""
    try:
        customer_id = request.customer_id
        if not customer_id:
            return OrderQueryResponse(
                response="I'd be happy to help with your order information. Could you please provide your Customer ID?"
            )
        
        user_messages = [m for m in request.messages if m.role == "user"]
        if not user_messages:
            raise HTTPException(status_code=400, detail="No user message found in the input.")

        user_query = user_messages[-1].message
        print(f"Received query: {user_query}")

        # 1. Process the order query using order service
        result = await order_service.process_order_query(customer_id, user_query)
        return OrderQueryResponse(**result)
    
    except Exception as e:
        print("Error proccessing query")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
    

@router.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status":"ok"}