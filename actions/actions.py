# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from typing import Any, Text, Dict, List
import requests
import logging
import random
from rasa_sdk import Action, Tracker,  FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from actions.custom_executor.custom_actions import set_language,fetch_product_details_from_api,fetch_product_details_from_api_bargain

logger = logging.getLogger(__name__)


class ActionFetchProductDetails(Action):
    def name(self) -> str:
        return "action_fetch_product_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> list:
        
        # Set the language based on the intent
        language = set_language(tracker)

        # Get the product name from the slot
        entities = tracker.latest_message.get('entities', [])
        logger.info(f"entities:{entities}")
        # product_name = tracker.get_slot("product_name")
        # logger.info(f"product_name:{product_name}")
        # Iterate over entities and find the 'product_name' entity
        for entity in entities:
            if entity['entity'] == 'product_name':  # Specify the entity you want to extract
                product_name = entity['value']
        logger.info(f"product_name:{product_name}")
        if not product_name:
            if language == '_hin':
                dispatcher.utter_message(text="कृपया मुझे उस उत्पाद का नाम बताएं जिसमें आप रुचि रखते हैं।")
            else:
                dispatcher.utter_message(text="Could you tell me the name of the product you're interested in?")
            return []

        # Call the API function to fetch product details (assuming you have implemented this function)
        product_details = fetch_product_details_from_api(product_name)
        
        if "error" in product_details:
            if language == '_hin':
                dispatcher.utter_message(text=f"मुझे उत्पाद विवरण प्राप्त करने में समस्या हुई। त्रुटि: {product_details['error']}")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't fetch the product details. Error: {product_details['error']}")
            return []

        if not product_details:
            if language == '_hin':
                dispatcher.utter_message(text=f"मुझे '{product_name}' से मेल खाता हुआ कोई उत्पाद नहीं मिला।")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find a product matching '{product_name}'.")
            return []

        # Extract product data
        original_price = product_details['price']
        title = product_details['title']
        description = product_details['description']
        image = product_details['image']

        # Prepare the response
        if language == '_hin':
            dispatcher.utter_message(
                text=f"यह हैं '{title}' का विवरण:\n"
                     f"कीमत: ₹{original_price:.2f}\n"
                     f"विवरण: {description}",
                image=image
            )
        else:
            dispatcher.utter_message(
                text=f"Here is the detail of '{title}':\n"
                     f"Price: ${original_price:.2f}\n"
                     f"Description: {description}",
                image=image
            )

        return []



class action_bargain_logic(Action):
    def name(self) -> Text:
        return "action_bargain_logic"

    def calculate_discount(self, original_price: float, current_discount: int, minimum_price: float) -> float:
        """
        Calculate the next bargaining price based on current discount and constraints.
        """
        next_discount = current_discount + 5  # Increment discount by 5%
        discounted_price = original_price * (1 - next_discount / 100)
        return max(discounted_price, minimum_price)

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> list:
        
        # Set the language based on the intent
        language = set_language(tracker)

        # Get the product name from the slot
        product_name = tracker.get_slot("product_name")

        if not product_name:
            if language == '_hin':
                dispatcher.utter_message(text="कृपया मुझे उस उत्पाद का नाम बताएं जिसमें आप रुचि रखते हैं।")
            else:
                dispatcher.utter_message(text="Could you tell me the name of the product you're interested in?")
            return []

        # Call the API function to fetch product details (assuming you have implemented this function)
        product_details = fetch_product_details_from_api_bargain(product_name)
        
        if "error" in product_details:
            if language == '_hin':
                dispatcher.utter_message(text=f"मुझे उत्पाद विवरण प्राप्त करने में समस्या हुई। त्रुटि: {product_details['error']}")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't fetch the product details. Error: {product_details['error']}")
            return []

        if not product_details:
            if language == '_hin':
                dispatcher.utter_message(text=f"मुझे '{product_name}' से मेल खाता हुआ कोई उत्पाद नहीं मिला।")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find a product matching '{product_name}'.")
            return []

        # Extract product data
        original_price = product_details['price']
        title = product_details['title']
        description = product_details['description']
        minimum_price = original_price * 0.8  # Minimum price: 80% of the original price

        # Handle bargaining logic
        current_discount = tracker.get_slot("current_discount") or 0
        current_discount = int(current_discount)
        next_price = self.calculate_discount(original_price, current_discount, minimum_price)

        # Prepare the response
        if next_price > minimum_price:
            if language == '_hin':
                dispatcher.utter_message(
                    text=f"'{title}' की वर्तमान कीमत ${original_price:.2f} है। "
                         f"मैं इसे ${next_price:.2f} में दे सकता हूँ। क्या यह आपको ठीक लगता है?"
                )
            else:
                dispatcher.utter_message(
                    text=f"The current price for '{title}' is ${original_price:.2f}. "
                         f"I can offer it for ${next_price:.2f}. Does this work for you?"
                )
        else:
            if language == '_hin':
                dispatcher.utter_message(
                    text=f"'{title}' के लिए मैं जो न्यूनतम कीमत दे सकता हूँ वह ${minimum_price:.2f} है। यह एक बेहतरीन डील है! क्या आप आगे बढ़ना चाहेंगे?"
                )
            else:
                dispatcher.utter_message(
                    text=f"The lowest price I can offer for '{title}' is ${minimum_price:.2f}. It's a great deal! Let me know if you'd like to proceed."
                )

        # Update discount slot for next round
        return [{"slot_name": "current_discount", "value": current_discount + 5}]


# Global variable to track the number of attempts for each user
attempt_counter = {}

class ActionTrackOrder(FormValidationAction):
    def name(self) -> Text:
        return "track_order_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["order_id"]

    def validate_order_id(self, order_id: Text) -> bool:
        """
        Validate the order ID against the expected format: ORD123 (not case-sensitive).
        """
        return bool(re.match(r"^ord\d{3}$", order_id.lower()))

    def fetch_order_status(self, order_id: Text) -> Dict:
        """
        Simulate fetching order details dynamically based on order ID.
        """
        statuses = ["Shipped", "Out for Delivery", "Delivered", "Processing"]
        random_status = random.choice(statuses)
        if random_status == "Delivered":
            return {
                "status": random_status,
                "delivery_date": f"2024-11-{random.randint(20, 26)}",
            }
        elif random_status == "Shipped":
            return {
                "status": random_status,
                "expected_delivery": f"2024-12-{random.randint(1, 5)}",
            }
        elif random_status == "Out for Delivery":
            return {
                "status": random_status,
                "expected_delivery": f"2024-11-{random.randint(27, 29)}",
            }
        else:
            return {"status": random_status, "expected_delivery": "TBD"}

    def validate(self, slot_values: Dict[Text, Any], dispatcher: CollectingDispatcher,
                 tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        global attempt_counter

        order_id = slot_values.get("order_id")
        language = set_language(tracker)

        # Initialize attempt counter for a user
        user_id = tracker.sender_id
        if user_id not in attempt_counter:
            attempt_counter[user_id] = 0

        # Check if the order ID is valid
        if not order_id:
            if language == '_hin':
                dispatcher.utter_message(text="कृपया अपना ऑर्डर आईडी दर्ज करें (फॉर्मेट: ORD123)।")
            else:
                dispatcher.utter_message(text="Please enter your Order ID in the format ORD123.")
            return {"order_id": None}

        if not self.validate_order_id(order_id):
            attempt_counter[user_id] += 1

            if attempt_counter[user_id] >= 3:
                if language == '_hin':
                    dispatcher.utter_message(
                        text="आपने कई बार गलत ऑर्डर आईडी दर्ज की है। कृपया सहायता के लिए हमारे सपोर्ट से संपर्क करें। 🙁"
                    )
                else:
                    dispatcher.utter_message(
                        text="You have entered the wrong Order ID multiple times. Please contact support for help. 🙁"
                    )
                # Reset attempt counter for this user
                attempt_counter[user_id] = 0
                return []

            if language == '_hin':
                dispatcher.utter_message(text="ऑर्डर आईडी फॉर्मेट गलत है। कृपया फॉर्मेट: ORD123 का पालन करें।")
            else:
                dispatcher.utter_message(text="The Order ID format is invalid. Please use the format ORD123.")
            return {"order_id": None}

        # Reset the counter on successful entry
        attempt_counter[user_id] = 0
        return {"order_id": order_id}

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> None:
        order_id = tracker.get_slot("order_id")
        language = set_language(tracker)

        if order_id:
            order_details = self.fetch_order_status(order_id)

            if order_details:
                if "delivery_date" in order_details:
                    if language == '_hin':
                        dispatcher.utter_message(
                            text=f"ऑर्डर {order_id.upper()} को {order_details['delivery_date']} को डिलीवर किया गया है।"
                        )
                    else:
                        dispatcher.utter_message(
                            text=f"Order {order_id.upper()} has been delivered on {order_details['delivery_date']}."
                        )
                elif "expected_delivery" in order_details:
                    if language == '_hin':
                        dispatcher.utter_message(
                            text=f"ऑर्डर {order_id.upper()} वर्तमान में '{order_details['status']}' है और {order_details['expected_delivery']} तक डिलीवर होने की उम्मीद है।"
                        )
                    else:
                        dispatcher.utter_message(
                            text=f"Order {order_id.upper()} is currently '{order_details['status']}' "
                                 f"and is expected to be delivered by {order_details['expected_delivery']}."
                        )
                else:
                    if language == '_hin':
                        dispatcher.utter_message(
                            text=f"ऑर्डर {order_id.upper()} वर्तमान में '{order_details['status']}' है।"
                        )
                    else:
                        dispatcher.utter_message(
                            text=f"Order {order_id.upper()} is currently '{order_details['status']}'."
                        )
            else:
                if language == '_hin':
                    dispatcher.utter_message(text=f"मुझे ऑर्डर आईडी {order_id.upper()} के लिए कोई विवरण नहीं मिला।")
                else:
                    dispatcher.utter_message(text=f"Sorry, we could not find any details for Order ID: {order_id.upper()}.")


class ActionFallbackWithMenu(Action):

    def name(self) -> Text:
        return "action_fallback_with_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Set the language based on the intent
        language = set_language(tracker)

        # Retrieve the last user message for context
        user_message = tracker.latest_message.get("text", "")

        # Construct a friendly response with emojis and options in a single message
        if language == '_hin':
            response = (
                "मुझे खेद है, मैं ठीक से समझ नहीं पाया। 😅\n\n"
                "यहाँ कुछ चीज़ें हैं जिनमें मैं आपकी मदद कर सकता हूँ:\n"
                "• *अपना ऑर्डर ट्रैक करें*: अपने ऑर्डर की स्थिति चेक करें।\n"
                "• *बेहतर कीमत के लिए मोलभाव करें*: आइए बात करें! 🤝\n"
                "• *उत्पाद विवरण देखें*: किसी उत्पाद पर अधिक जानकारी प्राप्त करें। 🛒\n"
                "• *हमारी वेबसाइट पर जाएं*: और अधिक उत्पाद और विवरण ब्राउज़ करें। 🌐\n\n"
                "अधिक जानकारी के लिए, आप हमारी [वेबसाइट](https://example.com) पर जा सकते हैं।"
            )
        else:
            response = (
                "I'm sorry, I didn't quite catch that. 😅\n\n"
                "Here are some things I can help you with:\n"
                "• *Track your order*: Check the status of your order.\n"
                "• *Bargain for a better price*: Let's negotiate! 🤝\n"
                "• *Check product details*: Get more information on a product. 🛒\n"
                "• *Visit our website*: Browse more products and details. 🌐\n\n"
                "For more details, you can visit our [website](https://example.com)."
            )
        
        # Send the crafted message using a single dispatcher call
        dispatcher.utter_message(text=response)
        
        # Optionally log user input for further analysis (for debugging)
        dispatcher.utter_message(text=f"Just for context, your message was: \"{user_message}\".")
        
        return []
