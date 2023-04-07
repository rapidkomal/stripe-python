import os
from flask import Flask, render_template, request, jsonify
import stripe

stripe_keys = {
  'secret_key': os.getenv('STRIPE_PUBLIC_KEY'),
  'publishable_key': os.getenv('STRIPE_SECRET_KEY')
}
#pk_test_51MtsqOSJDcfPOfrVtZItVFkrrino5kiki8sc3TvylEwxHHiJzPte3FXIhjWJ70ANLDq8sZDZCvWTcygT4r1zAVM700iqeTrVDr
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
    domain_url = "http://127.0.0.1:5000/"
    stripe.api_key = stripe_keys["secret_key"]

    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [payment_intent_data] - capture the payment later
        # [customer_email] - prefill the email input in the form
        # For full details see https://stripe.com/docs/api/checkout/sessions/create

        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        # checkout_session = stripe.checkout.Session.create(
        #     success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
        #     cancel_url=domain_url + "cancelled",
        #     payment_method_types=["card"],
        #     mode="payment",
        #     line_items=[
        #         {
        #             "name": "T-shirt",
        #             "quantity": 1,
        #             "currency": "usd",
        #             "amount": "2000",
        #         }
        #     ]
        # )
        product = stripe.Product.create(
        name='T-shirt',
        description='Comfortable cotton t-shirt',
        # images=['https://example.com/t-shirt.png'],
        )

        price = stripe.Price.create(
        product=product.id,
        unit_amount=500,
        currency='inr',
        )
        print(price)
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price.id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            # success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
            # cancel_url=domain_url + "cancelled",
            success_url='http://localhost:5000/success',
            cancel_url='http://localhost:5000/cancel',
        )
        return jsonify({"sessionId":  session.id})
        # return jsonify({'id': session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403
    
# @app.route('/')
# def index():
#     return render_template('index.html', key=stripe_keys['publishable_key'])

# @app.route('/charge', methods=['POST'])
# def charge():
#     # Amount in cents
#     amount = 100
#     print("amount: ", amount)
#     customer = stripe.Customer.create(
#         email='customer@example.com',
#         source=request.form['stripeToken']
#     )
#     print("customer: ", customer)
#     charge = stripe.Charge.create(
#         customer=customer.id,
#         amount=amount,
#         currency='usd',
#         description='Flask Charge'
#     )
#     print("charge: ", charge)
    
#     return render_template('charge.html', amount=amount)

if __name__ == '__main__':
    app.run(debug=True)