import json
import sys

from flask import Flask, request
from flask_cors import CORS
import kin
from kin import errors as kin_errors

app = Flask(__name__)
CORS(app)


@app.route("/status")
def status():
    # Return sdk status in json, if fails, returns the exception
    try:
        return json.dumps(sdk.get_status()), 200
    except Exception as e:
        response = {'error': 'unexpected error: ' + str(e)}
        return json.dumps(response), 500


@app.route("/fund")
def fund():
    # Funds an account with <amount> kin , if fails, returns the corresponding error message

    destination = request.args.get('account')
    amount = request.args.get('amount')

    if destination is None:
        return make_reply(400, 'Account parameter missing')
    if amount is None:
        return make_reply(400, 'Amount parameter missing')

    # Verify amount is a number
    try:
        amount = float(amount)
    except ValueError:
        return make_reply(400, 'Invalid amount')
    except Exception as e:
        return make_reply(500, 'unexpected error: {}'.format(str(e)))

    # Fund the account
    try:
        sdk.send_kin(destination, amount)
        return make_reply(200)

    # If the account is not created yet
    except kin_errors.AccountNotFoundError:
        return make_reply(400, 'Account does not exist')

    # If the account has no trustline
    except kin_errors.AccountNotActivatedError:
        return make_reply(400, 'No KIN trustline established')

    except Exception as e:
        if 'invalid address' in str(e):
            return make_reply(400, 'Invalid address')
        # If i get an unexpected error, return it
        else:
            return make_reply(500, 'unexpected error: {}'.format(str(e)))


def make_reply(status, error=None):
    # Build json reply and return it + HTTP code
    success = True if status == 200 else False
    reply = {'success': success,
             'error': error}
    return json.dumps(reply), status


def main():
    global sdk
    sdk = kin.SDK(network=sys.argv[1],
                  secret_key=sys.argv[2])
    app.run()


if __name__ == '__main__':
    main()
