SET SEARCH_PATH TO projekt;

DROP TABLE client;

CREATE TABLE client(
    id_client BIGSERIAL PRIMARY KEY,
    fname VARCHAR(20),
    lname VARCHAR(30),
    age INT,
    address VARCHAR(30),
    email VARCHAR(40),
    login VARCHAR(20),
    password VARCHAR(64)
);

-- password: password
INSERT INTO client (fname, lname, age, address, email, login, password) VALUES
    ('Test', 'User', -1, 'localhost', 'example@email.com', 'user', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');

-- password: He11o
INSERT INTO client (fname, lname, age, address, email, login, password) VALUES
    ('Adam', 'Kubacki', 19, '30-100 Krakow', 'adamKub@gmail.com', 'adamczycha', '7144ef0ab2fd42660eeec67e468702775810a6474c3f397c533eed7405b6cdb3');

SELECT * FROM client;

DELETE FROM client WHERE id_client > 2;