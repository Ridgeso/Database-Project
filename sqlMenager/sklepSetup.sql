SET SEARCH_PATH TO projekt;

-- Tabele
CREATE TABLE kategorie
(
    id_kategorii INT PRIMARY KEY,
    nazwa        VARCHAR(32) NOT NULL
);

CREATE TABLE podkategoria
(
    id_podkat    INT PRIMARY KEY,
    id_kategorii INT,
    nazwa        VARCHAR(32) NOT NULL
);

CREATE TABLE produkt_opis
(
    id_opisu  INT PRIMARY KEY,
    producent VARCHAR(30) NOT NULL,
    opis      text        NOT NULL
);

CREATE TABLE produkty
(
    id_produktu  INT PRIMARY KEY,
    nazwa        VARCHAR(48)    NOT NULL,
    cena         decimal(10, 2) NOT NULL,
    id_opisu     INT,
    id_podkat    INT,
    specyfikacja TEXT
);

CREATE TABLE magazyn
(
    id_magazynu INT PRIMARY KEY,
    nazwa       VARCHAR(20) NOT NULL,
    adres       VARCHAR(32)
);

CREATE TABLE stan_magazynu
(
    id_magazynu INT,
    id_produktu INT,
    ilosc       INT
);

CREATE TABLE opinie
(
    id_opini    INT PRIMARY KEY,
    ocena       INT         NOT NULL,
    urzytkownik VARCHAR(32) NOT NULL,
    opinia      text
);

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

ALTER TABLE podkategoria
    ADD FOREIGN KEY (id_kategorii) REFERENCES kategorie (id_kategorii);

ALTER TABLE produkty
    ADD FOREIGN KEY (id_opisu) REFERENCES produkt_opis (id_opisu);
ALTER TABLE produkty
    ADD FOREIGN KEY (id_podkat) REFERENCES podkategoria (id_podkat);

ALTER TABLE stan_magazynu
    ADD FOREIGN KEY (id_magazynu) REFERENCES magazyn (id_magazynu);
ALTER TABLE stan_magazynu
    ADD FOREIGN KEY (id_produktu) REFERENCES produkty (id_produktu);


INSERT INTO produkt_opis VALUES (1, 'Kingston FURY', 'Pamięć RAM DDR4 Kingston FURY Beast Black 32 GB' ||
'Zmodernizuj swój system dzięki stylowej i niezwykle wydajnej pamięci RAM DDR4 Kingston FURY Beast Black.' ||
'Dwa moduły o łącznej pojemności 32 GB (2x16 GB) oferują taktowanie 2666 MHz oraz opóźnienia na poziomie CL16.' ||
'Ponadto moduły Kingston FURY Beast Black wspierają obsługę profili XMP.');
INSERT INTO kategorie VALUES (1, 'Pamiec');
INSERT INTO podkategoria VALUES (1, 1, 'RAM');
INSERT INTO produkty VALUES (1, 'Beast Black', 319.00, 1, 1, '32 GB (2x16GB), 2666 MHz CL16');

-- password: password
INSERT INTO client (fname, lname, age, address, email, login, password) VALUES
    ('Test', 'User', -1, 'localhost', 'example@email.com', 'user', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');

-- password: He11o
INSERT INTO client (fname, lname, age, address, email, login, password) VALUES
    ('Adam', 'Kubacki', 19, '30-100 Krakow', 'adamKub@gmail.com', 'adamczycha', '7144ef0ab2fd42660eeec67e468702775810a6474c3f397c533eed7405b6cdb3');


SELECT * FROM client;
DELETE FROM client WHERE id_client > 2;