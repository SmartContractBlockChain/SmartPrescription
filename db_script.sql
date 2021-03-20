USE smartPrescription;

CREATE TABLE users (
     id INT NOT NULL AUTO_INCREMENT,
     name CHAR(30) NOT NULL,
     surname CHAR(30) NOT NULL,
     password varchar(255) NOT NULL,
     userType ENUM('Doctor', 'Pharmacist', 'Patient') NOT NULL,
     blockchainAddress varchar(255) NOT NULL,
     PRIMARY KEY (id)
);

INSERT INTO users(name,surname,password,userType,blockchainAddress)
 VALUES('Peter','McBurney',SHA1('BlockChainIsAwesome'),'Patient','0x8c635509D3154d91E7aE90719a63a46fb8c303c4'),
        ('Abdul','Basit',SHA1('password123'),'Patient','0x280f37D241c4E54b949adD285CE7388af9D422d4'),
        ('Aishik','Ghosh',SHA1('password1234'),'Patient','0xa8bF1D8F84BC30b9417106bfd3ce4a58443538Fd'),
        ('Aya','Khashoggi',SHA1('password12345'),'Pharmacist','0x0daC8768EDD1F72a0b37F8e558A0496DBBfF398a'),
        ('Kajetan','Dymkiewicz',SHA1('$uper$tr0ngP4$$w00rD'),'Doctor','0x8aec3e14459774FDDdd1188796b70c88DC63589A'),
        ('Klaudia','Marciniak',SHA1('Pompom12'),'Doctor','0x961785466649E2f142618d86f9dfCdED227E509E'),
        ('Linfeng','Wang',SHA1('HappyPanda!@#'),'Pharmacist','0x9Ad42ca69eF89897F65b9E27a5B367FbB6c7e3cC'),
        ('Timothee','Heller',SHA1('VivaLaFrance!'),'Doctor','0x92f132ad45AFbF1Db19d37b4FEaB21a7854BbdFF'),
        ('Xiaojin','Sun',SHA1('password123456'),'Pharmacist','0x1B8D0e98E21eE637b6a0e64f374551de6a4f33A8');
