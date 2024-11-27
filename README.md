Rasa E-commerce Chatbot 🤖🛒
Welcome to the Rasa E-commerce Chatbot! This is a conversational AI bot built using Rasa, designed to help users with various e-commerce tasks such as product searches, bargaining for better prices, order tracking, and much more. It supports multiple languages, including English 🇬🇧 and Hindi 🇮🇳.

🏗️ Project Structure
The project is organized as follows:

bash
Copy code
rasa_ecommerce_chatbot/
├── actions/
│   ├── __init__.py
│   ├── actions.py       # Contains custom action logic and API integration
│   ├── custom_executor  # Custom executor for handling special action logic
│   ├── custom_actions.py # Contains specific custom actions
├── data/
│   ├── nlu.yml          # NLU training data
│   ├── stories.yml      # Stories for training
│   ├── rules.yml        # Rules for fallback and other basic behaviors
├── models/              # Generated Rasa models
├── domain.yml           # Rasa domain configuration
├── config.yml           # Pipeline and policy configuration
├── credentials.yml      # Channel credentials
├── endpoints.yml        # Endpoint configurations
├── tests/
│   ├── test_stories.yml # Test stories for bot evaluation
└── README.md            # Project documentation
📂 Key Components
Actions (actions/): Contains custom actions that interact with external APIs, process data, and make dynamic decisions based on user input.

Data (data/): This folder contains the necessary training data for NLU (Natural Language Understanding), stories for conversation flow, and fallback rules.

Models (models/): Stores the Rasa models generated after training, which are used to predict intents and entities.

Domain (domain.yml): Defines the structure of the chatbot, including intents, entities, actions, slots, and responses. It also includes multilingual support.

Configuration (config.yml, endpoints.yml): These files contain configurations for the Rasa pipeline (e.g., NLU model, dialogue policies) and endpoints (e.g., custom action server, APIs).

Testing (tests/): Includes test stories to evaluate how well the chatbot performs in various real-world scenarios.

🚀 Functionalities
1. Product Information 🛍️
Get product details: Users can ask for details about any product, including price, description, and an image.
The bot fetches this information dynamically from an external API.
If a product is not found or there is an issue fetching the details, the bot provides appropriate error messages.
Example:
User: "Tell me about the iPhone 14."
Bot: "Here is the detail of iPhone 14: Price: $999.99. Description: The latest model of iPhone with enhanced features. [Image of iPhone]."
2. Bargaining 🤝💰
Negotiate prices: Users can bargain for a better price. The bot offers a discount based on the current discount percentage, but ensures the price does not go below a minimum allowed price.
The bot increments the discount and offers a new price after each negotiation attempt.
Example:
User: "I want to buy the iPhone 14, but the price is too high."
Bot: "The current price for iPhone 14 is $999.99. I can offer it to you for $949.99. Does that work for you?"
3. Order Tracking 📦🚚
Track your order: Users can track their orders using an Order ID (e.g., ORD123).
The bot validates the order ID format and fetches the status of the order from a simulated API.
If the user enters the wrong order ID multiple times, the bot will guide them to contact support.
Example:
User: "Where is my order ORD123?"
Bot: "Your order is currently 'Out for Delivery' and is expected to be delivered by 2024-11-28."
4. Fallback Handling 🚨
Fallback Responses: When the bot doesn't understand the user's request, it provides a fallback message with a list of available options.
The fallback responses are customizable for both English and Hindi users.
Example:
User: "I want to buy something."
Bot: "I'm sorry, I didn't quite catch that. 😅 Here are some things I can help you with: 1️⃣ Track your order 2️⃣ Bargain for a better price 3️⃣ Check product details."
🛠️ Custom Actions
1. ActionFetchProductDetails 📄
This custom action fetches product details such as title, price, description, and image from an external API.
Handles both successful responses and error handling in case the product is not found.
2. ActionBargainLogic 💸
Implements the bargaining logic. It calculates the discount for a product and suggests a new price.
Ensures the new price doesn't fall below a minimum threshold, making sure the deal is still profitable.
3. ActionTrackOrder 🗂️
The bot requests the Order ID from the user, validates the format, and fetches the current order status (Shipped, Delivered, etc.).
Provides the expected delivery date if the order is out for delivery.
4. ActionFallbackWithMenu ❓
Handles fallback scenarios when the bot fails to understand the user’s request.
Provides a menu of options that the user can choose from, such as tracking orders, bargaining, or viewing product details.
⚙️ Configuration
domain.yml
Defines the intents, actions, slots, and responses used by the bot. It also handles multilingual responses, including English and Hindi.

config.yml
Contains the pipeline configuration for natural language understanding (NLU), including the components such as tokenizers, intent classifiers, and entity extractors. It also defines dialogue policies.

endpoints.yml
Defines the endpoints for the bot’s action server, API integrations, and external services.

🧪 Testing and Evaluation
Test Stories: The project includes test stories that simulate different conversation scenarios to ensure the bot behaves as expected.
Unit Tests: Unit tests can be written to ensure that custom actions, such as product fetching and order tracking, work as expected.
🚀 How to Run
Prerequisites
Install the necessary dependencies:

bash
Copy code
pip install -r requirements.txt
Train the Rasa model:


rasa train
Start the action server:


rasa run actions
Start the Rasa shell (for testing in terminal):

rasa shell
Alternatively, you can integrate the bot with different channels such as Facebook Messenger, Slack, or use Rasa's REST API.

💡 Future Improvements
Enhanced Product API Integration: Integrate with more sophisticated product APIs for better product recommendations and dynamic pricing.
Expand Language Support: Add more languages to make the chatbot accessible to a wider audience.
AI-Powered Bargaining: Implement AI-based bargaining strategies to offer smarter price negotiations.
📜 License
This project is licensed under the MIT License. See the LICENSE file for more details.

🤝 Contributions
We welcome contributions! If you'd like to help improve this bot, feel free to open an issue or create a pull request.

This README provides an overview of the Rasa E-commerce Chatbot project, including setup instructions, features, and how to get started. Let me know if you need further details or clarification. Happy coding! 😄