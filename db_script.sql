USE smartPrescription;

CREATE TABLE users (
     id INT NOT NULL AUTO_INCREMENT,
     name CHAR(30) NOT NULL,
     surname CHAR(30) NOT NULL,
     password varchar(255) NOT NULL,
     userType ENUM('Doctor', 'Pharmacist', 'Patient') NOT NULL,
     blockchainAddress VARCHAR(255) NOT NULL,
     PRIMARY KEY (id)
);

CREATE TABLE prescriptions (
    id INT NOT NULL AUTO_INCREMENT,
    address VARCHAR(255) NOT NULL,
    doctor_id INT NOT NULL,
    patient_id INT NOT NULL,
    pharmacist_id INT,
    PRIMARY KEY (id)
);

INSERT INTO users(name,surname,password,userType,blockchainAddress)
 VALUES('Peter','McBurney',SHA1('BlockChainIsAwesome'),'Patient','0x4D79c8fa25f8bA5CF960028e2D17D7cd01d7b23F'),
        ('Abdul','Basit',SHA1('password123'),'Patient','0x280f37D241c4E54b949adD285CE7388af9D422d4'),
        ('Aishik','Ghosh',SHA1('password1234'),'Patient','0xa8bF1D8F84BC30b9417106bfd3ce4a58443538Fd'),
        ('Aya','Khashoggi',SHA1('password12345'),'Pharmacist','0x9d60DE24D1603B09bF1252235f17AaBAaE2314ee'),
        ('Kajetan','Dymkiewicz',SHA1('$uper$tr0ngP4$$w00rD'),'Doctor','0xD92abf7FcdB40960667D0390dB33f42281d67864'),
        ('Klaudia','Marciniak',SHA1('Pompom12'),'Doctor','0x961785466649E2f142618d86f9dfCdED227E509E'),
        ('Linfeng','Wang',SHA1('HappyPanda!@#'),'Pharmacist','0x9Ad42ca69eF89897F65b9E27a5B367FbB6c7e3cC'),
        ('Timothee','Heller',SHA1('VivaLaFrance!'),'Doctor','0x92f132ad45AFbF1Db19d37b4FEaB21a7854BbdFF'),
        ('Xiaojin','Sun',SHA1('password123456'),'Pharmacist','0x1B8D0e98E21eE637b6a0e64f374551de6a4f33A8');

INSERT INTO prescriptions(address, doctor_id, patient_id) VALUES ('0x3A7cF9Ce0b09DfF06d7808053F275De52b49cBb8',5,1);

SELECT address as 'prescription address'
FROM users JOIN prescriptions ON doctor_id = users.id
WHERE users.name = 'Kajetan' and surname = 'Dymkiewicz' and userType ='Doctor';

SELECT blockchainAddress FROM users
WHERE users.name = 'Kajetan' AND users.surname = 'Dymkiewicz' AND users.userType = 'Doctor';

SELECT name, surname,blockchainAddress FROM users WHERE userType = 'Pharmacist';

SELECT * FROM prescriptions;
