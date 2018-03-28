# stellar-faucet

A faucet that can be used to give testnet kin to users

## Prerequisites:
Built to work on python 3.x

Install the dependencies:
```
pip install pipenv
pipenv install
```

## Running the program:
Enter the pipenv shell:
```bash
pipenv shell
```
Run the script  
```
python main.py <TESTNET/MAINNET> <seed to faucet account>
```

## Endpoints:
Success will return http code 200  
Excpected errors will return http code 400  
Unexpected errors will return http code 500

**GET '/status'**  
```
{
'address': 'GBDUPSZP4APH3PNFIMYMTHIGCQQ2GKTPRBDTPCORALYRYJZJ35O2LOBL',
 'network': 'TESTNET',
 'channels': {'all': 1, 'free': 1},
 'horizon': {'online': True,
 	'uri': 'https://horizon-testnet.stellar.org',
 	'error': None},
 'kin_asset': 
 	{
    	'issuer': 'GCKG5WGBIJP74UDNRIRDFGENNIH5Y3KBI5IHREFAJKV4MQXLELT7EX6V',
        'code': 'KIN'
    }
}

OR

{"error" : 'unexpected error: exception message'}  

```

**GET '/fund?account=\<account\>&amount=\<amount\>'**
```
{
'succsseful': True/False
'error': None/'Account does not exist'/'No KIN trustline established'/'Invalid address'/'Amount parameter missing'/'Account parameter missing'/'Invalid amount'
}
```














