BEGIN TRANSACTION;

COPY seasons FROM 'C:/DBMS_Project_data/seasons.csv' WITH CSV HEADER DELIMITER AS ',';
COPY circuits FROM 'C:/DBMS_Project_data/circuits.csv' WITH CSV HEADER DELIMITER AS ',';
COPY races FROM 'C:/DBMS_Project_data/races.csv' WITH CSV HEADER DELIMITER AS ',';
COPY status FROM 'C:/DBMS_Project_data/status.csv' WITH CSV HEADER DELIMITER AS ',';
COPY constructors FROM 'C:/DBMS_Project_data/constructors.csv' WITH CSV HEADER DELIMITER AS ',';
COPY drivers FROM 'C:/DBMS_Project_data/drivers.csv' WITH CSV HEADER DELIMITER AS ',';
COPY qualifying FROM 'C:/DBMS_Project_data/qualifying.csv' WITH CSV HEADER DELIMITER AS ',';
COPY results FROM 'C:/DBMS_Project_data/results.csv' WITH CSV HEADER DELIMITER AS ',';
COPY champions FROM 'C:/DBMS_Project_data/champions.csv' WITH CSV HEADER DELIMITER AS ',';
COPY constructor_champions FROM 'C:/DBMS_Project_data/constructor_champions.csv' WITH CSV HEADER DELIMITER AS ',';
COPY driver_standings FROM 'C:/DBMS_Project_data/driver_standings.csv' WITH CSV HEADER DELIMITER AS ',';
COPY constructor_standings FROM 'C:/DBMS_Project_data/constructor_standings.csv' WITH CSV HEADER DELIMITER AS ',';

END TRANSACTION;