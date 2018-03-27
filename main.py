import json
import sys

from flask import Flask, request
import kin
from kin import errors as kin_errors


app = Flask(__name__)


@app.route("/status")
def status():
    # Return sdk status in json, if fails, returns the exception
    try:
        return str(json.dumps(sdk.get_status())), 200
    except Exception as e:
        return str(e), 500


@app.route("/fund")
def fund():
    # Funds an account with <amount> kin , if fails, returns the corresponding error message

    destination = request.args.get('account')
    amount = request.args.get('amount')
    response = send_kin(destination,amount)
    data = {'successful': True if response[1] == 200 else False,
            'error': response[0]}
    json_response = json.dumps(data)

    return json_response, response[1]


def send_kin(destination,amount):
    # Verify that I got both variables
    if destination is None:
        return 'No account', 400
    if amount is None:
        return 'No amount', 400

    # Verify amount is a number
    try:
        amount = float(amount)
    except ValueError:
        return 'Invalid amount', 400
    except Exception as e:
        return 'unexpected error: {}'.format(str(e)), 500

    # Fund the account
    try:
        sdk.send_kin(destination, amount)
        return None, 200

    # If the account is not created yet
    except kin_errors.AccountNotFoundError:
        return 'Account does not exist', 400

    # If the account has no trustline
    except kin_errors.AccountNotActivatedError:
        return 'No KIN trustline established', 400

    except Exception as e:
        if 'invalid address' in str(e):
            return 'Invalid address', 400
        # If i get an unexpected error, return it
        else:
            return 'unexpected error: {}'.format(str(e)), 500


def main():
    global sdk
    sdk = kin.SDK(network='TESTNET',
                  secret_key=sys.argv[1])
    app.run()

if __name__ == '__main__':
    main()
