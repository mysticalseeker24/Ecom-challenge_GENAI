from datetime import datetime
from typing import Any
import json
import numpy as np


class ResponseFormatterService:
    def __init__(self) -> None:
        pass

    async def format_response(self, query: str, customer_id: str, data: Any, response_formatting_prompt: Any, llm: Any) -> str:
        """
        Format the API response data into a user-friendly message
        """
        try:
            # Custom JSON encoder to handle various data types
            class CustomJSONEncoder(json.JSONEncoder):
                def default(self, obj):
                    # Handle datetime objects
                    if isinstance(obj, datetime):
                        return obj.isoformat()

                    # Handle pandas/numpy NaN
                    if pd.isna(obj):
                        return None

                    # Handle numpy numeric types
                    if isinstance(obj, (np.integer, np.floating)):
                        return obj.item()

                    # Handle numpy arrays
                    if isinstance(obj, np.ndarray):
                        return obj.tolist()

                    # Let the base class default method handle other types
                    return super().default(obj)

            # Serialize the data to JSON with custom encoder
            json_data = json.dumps(data, cls=CustomJSONEncoder, ensure_ascii=False)

            # Use LLM to format the response
            formatting_chain = response_formatting_prompt | llm
            formatting_result = formatting_chain.invoke({
                "query": query,
                "customer_id": customer_id,
                "data": json_data
            })

            return formatting_result.content
        except Exception as e:
            print(f"Error formatting response: {str(e)}")
            # Improved fallback response
            try:
                if isinstance(data, list) and len(data) > 0:
                    item = data[0]
                    details = []
                    if 'Order_Date' in item:
                        details.append(f"ordered on {datetime.strptime(item['Order_Date'], '%Y-%m-%d').strftime('%B %d, %Y')}")
                    if 'Product_Category' in item:
                        details.append(f"category: {item['Product_Category']}")
                    if 'Sales' in item:
                        details.append(f"amount: ${float(item['Sales']):.2f}")
                    return f"I found your order ({' '.join(details)}) but had trouble formatting details. Please contact support for more information."
            except Exception as fallback_error:
                print(f"Fallback formatting failed: {str(fallback_error)}")
            return "I found your order information but had trouble formatting it. Please check your account or contact support."
