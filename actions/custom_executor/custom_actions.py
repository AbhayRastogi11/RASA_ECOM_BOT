import logging
import requests
from typing import List, Dict, Any

logger = logging.getLogger(__name__)
API_ENDPOINT = "https://fakestoreapi.com/products"

def set_language(tracker):
    intent_name = tracker.latest_message['intent'].get('name', '')
    
    # Check if the intent name ends with '_hin' (case-sensitive)
    if intent_name.endswith('_hin'):
        logger.info(f"Inside: Intent ends with '_hin' - {intent_name}")
        return '_hin'
    else:
        logger.info(f"Inside else: Intent doesn't end with '_hin' - {intent_name}")
        return ''


# def fetch_product_details_from_api(query: str):
#     """
#     Fetch product details from the API based on the product query.
#     Handles exceptions in case of errors during the API request.
#     """
#     try:
#         response = requests.get(API_ENDPOINT)
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         products = response.json()

#         # Search for matching products
#         matching_products = [
#             product for product in products if query.lower() in product['title'].lower()
#         ]
        
#         if matching_products:
#             return matching_products[0]  # Return the first matching product
#         else:
#             return None  # No match found

#     except requests.exceptions.RequestException as e:
#         # Handle any exceptions (network issues, API errors, etc.)
#         return {"error": f"API request failed: {str(e)}"}


from fuzzywuzzy import fuzz, process

API_ENDPOINT = "https://fakestoreapi.com/products"  # Your API endpoint

def fetch_product_details_from_api(product_name: str):
    """
    Fetch product details from the API based on the product name.
    Uses fuzzy matching to find the closest product title.
    Handles API exceptions and returns product details or error messages.
    """
    try:
        # Send request to API
        response = requests.get(API_ENDPOINT)
        response.raise_for_status()  # Check if the request was successful

        # Parse response JSON
        products = response.json()

        # List to hold the products' titles
        product_titles = [product['title'] for product in products]

        # Use fuzzywuzzy to get the closest matches for the product_name
        best_match, score = process.extractOne(product_name, product_titles, scorer=fuzz.partial_ratio)

        # If the match score is sufficiently high (e.g., above 70), consider it a valid match
        if score >= 70:  # You can adjust the threshold as needed
            # Find the product with the best match
            matching_product = next(product for product in products if product['title'] == best_match)
            
            # Return product details
            return {
                'title': matching_product['title'],
                'price': matching_product['price'],
                'description': matching_product['description'],
                'image': matching_product['image']
            }
        else:
            # Return error if no suitable match is found
            return {"error": f"No product found matching '{product_name}'."}

    except requests.exceptions.RequestException as e:
        # Handle any exceptions related to the API request
        return {"error": f"API request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}



def fetch_product_details_from_api_bargain(product_name: str) -> Dict:
    """
    Fetch product details from the FakeStore API based on product title.
    This function includes exception handling for the API request.
    """
    try:
        # Make the API request with a timeout of 5 seconds
        response = requests.get(API_ENDPOINT, timeout=5)
        response.raise_for_status()

        products = response.json()

        # Search for the product by title (case-insensitive)
        for product in products:
            if product_name.lower() in product['title'].lower():
                return product  # Return the matching product details

        return {}  # Return an empty dictionary if no product is found

    except requests.exceptions.RequestException as e:
        # Return an error message if the request fails
        return {"error": f"Error fetching product details: {str(e)}"}
