from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.image import Image
from models.user import User
from models.transaction import Transaction
from helpers import get_client_token, create_transaction
from braintree.successful_result import SuccessfulResult
from flask_login import current_user
# import requests

transactions_blueprint = Blueprint('transactions',
                            __name__,
                            template_folder='templates')

@transactions_blueprint.route('/new', methods=['GET'])
def new(image_id):
    return render_template('transactions/new.html', client_token=get_client_token(), image_id=image_id)

@transactions_blueprint.route('/', methods=['POST'])
def create(image_id):
    data = request.form
    image = Image.get_by_id(image_id)

    result = create_transaction(data.get("amount"), data.get("payment_method_nonce"))
    print(type(result))
    if type(result) == SuccessfulResult:
        new_transaction = Transaction(amount=data.get("amount"), image=image, user_id=current_user.id)
        if new_transaction.save():

            # If want to use mailgun api
            # from app import app
            # requests.post(
            #   "https://api.mailgun.net/v3/<YOUR_DOMAIN_NAME>/messages",
            #   auth=("api", app.config.get("MAILGUN_API") ),
            #   data={"from": "Mailgun Sandbox <YOUR_DOMAIN_NAME>",
            #     "to": "Your Name <DOMAIN_EMAIL>",
            #     "subject": "Hello",
            #     "text": "Successfully donated"})

            flash("Transactions successfull", "success")
            return redirect(url_for("users.show", username=image.user.username ))
        else:
            flash("Could not save transaction", "danger")
            return redirect(url_for("users.show", username=image.user.username )) 
    else:
        flash("Could not create braintree transaction", "danger")
        return redirect(url_for("users.show", username=image.user.username )) 