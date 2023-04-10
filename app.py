import os
from flask import Flask, render_template, request, jsonify
import stripe

stripe_keys = {
  'secret_key': os.getenv('STRIPE_PUBLIC_KEY'),
  'publishable_key': os.getenv('STRIPE_SECRET_KEY')
}

stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__ ,static_url_path='/static')


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/cancelled")
def cancelled():
    return render_template("cancelled.html")

@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)

@app.route("/create-checkout-session")
def create_checkout_session():
    stripe.api_key = stripe_keys["secret_key"]

    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [payment_intent_data] - capture the payment later
        # [customer_email] - prefill the email input in the form

        product = stripe.Product.create(
        name='T-shirt',
        description='Comfortable cotton t-shirt',
        )

        price = stripe.Price.create(
        product=product.id,
        unit_amount=500,
        currency='inr',
        )
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price.id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=f'{os.getenv('LOCAL_URL')}success',
            cancel_url=f'{os.getenv('LOCAL_URL')}cancel',
        )
        return jsonify({"sessionId":  session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403
    
if __name__ == '__main__':
    app.run(debug=True)