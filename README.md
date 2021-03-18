# SmartPrescription

1 Install ganache either desktop (https://www.trufflesuite.com/ganache) or command line version ```npm install -g
 ganache-cli``` or ```yarn global add ganache-cli```

2 create virtual env. using conda:
```
conda create --name smartPrescription python=3.9
```
3 activate virtual env:
```
conda activate smartPrescription
```
4 install web3:
```
conda install web3
```
5 install  solx:
```
conda install py-solc-x
```
6 activate local blockchain either via cmd or by desktop application and make sure its running on port 8545
To do it by command line: 
```
 ganache-cli  
```
7 Run ganache integration script to deploy and obtain data from test smartcontract
```
python ganache_integration.py
```
