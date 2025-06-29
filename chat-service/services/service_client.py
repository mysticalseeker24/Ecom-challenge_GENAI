import httpx
import logging
import asyncio
import json
from typing import Dict, Any, Optional
import config

logger = logging.getLogger(__name__)

class ServiceClient:
    """
    Client for making HTTP requests to microservices
    with built-in retry and error handling
    """
    
    def __init__(
        self, 
        base_url: str, 
        timeout: int = config.HTTP_TIMEOUT,
        max_retries: int = config.HTTP_RETRIES
    ):
        """
        Initialize the service client
        
        Args:
            base_url: Base URL of the service
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.max_retries = max_retries
        
        # Initialize transport limits
        self.limits = httpx.Limits(
            max_keepalive_connections=5,
            max_connections=10,
            keepalive_expiry=30.0
        )
    
    async def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a POST request to the service
        
        Args:
            endpoint: API endpoint path
            data: Request payload
            
        Returns:
            Response data as dictionary
        """
        url = f"{self.base_url}{endpoint}"
        logger.debug(f"Making POST request to {url}")
        
        for attempt in range(self.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self.timeout, limits=self.limits) as client:
                    response = await client.post(
                        url,
                        json=data,
                        headers={"Content-Type": "application/json"}
                    )
                    
                    # Handle HTTP status codes
                    if response.status_code == 200:
                        return response.json()
                    else:
                        error_msg = f"Service returned {response.status_code}: {response.text}"
                        logger.error(error_msg)
                        
                        # Retry on server errors
                        if response.status_code >= 500 and attempt < self.max_retries:
                            await self._backoff(attempt)
                            continue
                            
                        # Return error details if available
                        try:
                            error_data = response.json()
                            return {
                                "error": error_data.get("detail", error_msg),
                                "status_code": response.status_code
                            }
                        except json.JSONDecodeError:
                            return {
                                "error": error_msg,
                                "status_code": response.status_code
                            }
                        
            except (httpx.RequestError, httpx.TimeoutException) as e:
                logger.error(f"Request failed: {str(e)}")
                
                if attempt < self.max_retries:
                    await self._backoff(attempt)
                else:
                    return {
                        "error": f"Service unavailable after {self.max_retries} attempts: {str(e)}",
                        "status_code": 503
                    }
                
        # This should never happen but just in case
        return {
            "error": "Request failed",
            "status_code": 500
        }
        
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a GET request to the service
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            Response data as dictionary
        """
        url = f"{self.base_url}{endpoint}"
        logger.debug(f"Making GET request to {url}")
        
        for attempt in range(self.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self.timeout, limits=self.limits) as client:
                    response = await client.get(
                        url,
                        params=params
                    )
                    
                    # Handle HTTP status codes
                    if response.status_code == 200:
                        return response.json()
                    else:
                        error_msg = f"Service returned {response.status_code}: {response.text}"
                        logger.error(error_msg)
                        
                        # Retry on server errors
                        if response.status_code >= 500 and attempt < self.max_retries:
                            await self._backoff(attempt)
                            continue
                            
                        # Return error details if available
                        try:
                            error_data = response.json()
                            return {
                                "error": error_data.get("detail", error_msg),
                                "status_code": response.status_code
                            }
                        except json.JSONDecodeError:
                            return {
                                "error": error_msg,
                                "status_code": response.status_code
                            }
                        
            except (httpx.RequestError, httpx.TimeoutException) as e:
                logger.error(f"Request failed: {str(e)}")
                
                if attempt < self.max_retries:
                    await self._backoff(attempt)
                else:
                    return {
                        "error": f"Service unavailable after {self.max_retries} attempts: {str(e)}",
                        "status_code": 503
                    }
                
        # This should never happen but just in case
        return {
            "error": "Request failed",
            "status_code": 500
        }
    
    async def _backoff(self, attempt: int) -> None:
        """
        Implements exponential backoff strategy for retries
        
        Args:
            attempt: Current attempt number (0-based)
        """
        backoff_time = min(0.1 * (2 ** attempt), 5)  # Cap at 5 seconds
        logger.info(f"Retrying in {backoff_time:.2f} seconds...")
        await asyncio.sleep(backoff_time)