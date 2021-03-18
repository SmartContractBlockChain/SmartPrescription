USE smartPrescription;

CREATE TABLE users (
     id INT NOT NULL AUTO_INCREMENT,
     name CHAR(30) NOT NULL,
     surname CHAR(30) NOT NULL,
     password varchar(255) NOT NULL,
     userType ENUM('Doctor', 'Pharmacist', 'Patient') NOT NULL,
     blockchainAddress varchar(255) DEFAULT NULL,
     PRIMARY KEY (id)
);

INSERT INTO users(name,surname,password,userType) VALUES('John','Smith',MD5('password123'),'Patient');
