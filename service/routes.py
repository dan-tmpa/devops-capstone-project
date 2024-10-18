"""
Account Service

This microservice handles the lifecycle of Accounts
"""
# pylint: disable=unused-import
from flask import jsonify, request, make_response, abort, url_for   # noqa; F401
from service.models import Account
from service.common import status  # HTTP Status Codes
from . import app  # Import Flask application


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
            # paths=url_for("list_accounts", _external=True),
        ),
        status.HTTP_200_OK,
    )

######################################################################
# CREATE A NEW ACCOUNT
######################################################################
@app.route("/accounts", methods=["POST"])
def create_accounts():
    """
    Creates an Account
    This endpoint will create an Account based the data in the body that is posted
    """
    app.logger.info("Request to create an Account")
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    message = account.serialize()
    # Uncomment once get_accounts has been implemented
    # location_url = url_for("get_accounts", account_id=account.id, _external=True)
    location_url = "/"  # Remove once get_accounts has been implemented
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# LIST ALL ACCOUNTS
######################################################################

@app.route("/accounts", methods=["GET"])
def list_accounts():
    """
    List all Accounts
    This endpoint will list all Accounts
    """
    app.logger.info("Request to list Accounts")
    accounts = Account.all()
    accounts_list = []
    for account in accounts:
        accounts_list.append(account.serialize())
    app.logger.info("%s accounts being returned.", len(accounts_list))
    
    # use the Account.all() method to retrieve all accounts
    # create a list of serialize() accounts
    # log the number of accounts being returned in the list 
    # return the list with a return code of status.HTTP_200_OK
    return jsonify(accounts_list), 200


######################################################################
# READ AN ACCOUNT
######################################################################

@app.route("/accounts/<int:id>", methods=["GET"])
def read_account(id):
    """
    Read an Account
    This endpoint will read an Account based on the data in the body that is posted.
    """
    app.logger.info("Request to read an Account with id: %s", id)
    account = Account.find(id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{id}] could not be found.")
    
    return account.serialize(), status.HTTP_200_OK


######################################################################
# UPDATE AN EXISTING ACCOUNT
######################################################################

@app.route("/accounts/<int:id>", methods=["PUT"])
def update_accounts(id):
    """
    Update an Account
    This endpoint will update an Account based on the posted data
    """
    app.logger.info("Request to update an Account with id: %s", id)
    account = Account.find(id)

    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{id}] could not be found.")

    account.deserialize(request.get_json())
    account.update()

    return account.serialize(), status.HTTP_200_OK

######################################################################
# DELETE AN ACCOUNT
######################################################################
@app.route("/accounts/<int:id>", methods=["DELETE"])
def delete_accounts(id):
    """
    Delete an Account
    This endpoint will delete an Account based on the account_id that is requested
    """
    app.logger.info("Request to delete an Account with id: %s", id)
    account = Account.find(id)
    if account:
        account.delete()
    else:
        abort(status.HTTP_405_METHOD_NOT_ALLOWED, "Method not allowed")

    # use the Account.find() method to retrieve the account by the account_id
    # if found, call the delete() method on the account
    # return and empty body ("") with a return code of status.HTTP_204_NO_CONTENT

    return "", status.HTTP_204_NO_CONTENT


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )
