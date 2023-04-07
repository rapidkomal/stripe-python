from flask import Flask, render_template, url_for, request, abort
import stripe
import os
from dotenv import load_dotenv
load_dotenv() 

app = Flask(__name__)
print("os.getenv('STRIPE_PUBLIC_KEY') os.getenv('STRIPE_PUBLIC_KEY'): ", os.getenv('STRIPE_PUBLIC_KEY'))
app.config['STRIPE_PUBLIC_KEY'] = os.getenv('STRIPE_PUBLIC_KEY') #'YOUR_STRIPE_PUBLIC_KEY'
app.config['STRIPE_SECRET_KEY'] = os.getenv('STRIPE_SECRET_KEY') #'YOUR_STRIPE_SECRET_KEY'

stripe.api_key = app.config['STRIPE_SECRET_KEY']

@app.route('/test')
def test():
    # customer = stripe.Customer.create(
    # name="John Doe",
    # email="john.doe@example.com",
    # phone="555-1234",
    # address={
    #     "line1": "123 Main St",
    #     "line2": "Apt 4",
    #     "city": "Anytown",
    #     "state": "CA",
    #     "country": "US",
    #         "postal_code": "12345"
    #     }
    # )
    # print(customer)
    
    # charge = stripe.Charge.create(
    #     amount=1000,
    #     currency="usd",
    #     description="Example charge",
    #     customer=customer.id
    # )

    # print("data"*10, charge)

    data = stripe.PaymentIntent.create(amount=500, currency="gbp", payment_method="pm_card_visa")
    print("data"*10, str(data))
    return "success"
@app.route('/')
def get_list():
    charges = stripe.Charge.list(limit=10)
    all_charge = []
    for charge in charges:
        print(charge)
        all_charge.append(charge)
    return str(all_charge)


if __name__=='__main__':
    app.run(host="0.0.0.0", debug = True)