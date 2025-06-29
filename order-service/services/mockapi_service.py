from config import MOCK_API_URL
import httpx

class MockAPI:
    """Service that calls the mockapi and returns the responses"""

    def __init__(self) -> None:
        pass

    async def call_mock_api(self, endpoint, parameters):
        try:
            async with httpx.AsyncClient() as client:
                # Construct the URL based on the endpoint and parameters
                url = f"{MOCK_API_URL}{endpoint}"

                # Handle different endpoint types
                if "/data/customer/" in endpoint:
                    url = f"{MOCK_API_URL}/data/customer/{parameters.get('customer_id')}"
                elif "/data/product-category/" in endpoint:
                    url = f"{MOCK_API_URL}/data/product-category/{parameters.get('category')}"
                elif "/data/order-priority/" in endpoint:
                    url = f"{MOCK_API_URL}/data/order-priority/{parameters.get('priority')}"
                else:
                    # For endpoints without path parameters
                    url = f"{MOCK_API_URL}{endpoint}"
                print(url)
                # Make the API call
                response = await client.get(url)
            
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"Mock API error: {response.status_code} - {response.text}")
                    return None
                
        except Exception as e:
            print(f"Error calling mock API: {str(e)}")
            return None
        
    def get_mockapi_service(self):
        return self