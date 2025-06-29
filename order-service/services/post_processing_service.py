from typing import Dict, Any
from datetime import datetime
import re
import pandas as pd


class PostProcessingService:
    def __init__(self) -> None:
        pass

    def apply_post_processing(self, api_data, post_processing: Dict[str, Any], query_type: str):
        """
        Apply post-processing filters to the API response data
        """
        if not api_data or not post_processing:
            # If this is a "most recent" query and we have a list of orders
            if query_type == "most_recent" and isinstance(api_data, list):
                # Convert string dates to datetime objects for sorting
                for item in api_data:
                    if "Order_Date" in item:
                        try:
                            item["Order_Date_dt"] = datetime.strptime(item["Order_Date"], "%Y-%m-%d")
                        except:
                            item["Order_Date_dt"] = datetime.min

                # Sort by date (descending) and get the most recent
                sorted_data = sorted(api_data, key=lambda x: x.get("Order_Date_dt", datetime.min), reverse=True)
                return sorted_data[:1] if sorted_data else []
            return api_data

        # Convert to DataFrame for easier filtering and sorting
        df = pd.DataFrame(api_data if isinstance(api_data, list) else [api_data])
        if df.empty:
            return api_data

        # Apply filtering if specified
        filter_by = post_processing.get("filter_by")
        if filter_by and len(filter_by) == 3:
            field, condition, value = filter_by
            if field in df.columns:
                if condition == "equals":
                    df = df[df[field] == value]
                elif condition == "contains":
                    df = df[df[field].str.contains(value, case=False, na=False)]
                elif condition == "greater_than":
                    df = df[df[field] > value]
                elif condition == "less_than":
                    df = df[df[field] < value]

        # Apply sorting if specified
        sort_by = post_processing.get("sort_by")
        sort_order = post_processing.get("sort_order", "desc")
        if sort_by and sort_by in df.columns:
            df = df.sort_values(by=sort_by, ascending=(sort_order.lower() == "asc"))

        # Apply limit if specified
        limit = post_processing.get("limit")
        if limit and isinstance(limit, int) and limit > 0:
            df = df.head(limit)

        # Special handling for "most_recent" query type
        if query_type == "most_recent":
            if "Order_Date" in df.columns:
                df["Order_Date_dt"] = pd.to_datetime(df["Order_Date"], errors="coerce")
                df = df.sort_values(by="Order_Date_dt", ascending=False)
                df = df.head(1)

        # Convert back to records format
        return df.to_dict(orient="records")
