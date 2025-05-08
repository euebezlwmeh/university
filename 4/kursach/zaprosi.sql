-- Регистрация новых лекарственных препаратов 
INSERT INTO Storage_conditions (min_temperature, max_temperature, lighting, humidity)
VALUES (2, 25, 'Ограниченное', 40)

INSERT INTO Medicine (id_storage_conditions, INN, trade_name, control_level, form_release, dosage)
VALUES (1, 'Парацетамол', 'Парацетамол Реневал', 'Общий', 'Таблетки', 500)

-- Регистрация новых партий лекарственных препаратов 
INSERT INTO Producer(name_, country, contacts)
VALUES ('Треугольник', 'Российская Федерация', 'treugolnik@mail.ru')

INSERT INTO Medicine_batch (id_medicine, id_producer, series, production_date, expiration_date, count)
VALUES (1, 1, 1000, '2025-01-20', '2028-01-20', 200)

-- Списание лекарственных препаратов из партии
INSERT INTO Batch_writing_off (id_medicine_batch, written_off_date, reason, count)
VALUES (1, '2025-03-05', 'Нарушение упаковки', 10)

UPDATE Medicine_batch
SET count = Medicine_batch.count - Batch_writing_off.count
FROM Batch_writing_off
WHERE Medicine_batch.id_medicine_batch = Batch_writing_off.id_medicine_batch

-- Просмотр всех партий лекарственных препаратов
SELECT Medicine.INN, Medicine.trade_name, Medicine.control_level, Medicine.form_release, Medicine.dosage, 
Medicine_batch.series, Medicine_batch.production_date, Medicine_batch.expiration_date, Medicine_batch.count 
FROM Medicine_batch
JOIN Medicine ON Medicine.id_medicine = Medicine_batch.id_medicine



-- СОЗДАНИЕ ТАБЛИЦ
CREATE TABLE Storage_conditions(
    id_storage_conditions SERIAL PRIMARY KEY,
    min_temperature DECIMAL NOT NULL,
    max_temperature DECIMAL NOT NULL,
    lighting VARCHAR(16) NOT NULL,
    humidity DECIMAL NOT NULL
);

CREATE TABLE Medicine(
    id_medicine SERIAL PRIMARY KEY,
    id_storage_conditions INTEGER NOT NULL,
    INN VARCHAR(60) NOT NULL,
    Trade_name VARCHAR(30) NOT NULL,
    control_level VARCHAR(14) NOT NULL,
    form_release VARCHAR(10) NOT NULL,
    dosage INTEGER NOT NULL	
);

CREATE TABLE Medicine_batch(
    id_medicine_batch SERIAL PRIMARY KEY,
    id_medicine	INTEGER NOT NULL,
    id_producer	INTEGER NOT NULL,
    series INTEGER NOT NULL,
    production_date	DATE NOT NULL,
    expiration_date	DATE NOT NULL,	
    count INTEGER NOT NULL
);

CREATE TABLE Batch_writing_off(
    id_batch_writing_off SERIAL PRIMARY KEY,
    id_medicine_batch INTEGER NOT NULL,
    written_off_date DATE NOT NULL,
    reason VARCHAR(40) NOT NULL,
    count INTEGER NOT NULL
);

CREATE TABLE Producer(
    id_producer SERIAL PRIMARY KEY,
    name_ VARCHAR(50) NOT NULL,
    country	VARCHAR(20) NOT NULL,	
    contacts VARCHAR(30) NOT NULL	
);

ALTER TABLE Medicine
    ADD CONSTRAINT medicine_storage_conditions_id_fkey FOREIGN KEY (id_storage_conditions)
    REFERENCES Storage_conditions(id_storage_conditions) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

ALTER TABLE Medicine_batch
    ADD CONSTRAINT medicine_batch_medicine_id_fkey FOREIGN KEY (id_medicine)
    REFERENCES Medicine(id_medicine) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

ALTER TABLE Medicine_batch
    ADD CONSTRAINT medicine_batch_producer_id_fkey FOREIGN KEY (id_producer)
    REFERENCES Producer(id_producer) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

ALTER TABLE Batch_writing_off
    ADD CONSTRAINT batch_writing_off_medicine_batch_id_fkey FOREIGN KEY (id_medicine_batch)
    REFERENCES Medicine_batch(id_medicine_batch) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


-- ВСТАВКА ДАННЫХ
-- Регистрация новых лекарственных препаратов 
INSERT INTO Storage_conditions (min_temperature, max_temperature, lighting, humidity) VALUES 
(2, 25, 'Ограниченное', 40),
(2, 25, 'Не чувствителен', 40),
(2, 25, 'Не чувствителен', 50),
(2, 20, 'Не чувствителен', 40),
(2, 25, 'Тёмное', 40),
(2, 25, 'Тёмное', 30);


INSERT INTO Medicine (id_storage_conditions, INN, trade_name, control_level, form_release, dosage) VALUES 
(1, 'Парацетамол', 'Парацетамол Реневал', 'Общий', 'Таблетки', 500),
(2, 'Азелаиновая кислота', 'Азикс-Дерм', 'Общий', 'Мазь', 20),
(4, 'Этанол', 'Спирт этиловый', 'Психотропный', 'Жидкость', 100),
(3, 'Морфин', 'Морфин', 'Наркотический', 'Таблетки', 10),
(2, 'Уголь активированный', 'Активированный уголь', 'Общий', 'Таблетки', 250),
(5, 'Аммиак', 'Аммиак', 'Общий', 'Раствор', 44),
(6, 'Тиопентал натрий', 'Тиопентал натрия', 'Наркотический', 'Порошок', 1),
(6, 'Фентанил', 'Фентанил', 'Наркотический', 'Раствор', 50),
(6, 'Пропионилфенилэтоксиэтилпиперидин', 'Просидол', 'Наркотический', 'Таблетки', 20),
(5, 'Амитриптилин ', 'Амитриптилин ', 'Психотропный', 'Таблетки', 25);

-- Регистрация новых партий лекарственных препаратов 
INSERT INTO Producer(name_, country, contacts) VALUES 
('Фармстандарт', 'Российская Федерация', 'info@pharmstd.ru'),
('Верофарм', 'Российская Федерация', 'contact@veropharm.ru'),
('Биокад', 'Российская Федерация', 'biocad@biocad.ru'),
('Новартис Фарма', 'Швейцария', 'novartis.info@novartis.com'),
('Пфайзер', 'США', 'russia.medinfo@pfizer.com'),
('АстраЗенека', 'Великобритания', 'info.russia@astrazeneca.com'),
('Гедеон Рихтер', 'Венгрия', 'office@richter.ru'),
('Сервье', 'Франция', 'contact.russia@servier.com'),
('Такеда', 'Япония', 'medinfo.russia@takeda.com'),
('Байер', 'Германия', 'med.info@bayer.com');

INSERT INTO Medicine_batch (id_medicine, id_producer, series, production_date, expiration_date, count) VALUES 
(1, 1, 1025, '2024-01-15', '2026-01-15', 150),
(2, 3, 2048, '2024-03-10', '2027-03-10', 250),
(3, 5, 3096, '2023-11-20', '2025-11-20', 180),
(4, 2, 4123, '2024-02-05', '2026-02-05', 300),
(5, 4, 5071, '2023-12-15', '2025-12-15', 120),
(6, 7, 6324, '2024-04-01', '2028-04-01', 200),
(7, 6, 7459, '2023-09-30', '2026-09-30', 275),
(8, 9, 8562, '2024-01-25', '2027-01-25', 190),
(9, 8, 9637, '2023-10-10', '2025-10-10', 220),
(10, 10, 1074, '2024-02-18', '2026-02-18', 160);

-- Списание лекарственных препаратов из партии
INSERT INTO Batch_writing_off (id_medicine_batch, written_off_date, reason, count) VALUES
(1, '2024-02-10', 'Истёкший срок годности', 5),
(2, '2024-03-15', 'Повреждение упаковки', 8),
(3, '2024-01-20', 'Изменение физико-химических свойств', 3),
(4, '2024-04-05', 'Брак производства', 12),
(5, '2024-02-28', 'Нарушение условий хранения', 7),
(6, '2024-03-10', 'Механическое повреждение', 10),
(7, '2024-01-15', 'Истечение срока годности', 14),
(8, '2024-04-01', 'Повреждение упаковки', 2),
(9, '2024-03-22', 'Нарушение герметичности', 6),
(10, '2024-02-18', 'Истёкший срок годности', 4);