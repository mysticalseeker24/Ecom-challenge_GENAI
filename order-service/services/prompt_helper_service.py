from typing import Dict, Any
from dataclasses import dataclass
from langchain.prompts import ChatPromptTemplate

class PromptHelperService:
    def __init__(self) -> None:
        self.order_query_analysis_prompt = ChatPromptTemplate.from_messages([
            ("system","""You are an AI assistant for an e-commerce website specializing in musical instruments and other products.
            Your task is to analyze customer queries about their orders and determine which API endpoint to call.

            Available API endpoints:
            1. /data/customer/{{customer_id}} - Get all orders for a specific customer
            2. /data/product-category/{{category}} - Get all orders for a specific product category
            3. /data/order-priority/{{priority}} - Get orders with a specific priority (Low, Medium, High, Critical)
            4. /data/total-sales-by-category - Get total sales by product category
            5. /data/high-profit-products - Get high-profit products (default threshold: $100)
            6. /data/shipping-cost-summary - Get shipping cost statistics
            7. /data/profit-by-gender - Get total profit by customer gender

            Analyze the query to determine:
            1. Which API endpoint to call
            2. Any parameters needed for the API call
            3. If filtering of results is needed post-API call

            Response format:
            {{
              "endpoint": "the_endpoint_to_call",
              "parameters": {{"param_name": "param_value"}},
              "post_processing": {{
                "filter_by": ["field_name", "condition", "value"],
                "sort_by": "field_name",
                "sort_order": "asc|desc",
                "limit": number_of_results
              }},
              "query_type": "most_recent|specific_product|all_orders|etc"
            }}

            The "parameters" should include any path parameters needed for the endpoint.
            Only return the JSON object, no additional text. not even ```json```"""
            ),
            ("user", "Customer ID: {customer_id}\nQuery: {query}")
        ])
        self.response_formatting_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful e-commerce assistant. Format the following order data into a friendly, conversational response.
                For dates, format them as "Month Day, Year".
                For monetary values, include the dollar sign and format as currency.
                If asked about most recent orders, make sure to highlight that these are the most recent ones.
                Respond as if you're directly addressing the customer.
                Make the response conversational and helpful.

                Here is the request query: "{query}"
                Here is the customer ID: "{customer_id}"
                Here is the raw data to format:
                {data}

                Format this into a response that answers the customer's query directly and politely."""),
             ("user", "Please format the response.")
        ])


    def get_order_query_analysis_prompt(self):
            return self.order_query_analysis_prompt
        

    def get_response_formatting_prompt(self):
            return self.response_formatting_prompt
        