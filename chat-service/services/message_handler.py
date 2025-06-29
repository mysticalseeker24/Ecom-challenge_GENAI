import json
import logging
from typing import Dict, Any, Tuple, Optional, List
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from services.service_client import ServiceClient
import config
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from pydantic import BaseModel

# Configure logger
logger = logging.getLogger(__name__)
from pydantic import BaseModel

def serialize_messages(messages):
    return [m.dict() if isinstance(m, BaseModel) else m for m in messages]

def serialize_metadata(metadata):
    if isinstance(metadata, dict):
        return {
            k: v.model_dump() if isinstance(v, BaseModel) else v
            for k, v in metadata.items()
        }
    return metadata

class MessageHandler:
    def __init__(self):
        """Initialize the message handler with an LLM and service clients."""
        self.llm = ChatOpenAI(
            api_key=config.OPENAI_API_KEY,
            model=config.LLM_MODEL,
            temperature=config.LLM_TEMPERATURE,
        )
        
        self.product_service_client = ServiceClient(config.PRODUCT_SEARCH_URL)
        self.order_service_client = ServiceClient(config.ORDER_LOOKUP_URL)
        
        # Intent classification prompt
        self.intent_classification_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an AI assistant for an e-commerce website specializing in musical instruments and related products.
Your task is to classify user queries into one of these categories:
1. PRODUCT_QUERY - Questions about product details, recommendations, comparisons, or features
2. ORDER_QUERY - Questions about order status, history, or details
3. GENERAL_QUERY - General questions that don't fit into the above categories

For ORDER_QUERY, determine if the customer_id is present in the query.

Response format:
{{
  "intent": "[PRODUCT_QUERY|ORDER_QUERY|GENERAL_QUERY]",
  "has_customer_id": true|false,
  "customer_id": "extracted_id_if_present",
  "original_query": "the original user query",
  "requires_customer_id": true|false
}}

The "requires_customer_id" field should be true if:
1. The intent is ORDER_QUERY, AND
2. No customer_id is present in the query

Be precise in your detection and avoid false positives when extracting customer IDs.
Only return the JSON object, no additional text."""),
    ("user", "{user_message}")
        ])
        
        # General query prompt
        self.general_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful e-commerce assistant for a music instrument and related products store.
Respond to general queries in a friendly, concise, and helpful manner.
If the query might be related to products or orders but you're not sure, suggest that the user can ask about specific products or provide their Customer ID to check order status.
Keep responses brief, friendly, and focused on helping the customer."""),
            ("user", "{user_message}")
        ])

    async def handle_message(
        self, 
        messages: List[Dict[str,str]], 
        conversation_id: Optional[str] = None, 
        customer_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, bool, Dict[str, Any], str]:
        """
        Process the incoming message and route to appropriate service
        
        Returns:
            Tuple containing:
            - Response message
            - Whether customer ID is required
            - Metadata
            - Source type (product, order, or general)
        """
        # Combine message with customer_id if available for better context
        
        history = []
        for msg in messages:
            if msg.role == "user":
                history.append(HumanMessage(content=msg.message))
            elif msg.role == "assistant":
                history.append(AIMessage(content=msg.message))

        # Step 2: Collect all user messages into one string
        all_user_messages = " ".join([msg.message for msg in messages if msg.role == "user"])

        # Step 3: Append customer ID if known
        message_with_id = f"{all_user_messages} (Customer ID: {customer_id})" if customer_id else all_user_messages

        # Step 4: Pass the combined message to intent classifier
        intent_data = await self._classify_intent(message_with_id)  
        # Extract customer_id from the message if present and not already provided
        if intent_data.get("has_customer_id", False) and not customer_id:
            customer_id = intent_data.get("customer_id")
        
        # If an order query requires customer_id but none is provided
        if intent_data.get("intent") == "ORDER_QUERY" and intent_data.get("requires_customer_id", False):
            return (
                "I'd be happy to help with your order information. Could you please provide your Customer ID?",
                True,
                {},
                "general"
            )
        
        # Route the query based on intent
        if intent_data.get("intent") == "PRODUCT_QUERY":
            response, metadata = await self._handle_product_query(
                messages, 
                customer_id,
                metadata if metadata else {}
            )
            return response, False, metadata, "product"
            
        elif intent_data.get("intent") == "ORDER_QUERY":
            response, metadata = await self._handle_order_query(
                messages, 
                customer_id,
                metadata if metadata else {}
            )
            return response, False, metadata, "order"
            
        else:
            # Handle general queries
            response = await self._handle_general_query(messages)
            return response, False, {}, "general"

    async def _classify_intent(self, message: str) -> Dict[str, Any]:
        """Classify the intent of the message using the LLM."""
        try:
            intent_classification_chain = self.intent_classification_prompt | self.llm
            result = intent_classification_chain.invoke({"user_message": message})
            
            # Parse the JSON response
            intent_data = json.loads(result.content)
            logger.info(f"Intent classification: {intent_data}")
            return intent_data
            
        except Exception as e:
            logger.error(f"Failed to classify intent: {str(e)}", exc_info=True)
            # Default to general query if classification fails
            return {
                "intent": "GENERAL_QUERY",
                "has_customer_id": False,
                "requires_customer_id": False,
                "original_query": message
            }
    
    async def _handle_product_query(
        self, 
        messages: List[Dict[str,str]], 
        customer_id: Optional[str] = None,
        metadata: Dict[str, Any] = {}
    ) -> Tuple[str, Dict[str, Any]]:
        """Forward product queries to the product search service."""
        try:
            print(self.product_service_client.base_url)
            response = await self.product_service_client.post(
                "/query",
                {
                    "messages": serialize_messages(messages),
                    "customer_id": customer_id,
                    "metadata": serialize_metadata(metadata)
                }
            )
            
            if "response" in response:
                return response["response"], response.get("metadata", {})
            else:
                logger.warning(f"Unexpected product service response: {response}")
                return "I couldn't find information about that product. Can you try asking in a different way?", {}
                
        except Exception as e:
            logger.error(f"Error querying product service: {str(e)}", exc_info=True)
            return "I'm having trouble connecting to our product database right now. Please try again later.", {}
    
    async def _handle_order_query(
        self, 
        messages: List[Dict[str,str]], 
        customer_id: str,
        metadata: Dict[str, Any] = {}
    ) -> Tuple[str, Dict[str, Any]]:
        """Forward order queries to the order lookup service."""
        try:
            response = await self.order_service_client.post(
                "/query",
                {
                    "messages": serialize_messages(messages),
                    "customer_id": customer_id,
                    "metadata": serialize_metadata(metadata)
                }
            )
            
            if "response" in response:
                return response["response"], response.get("metadata", {})
            else:
                logger.warning(f"Unexpected order service response: {response}")
                return "I couldn't find information about your order. Please check your Customer ID and try again.", {}
                
        except Exception as e:
            logger.error(f"Error querying order service: {str(e)}", exc_info=True)
            return "I'm having trouble connecting to our order database right now. Please try again later.", {}
    
    async def _handle_general_query(self, messages: List[Dict[str,str]]) -> str:
        """Handle general queries using the LLM."""
        try:
            general_chain = self.general_prompt | self.llm
            result = general_chain.invoke({"user_message": messages})
            return result.content
            
        except Exception as e:
            logger.error(f"Error handling general query: {str(e)}", exc_info=True)
            return "I'm sorry, I'm having trouble processing your request. How else can I help you today?"