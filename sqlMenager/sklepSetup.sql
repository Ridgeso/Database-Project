SET SEARCH_PATH TO projekt;

-- Tabele
CREATE TABLE kategorie
(
    id_kategorii SERIAL PRIMARY KEY,
    nazwa        VARCHAR(32) NOT NULL
);

CREATE TABLE podkategoria
(
    id_podkat    SERIAL PRIMARY KEY,
    id_kategorii INT,
    nazwa        VARCHAR(32) NOT NULL
);

CREATE TABLE produkt_opis
(
    id_opisu  SERIAL PRIMARY KEY,
    producent VARCHAR(30) NOT NULL,
    opis      text        NOT NULL
);

CREATE TABLE produkty
(
    id_produktu  SERIAL PRIMARY KEY,
    nazwa        VARCHAR(48)    NOT NULL,
    cena         decimal(10, 2) NOT NULL,
    id_opisu     INT,
    id_podkat    INT,
    specyfikacja TEXT
);

CREATE TABLE magazyn
(
    id_magazynu SERIAL PRIMARY KEY,
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
    id_opini    SERIAL PRIMARY KEY,
    ocena       INT NOT NULL,
    id_client   INT NOT NULL,
    id_prod     INT NOT NULL,
    opinia      text
);

CREATE TABLE client
(
    id_client BIGSERIAL PRIMARY KEY,
    fname VARCHAR(20),
    lname VARCHAR(30),
    age INT,
    address VARCHAR(30),
    email VARCHAR(40),
    login VARCHAR(20),
    password VARCHAR(64)
);

CREATE TABLE wozek
(
    id_client INT,
    id_produktu INT,
    ilosc INT
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

ALTER TABLE wozek
    ADD FOREIGN KEY (id_client) REFERENCES client (id_client);
ALTER TABLE wozek
    ADD FOREIGN KEY (id_produktu) REFERENCES produkty (id_produktu);

ALTER TABLE opinie
    ADD FOREIGN KEY (id_client) REFERENCES client (id_client);
ALTER TABLE opinie
    ADD FOREIGN KEY (id_prod) REFERENCES produkty (id_produktu);

-- Funckje
CREATE OR REPLACE FUNCTION create_user
(
    Ifname VARCHAR(20),
    Ilname VARCHAR(30),
    Iage INT,
    Iaddress VARCHAR(30),
    Iemail VARCHAR(40),
    Ilogin VARCHAR(20),
    Ipassword VARCHAR(64)
)
    RETURNS INT AS
$$
    DECLARE
        that_user INT := -1;
    BEGIN
        IF Ilogin LIKE 'admin' THEN
            RETURN -1;
        END IF;
        that_user := (SELECT id_client FROM client WHERE login = Ilogin);
        IF that_user IS NOT NULL THEN
            RETURN -1;
        ELSE
            INSERT INTO client (fname, lname, age, address, email, login, password)
                VALUES (Ifname, Ilname, Iage, Iaddress, Iemail, Ilogin, Ipassword);
            RETURN (SELECT id_client FROM client WHERE login = Ilogin AND password = Ipassword);
        END IF;
    END;
$$
    LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION get_loged_user(Ilogin VARCHAR(20),Ipassword VARCHAR(64))
    RETURNS TABLE
    (
        Sid_client BIGINT,
        Sfname VARCHAR(20),
        Slname VARCHAR(30),
        Sage INT,
        Saddress VARCHAR(30),
        Semail VARCHAR(40)
    )
    AS
$$
    BEGIN
        RETURN QUERY
            SELECT id_client, fname, lname, age, address, email
                FROM client
                WHERE login = Ilogin AND password = Ipassword;
    END;
$$
    LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION sprzedaj_produkt(id_clienta int)
    RETURNS BOOLEAN AS
$$
    BEGIN
        UPDATE stan_magazynu sm SET
            ilosc = ilosc - (SELECT w.ilosc FROM wozek w WHERE w.id_produktu = sm.id_produktu and w.id_client = id_clienta)
        WHERE id_produktu IN (SELECT w.id_produktu FROM wozek w WHERE w.id_client = id_clienta);

        DELETE FROM wozek w WHERE w.id_client = id_clienta;

        RETURN TRUE;
    END;
$$
    LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION dodaj_produkt(
    iNazwa VARCHAR(48),
    iCena DECIMAL(10, 2),
    iProducent VARCHAR(30),
    iPodkat VARCHAR(32),
    iOpis TEXT,
    iSpecyfi TEXT
)
    RETURNS BOOLEAN AS
$$
    BEGIN
        WITH opis_row as (
            INSERT INTO produkt_opis (producent, opis) VALUES (iProducent, iOpis) RETURNING id_opisu
        )
        INSERT INTO produkty (nazwa, cena, id_opisu, id_podkat, specyfikacja) VALUES(
            iNazwa,
            iCena,
            (SELECT opr.id_opisu FROM opis_row opr),
            (SELECT pk.id_podkat FROM podkategoria pk WHERE pk.nazwa LIKE iPodkat),
            iSpecyfi
        );
        RETURN TRUE;
    END;
$$
    LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION czy_wiecej_niz_jedna_opinia()
    RETURNS TRIGGER AS
$$
    BEGIN
        IF (SELECT COUNT(*) FROM opinie WHERE id_client = NEW.id_client AND id_prod = NEW.id_prod) > 0 THEN
            RAISE EXCEPTION 'Nie mozna wystawic wiecej niz jednej opinii, edytuj poprzednia lub ja usun';
        END IF;
        RETURN NEW;
    END;
$$
    LANGUAGE 'plpgsql';

CREATE TRIGGER czy_wiecej_niz_jedna_opinia_TRIGGER
    BEFORE INSERT ON opinie
    FOR EACH ROW
    EXECUTE FUNCTION czy_wiecej_niz_jedna_opinia();

CREATE OR REPLACE FUNCTION usun_te_same_produkty_w_wozku()
    RETURNS TRIGGER AS
$$
    BEGIN
        IF (NEW.ilosc = 0) THEN
            DELETE FROM wozek WHERE id_client = NEW.id_client AND id_produktu = NEW.id_produktu;
        ELSEIF (SELECT ilosc FROM wozek WHERE id_client = NEW.id_client AND id_produktu = NEW.id_produktu) IS NULL THEN
            RETURN NEW;
        ELSEIF (SELECT ilosc FROM wozek WHERE id_client = NEW.id_client AND id_produktu = NEW.id_produktu) != NEW.ilosc THEN
            UPDATE wozek w SET ilosc = NEW.ilosc WHERE id_client = NEW.id_client AND id_produktu = NEW.id_produktu;
        ELSE
            RAISE LOG 'Ten produkt w wozku klienta juz istnieje';
        END IF;
        RETURN NULL;
    END;
$$
    LANGUAGE 'plpgsql';

DROP TRIGGER usun_te_same_produkty_w_wozku_TRIGGER ON wozek;
CREATE TRIGGER usun_te_same_produkty_w_wozku_TRIGGER
    BEFORE INSERT ON wozek
    FOR EACH ROW
    EXECUTE FUNCTION usun_te_same_produkty_w_wozku();

-- INSERTY
INSERT INTO client (fname, lname, age, address, email, login, password) VALUES
-- password: password
    ('Test', 'User', -1, 'localhost', 'example@email.com', 'user', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
    ('Admin', 'Administrator', 22, 'Kernel', 'admin@ork.xi', 'admin', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'),
-- password: He11o
    ('Adam', 'Kubacki', 19, '30-100 Krakow', 'adamKub@gmail.com', 'adamczycha', '7144ef0ab2fd42660eeec67e468702775810a6474c3f397c533eed7405b6cdb3');

INSERT INTO kategorie VALUES
    (1, 'myszki'),
    (2, 'monitory'),
    (3, 'procesory'),
    (4, 'klawiatury'),
    (5, 'sluchawki'),
    (6, 'telefony'),
    (7, 'Pamiec');

INSERT INTO podkategoria VALUES
    (1, 1, 'laserowa'),
    (2, 1, 'optyczna'),
    (3, 2, 'LED'),
    (4, 2, 'QLED'),
    (5, 2, 'IPS'),
    (6, 3, 'Intel'),
    (7, 3, 'AMD'),
    (8, 4, 'membranowe'),
    (9, 4, 'haptyczne'),
    (10, 5, 'douszne'),
    (11, 5, 'nauszne'),
    (12, 5, 'dokanalowe'),
    (13, 6, 'iPhone'),
    (14, 6, 'Samsung'),
    (15, 6, 'Nathing Phone'),
    (16, 6, 'Pixel'),
    (17, 7, 'RAM'),
    (18, 7, 'SSD'),
    (19, 7, 'Nvme');

INSERT INTO magazyn VALUES
    (1, 'Ornando', 'Warszawa 43-242'),
    (2, 'Kantar', 'Opole 11-131'),
    (3, 'Puerto', 'Krakow 30-100');

INSERT INTO produkt_opis VALUES
    (1, 'Steelseries', 'Z myślą o e-sporcie' ||
        'Myszka jest wyjątkowo ergonomiczna i wyposażona w praktyczne funkcje, które ułatwiają grę i dają przewagę nad konkurentami.' ||
        'Z myszą Rival 3 zwycięstwo przyjdzie Ci łatwo, bo zaprojektowano ją z myślą o najwyższej wytrzymałości. Skorzystaj z najnowszych technologii wykorzystywanych w produktach przeznaczonych dla profesjonalnych gamerów.'),
    (2, 'Samsung', 'Wielkie ekrany i dobrze wyswietlajace'),
    (3, 'Intel', 'Tak zwana szybkosc w komputerze'),
    (4, 'Ryzen', 'Klikasz sobie i jest fajnie'),
    (5, 'JBL', 'Idealne na zime w busie'),
    (6, 'Google', 'Genialny telefon z porzadnymi bebechami'),
    (7, 'WD Black', 'Pamięć RAM DDR4 Kingston FURY Beast Black 32 GB' ||
        'Zmodernizuj swój system dzięki stylowej i niezwykle wydajnej pamięci RAM DDR4 Kingston FURY Beast Black.' ||
        'Dwa moduły o łącznej pojemności 32 GB (2x16 GB) oferują taktowanie 2666 MHz oraz opóźnienia na poziomie CL16.' ||
        'Ponadto moduły Kingston FURY Beast Black wspierają obsługę profili XMP.');

INSERT INTO produkty VALUES
    (1, 'Rival 3',          120.00,     1, 1,  'Laserowa 8500 dpi'),
    (2, 'DeathAdder',       210.00,     1, 2,  'Optyczna 26000 dpi'),
    (3, 'Swift Pro',        2100.00,    2, 3,  '24.1" 1920x1080px 540Hz'),
    (4, 'Predator',         1520.00,    2, 4,  '4K 133Hz'),
    (5, 'Odyssey',          25230.00,   2, 5,  '8K 60Hz'),
    (6, 'Core I5',          5230.00,    3, 6,  '3.3 GHz 12Mb Cashe'),
    (7, 'Ryzen 3',          5432.00,    3, 7,  '3.5 GHz 8Mb Cashe'),
    (8, 'Blackwidow',       21430.00,   4, 8,  'Yellow switches'),
    (9, 'Apex 3',           310.00,     4, 9,  'Brown Swiches'),
    (10, 'Kraken',          4510.00,    5, 10, 'Bezprzewodowe dzwięk 2.0'),
    (11, 'Arctis',          3450.00,    5, 11, 'Bezprzewodowe dzwięk 7.1'),
    (12, 'JBL',             220.00,     5, 12, 'Bluetooth 50h on battery'),
    (13, '15 Pro',          23420.00,   6, 13, 'No drogo'),
    (14, 'S24',             2000.00,    6, 14, '10x zoom optyczny'),
    (15, 'Nothing Phone 2', 2310.00,    6, 15, 'Glypsh'),
    (16, 'Pixel 8',         2432410.00, 6, 16, 'Fajny jest'),
    (17, 'WD black',        2105.00,    7, 17, 'Do gier'),
    (18, 'Evo',             2102.00,    7, 18, 'Szybki'),
    (19, 'Beast Black',     319.00,     7, 19, '32 GB 2x16GB), 2666 MHz CL16');

INSERT INTO stan_magazynu VALUES
    (1, 1, 4), (1, 2, 5), (1, 3, 2), (1, 4, 3), (1, 5, 4), (1, 6, 5), (1, 7, 2), (1, 8, 3), (1, 9, 4), (1, 10, 5), (1, 11, 2), (1, 12, 3), (1, 13, 4), (1, 14, 5), (1, 15, 2), (1, 16, 3), (1, 17, 4), (1, 18, 5), (1, 19, 2),
    (2, 1, 5), (2, 2, 2), (2, 3, 3), (2, 4, 4), (2, 5, 5), (2, 6, 2), (2, 7, 3), (2, 8, 4), (2, 9, 5), (2, 10, 2), (2, 11, 3), (2, 12, 4), (2, 13, 5), (2, 14, 2), (2, 15, 3), (2, 16, 4), (2, 17, 5), (2, 18, 2), (2, 19, 3),
    (3, 1, 2), (3, 2, 3), (3, 3, 4), (3, 4, 5), (3, 5, 2), (3, 6, 3), (3, 7, 4), (3, 8, 5), (3, 9, 2), (3, 10, 3), (3, 11, 4), (3, 12, 5), (3, 13, 2), (3, 14, 3), (3, 15, 4), (3, 16, 5), (3, 17, 2), (3, 18, 3), (3, 19, 4);


SELECT * FROM client;