# stellar-faucet

A faucet that can be used to give testnet kin to users

## Prerequisites:
1. Edit the 'seeds.txt' file with the seeds and channels you wish to use
```
main seed  
channel seed 2  
channel seed 3  
channel seed 4  
channel seed 5  
.  
.  
.
```
2. Edit the docker-compose.yaml file and update the number of seeds (default 9)

## Run locally:
1. Install [docker and docker-compose](https://docs.docker.com/install/)
2. Inside this project's folder, run the command
```bash
$ sudo docker-compose up
```
The faucet will run on localhost:5000

## Deploy to a remote machine:
(This assumes that the remote machine has ubuntu 16+ installed)  
1. Install [ansible](http://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
2. Install the [angstwad.docker_ubuntu](https://github.com/angstwad/docker.ubuntu) role:
```bash
$ ansible-galaxy install angstwad.docker_ubuntu -p playbook/roles/
```
3. Edit the 'hosts' file inside ```playbook/inventory``` and add the IPs of the remote machines
4. Run the playbook:
```bash
$ ansible-playbook -i playbook/inventory/ playbook/main.yml
```
The faucet will run on <ip>:5000

## Endpoints:
Success will return http code 200  
Excpected errors will return http code 400  
Unexpected errors will return http code 500

**GET '/status'**  
```
{
'address': 'GBDUPSZP4APH3PNFIMYMTHIGCQQ2GKTPRBDTPCORALYRYJZJ35O2LOBL',
 'network': 'TESTNET',
 'channels': {'all': 8, 'free': 8},
 'horizon': {'online': true,
 	'uri': 'https://horizon-testnet.stellar.org',
 	'error': null},
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
'succsseful': true/false
'error': null/'Account does not exist'/'No KIN trustline established'/
         'Invalid address'/'Amount parameter missing'/'Account parameter missing'/'Invalid amount'/
         'unexcpected error: exception message'
}
```

