BEGIN TRANSACTION;

DROP TABLE IF EXISTS constructor_standings;
DROP TABLE IF EXISTS driver_standings;
DROP TABLE IF EXISTS constructor_champions;
DROP TABLE IF EXISTS champions;
DROP TABLE IF EXISTS results;
DROP TABLE IF EXISTS qualifying;
DROP TABLE IF EXISTS status;
DROP TABLE IF EXISTS drivers;
DROP TABLE IF EXISTS constructors;
DROP TABLE IF EXISTS races;
DROP TABLE IF EXISTS circuits;
DROP TABLE IF EXISTS seasons;

CREATE TABLE seasons(
	year int,
	PRIMARY KEY(year)
);

CREATE TABLE circuits(
	circuitid int DEFAULT NULL,
	circuitref varchar DEFAULT NULL,
	name varchar DEFAULT NULL,
	location varchar DEFAULT NULL,
	country varchar DEFAULT NULL,
	PRIMARY KEY(circuitid)
);

CREATE TABLE races(
	raceid int DEFAULT NULL,
	year int DEFAULT NULL,
	round int DEFAULT NULL,
	circuitid int DEFAULT NULL,
	name varchar DEFAULT NULL,
	PRIMARY KEY(raceid),
	FOREIGN KEY(year) REFERENCES seasons(year),
	FOREIGN KEY(circuitid) REFERENCES circuits(circuitid)
);

CREATE TABLE constructors(
	constructorid int DEFAULT NULL,
	constructorref varchar DEFAULT NULL,
	name varchar DEFAULT NULL,
	nationality varchar DEFAULT NULL,
	PRIMARY KEY(constructorid)
);

CREATE TABLE drivers(
	driverid int DEFAULT NULL,
	driverref varchar DEFAULT NULL,
	number int DEFAULT NULL,
	code varchar,
	forename varchar DEFAULT NULL,
	surname varchar DEFAULT NULL,
	nationality varchar DEFAULT NULL,
	PRIMARY KEY(driverid)
);

CREATE TABLE status(
	statusid int DEFAULT NULL,
	status varchar DEFAULT NULL,
	PRIMARY KEY(statusid)
);

CREATE TABLE qualifying(
	qualifyid int DEFAULT NULL,
	raceid int DEFAULT NULL,
	driverid int DEFAULT NULL,
	constructorid int DEFAULT NULL,
	position int DEFAULT NULL,
	q1 time DEFAULT NULL,
	q2 time DEFAULT NULL,
	q3 time DEFAULT NULL,
	PRIMARY KEY(qualifyid),
	FOREIGN KEY(raceid) REFERENCES races(raceid),
	FOREIGN KEY(driverid) REFERENCES drivers(driverid),
	FOREIGN KEY(constructorid) REFERENCES constructors(constructorid)
);

CREATE TABLE results(
	resultid int DEFAULT NULL,
	raceid int DEFAULT NULL,
	driverid int DEFAULT NULL,
	constructorid int DEFAULT NULL,
	grid int DEFAULT NULL,
	position int DEFAULT NULL,
	points float DEFAULT NULL,
	laps int DEFAULT NULL,
	fastestlap int DEFAULT NULL,
	fastestlap_time time DEFAULT NULL,
	statusid int DEFAULT NULL,
	PRIMARY KEY(resultid),
	FOREIGN KEY(raceid) REFERENCES races(raceid),
	FOREIGN KEY(driverid) REFERENCES drivers(driverid),
	FOREIGN KEY(constructorid) REFERENCES constructors(constructorid),
	FOREIGN KEY(statusid) REFERENCES status(statusid)
);

CREATE TABLE champions(
	year int,
	driverid int,
	PRIMARY KEY(year),
	FOREIGN KEY(driverid) REFERENCES drivers(driverid)
);

CREATE TABLE constructor_champions(
	year int,
	constructorid int,
	PRIMARY KEY(year),
	FOREIGN KEY(constructorid) REFERENCES constructors(constructorid)
);

CREATE TABLE driver_standings(
	driverstandingsId int,
	raceid int,
	driverid int,
	points float,
	position int,
	PRIMARY KEY(driverstandingsId),
	FOREIGN KEY(driverid) REFERENCES drivers(driverid),
	FOREIGN KEY(raceid) REFERENCES races(raceid)

);

CREATE TABLE constructor_standings(
	constructorstandingsId int,
	raceid int,
	constructorid int,
	points float,
	position int,
	PRIMARY KEY(constructorstandingsId),
	FOREIGN KEY(constructorid) REFERENCES constructors(constructorid),
	FOREIGN KEY(raceid) REFERENCES races(raceid)
);

END TRANSACTION;