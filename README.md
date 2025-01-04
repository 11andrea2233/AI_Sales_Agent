TechNerds Sales Assistant

Overview

The TechNerds Sales Assistant is an advanced AI-powered chatbot designed to facilitate efficient and effective sales interactions. Utilizing state-of-the-art machine learning models and integrating various utility tools, this sales assistant enhances customer service by providing tailored product recommendations, scheduling meetings, and processing payments.

Features

Intelligent Interaction: Leverages the groq/llama3-70b-8192 model for understanding and generating natural language responses, ensuring a seamless conversation with users.

Integrated Tools:

GenerateCalendlyInvitationLink: Schedules meetings directly through Calendly to enhance engagement with potential clients.

GetStoreInfo: Retrieves essential information about store locations and availability.

GetProductRecommendation: Offers personalized product recommendations based on user inquiries and preferences.

GenerateStripePaymentLink: Facilitates instant payment processing via Stripe, improving the checkout process
.
Environmentally Aware: Utilizes environment variables to manage sensitive data securely and efficiently.

Color-coded Conversations: Enhances user experience with color-coded text outputs, making interactions intuitive and user-friendly.

Customizable and Versatile: Supports multiple LLM (Language Learning Models) options, allowing for flexibility depending on specific needs or computational resources.


Purpose


This sales assistant is designed to optimize the sales process by:


Enhancing user engagement through quick and relevant responses.

Streamlining appointment scheduling and payment processes.

Providing accurate product recommendations and store information.


Who Can Use This?


Sales Teams: To augment their customer handling capacity and reduce response times.

E-commerce Platforms: To provide 24/7 support and enhance customer shopping experience.

Small to Medium Businesses (SMBs): To leverage AI capabilities for improving sales without the overhead of large teams.


Agent Tools


get_store_info: This leverages RAG search to retrieve general information about the TechNerds business, services, and products. All informations are retrieved from the docs files/Docs.txt.

get_product_recommendation: Uses an expert product recommendation agent to find the best products the store can offer based on customer requirements.

generate_calendly_invitation_link: Provide a link for scheduling a consultation with a tech expert through Calendly.

generate_stripe_payment_link: Create a Stripe payment link for customer purchases.


Getting Started:


Requirements:



Python 3.9+

Calendly API key

Stripe API key

Groq API key

Necessary Python libraries (listed in requirements.txt)

Langchain API Key

Google API Key

OpenAI API Key



SETUP

1. Clone the repo:
     git clone https://github.com/11andrea2233/AI_Sales_Agent.git

2. Create and activate a virtual environment

     python -m venv venv
     venv\Scripts\activate

3. Install the required packages:

    pip install -r requirements.txt

4. Setup the environment variables:

   Create a .env file in the root directory of the project and add your API keys:
   
      GROQ_API_KEY="you-key-here"
   
      CALENDLY_API_KEY="you-key-here"
   
      CALENDLY_EVENT_TYPE_UUID="you-key-here"
   
      STRIPE_API_KEY="you-key-here"
   
      LANGFUSE_SECRET_KEY="you-key-here"
   
      LANGFUSE_PUBLIC_KEY="you-key-here"
   
      LANGFUSE_HOST="you-key-here"
   
      LANGCHAIN_ENDPOINT="you-key-here"
   
      LANGCHAIN_API_KEY="you-key-here"
   
      LANGCHAIN_PROJECT="you-key-here"
   
      GOOGLE_API_KEY="you-key-here"
   
      OPENAI_API_KEY="you-key-here"


Running the application

1. To run the project, you must create the product database:

    python create_database.py

2. Run the sales bot

    python main.py
