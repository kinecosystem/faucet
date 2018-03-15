from flask import Flask, request
import kin
import json
import sys

app = Flask(__name__)


@app.route("/status")
def status():
    # Return sdk status in json, if fails, returns the exception
    try:
        return str(sdk.get_status())
    except Exception as e:
        return str(e)

@app.route("/fund")
def fund():
    # Funds an account with 4000 kin , if fails, returns the corresponding error message

    destination = request.args.get('account')
    response = send_kin(destination)
    data = {}
    data['successful'] = response[0]
    data['error'] = response[1]
    json_response = json.dumps(data)

    return json_response

def send_kin(destination):
    try:
        # Kin SDK does not throw an exception for no trust/not activated,
        # so I need to check that before

        if not sdk.check_account_exists(destination):
            return False,"Account does not exist"

        if not sdk.check_account_activated(destination):
            return False,"No KIN trustline established"


        sdk.send_kin(destination, 4000)
        return True,None

    except Exception as e:
        if 'invalid address' in str(e):
            return False,'Invalid address'
        # If i get an unexcpected error, return it
        else:
            return False,'unexpcted error: {}'.format(str(e))

def main():
    global sdk
    sdk = kin.SDK(network='TESTNET',
                  secret_key=sys.argv[1])
    app.run()

if __name__ == '__main__':
    main()
