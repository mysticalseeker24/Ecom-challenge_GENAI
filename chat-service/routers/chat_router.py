from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging
from services.message_handler import MessageHandler

# Configure logger
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(tags=["chat"])

# Initialize message handler
message_handler = MessageHandler()

class MessageItem(BaseModel):
    role: str  # "self" or "ai"
    message: str

class ChatRequest(BaseModel):
    messages: list[MessageItem]
    conversation_id: Optional[str] = None
    customer_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    requires_customer_id: bool = False
    conversation_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    source_type: Optional[str] = "general"  # 'product', 'order', or 'general'

@router.post("/chat", response_model=ChatResponse)
async def handle_chat(chat_request: ChatRequest):
    """
    Main endpoint to process user chat messages and route to appropriate services
    """
    try:
        logger.info(f"Received chat request: {len(chat_request.messages)}... messages")
        
        response, requires_id, metadata, source_type = await message_handler.handle_message(
            chat_request.messages,
            chat_request.conversation_id,
            chat_request.customer_id,
            chat_request.metadata
        )
        
        return ChatResponse(
            response=response,
            requires_customer_id=requires_id,
            conversation_id=chat_request.conversation_id,
            metadata=metadata,
            source_type=source_type
        )
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Chat processing error: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}