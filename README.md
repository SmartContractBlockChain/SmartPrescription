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

____
### DB integration

1 install mysql (https://www.mysql.com/downloads/)

2 login to mysql console 
```
sudo mysql -u root -p
```
3 create db user
```
CREATE USER 'SCBC'@'localhost' IDENTIFIED BY 'SCBC_PASS';
```
4 create db
```
CREATE DATABASE smartPrescription;
```
5 grant privilages
```
GRANT ALL PRIVILEGES ON smartPrescription.* TO 'SCBC'@'localhost';
```
6 install mysql connector
```
conda install -c anaconda mysql-connector-python 
```

7 run db_script.sql in IDE or in mysql console 

8 run flask
```
python db_integration.py
```
9 go to http://127.0.0.1:5000/ and see if you obtain data from db
