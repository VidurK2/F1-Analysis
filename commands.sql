--LANDING PAGE--
--LATEST RACES--
SELECT r.year, r.name as race, c.name as circuit, c.country, r.raceid, c.circuitid
FROM races as r, results re, circuits c
WHERE r.raceid = re.raceid AND c.circuitid = r.circuitid
GROUP BY (race, c.name, c.country, r.year, r.round,r.raceid,c.circuitid)
ORDER BY r.year DESC, r.round DESC
LIMIT 10;
--ALL RACES IN A GIVEN YEAR--
SELECT r.round, r.year, r.name as race, c.name as circuit, c.country, r.raceid, c.circuitid
FROM races as r, results re, circuits c
WHERE r.raceid = re.raceid AND c.circuitid = r.circuitid AND r.year = 2021
GROUP BY (race, c.name, c.country, r.year, r.round,r.raceid,c.circuitid)
ORDER BY r.round ASC;
--RESULTS FROM A GIVEN YEAR AND RACE NAME--
SELECT COALESCE(CAST(r.position as varchar),'NC'), d.forename||' '||d.surname, d.driverid, c.name AS constructor_name, c.constructorid, r.points
FROM results r
JOIN races ra ON r.raceId = ra.raceId
JOIN drivers d ON r.driverId = d.driverId
JOIN constructors c ON r.constructorId = c.constructorId
WHERE ra.name = 'Monaco Grand Prix' AND ra.year = 2017
ORDER BY r.position ASC; 
ORDER BY r.position ASC; 
--DRIVERS STANDINGS AFTER A GIVEN RACE--
WITH RaceResults AS (
    SELECT r.raceId, r.year, r.round
    FROM races r
    JOIN seasons s ON r.year = s.year
    WHERE s.year = 2017 and r.name = 'Bahrain Grand Prix'
)
SELECT ds.position, d.forename||' '||d.surname as name, ds.points as points
FROM driver_standings ds, drivers d, RaceResults rr
WHERE ds.raceId = rr.raceId and d.driverid = ds.driverid
ORDER BY position ASC;
--CONSTRUCTORS STANDINGS AFTER A GIVEN RACE--
WITH RaceResults AS (
    SELECT r.raceId, r.year, r.round
    FROM races r
    JOIN seasons s ON r.year = s.year
    WHERE s.year = 2021 and r.name = 'Abu Dhabi Grand Prix'
)
SELECT d.name as name, ds.points as points
FROM constructor_standings ds, constructors d, RaceResults rr
WHERE ds.raceId = rr.raceId and d.constructorid = ds.constructorid
ORDER BY position ASC;
------------------
--CURRENT DRIVERS--
WITH latest_race as (SELECT r.raceid
FROM races as r, results re
WHERE r.raceid = re.raceid 
ORDER BY r.year DESC, r.round DESC
LIMIT 1)

SELECT d.forename||' '||d.surname as driver, c.name as constructor
FROM results r, constructors c, drivers d
WHERE r.raceid = (SELECT * FROM latest_race) AND c.constructorid = r.constructorid AND d.driverid = r.driverid
ORDER BY r.constructorid
--ALL DRIVERS--
SELECT d.forename||' '||d.surname as name
FROM drivers d
ORDER BY name ASC
--DRIVER PROFILE--
SELECT
    (SELECT COUNT(*) 
     FROM results r
     JOIN drivers d ON r.driverId = d.driverId
     WHERE d.forename || ' ' || d.surname = 'Lewis Hamilton' AND r.position = 1) AS number_of_wins,
    
    (SELECT COUNT(*) 
     FROM results r
     JOIN drivers d ON r.driverId = d.driverId
     WHERE d.forename || ' ' || d.surname = 'Lewis Hamilton' AND r.position IN (1, 2, 3)) AS number_of_podiums,

    (SELECT COUNT(*) 
     FROM results r
     JOIN drivers d ON r.driverId = d.driverId
     WHERE d.forename || ' ' || d.surname = 'Lewis Hamilton' AND r.grid = 1) AS number_of_pole_positions,
    
    (SELECT COALESCE(SUM(r.points), 0)
     FROM results r
     JOIN drivers d ON r.driverId = d.driverId
     WHERE d.forename || ' ' || d.surname = 'Lewis Hamilton') AS number_of_points,

    (SELECT 
    SUM(CASE 
        WHEN r.position = 1 THEN 25
        WHEN r.position = 2 THEN 18
        WHEN r.position = 3 THEN 15
        WHEN r.position = 4 THEN 12
        WHEN r.position = 5 THEN 10
        WHEN r.position = 6 THEN 8
        WHEN r.position = 7 THEN 6
        WHEN r.position = 8 THEN 4
        WHEN r.position = 9 THEN 2
        WHEN r.position = 10 THEN 1
        ELSE 0
    END) AS total_normalised_points
    FROM results r JOIN drivers d ON r.driverId = d.driverId
    WHERE d.forename || ' ' || d.surname = 'Lewis Hamilton') AS number_of_points_normalised,


    (SELECT COUNT(*) 
     FROM results r
     JOIN drivers d ON r.driverId = d.driverId
     WHERE d.forename || ' ' || d.surname = 'Lewis Hamilton') AS number_of_race_starts,
	 
	(SELECT c.name
	FROM results AS r, drivers as d, races as ra, constructors as c
	WHERE r.driverid = d.driverid AND d.forename||' '||d.surname = 'Lewis Hamilton' AND
	r.raceid = ra.raceid AND c.constructorid = r.constructorid
	GROUP BY (ra.year, ra.round,d.driverid, c.constructorid, c.name)
	ORDER BY ra.year DESC, ra.round DESC
	LIMIT 1) AS team,

    (SELECT COUNT(*)
    FROM champions C
    JOIN drivers d ON d.driverId = c.driverId
    WHERE d.forename || ' ' || d.surname = 'Lewis Hamilton') AS number_of_championships
;
--CAREER DRIVER RESULTS IN ORDER--
SELECT ra.year, ra.name AS race, 
    CASE 
        WHEN r.position IS NULL AND (r.statusid = 81 OR r.statusid = 97) THEN '-'
		WHEN r.position IS NULL THEN 'NC'
        ELSE CAST(r.position AS VARCHAR)
    END AS position,
    CASE
		WHEN r.statusId = 81 OR r.statusid = 97 THEN 'DNQ'
        WHEN r.statusId != 1 THEN 'DNF'
        ELSE ''
    END AS status
FROM results r
JOIN races ra ON r.raceId = ra.raceId
JOIN drivers d ON r.driverId = d.driverId
LEFT JOIN status s ON r.statusId = s.statusId
WHERE d.forename||' '||d.surname = 'Lewis Hamilton'
ORDER BY ra.year ASC, ra.round ASC;
--TEAMMATE COMPARISON--
WITH GivenDriverRaces AS (
    SELECT r.raceId, r.constructorId,q1, q2, q3 
    FROM results r
    JOIN qualifying q ON r.raceId = q.raceId AND r.driverId = q.driverId
    JOIN drivers d ON r.driverId = d.driverId
    WHERE d.forename || ' ' || d.surname = 'Fernando Alonso'
),

TeammateRaces AS (
    SELECT r.raceId, r.constructorId, r.driverId,q1, q2, q3 
    FROM results r
    JOIN qualifying q ON r.raceId = q.raceId AND r.driverId = q.driverId
    WHERE EXISTS (
            SELECT 1 FROM GivenDriverRaces gdr 
            WHERE gdr.raceId = r.raceId AND gdr.constructorId = r.constructorId
        )
)

SELECT d.forename || ' ' || d.surname AS teammate_name,AVG(LEAST(g.q1, COALESCE(g.q2, g.q1), COALESCE(g.q3, g.q1)) - LEAST(t.q1, COALESCE(t.q2, t.q1), COALESCE(t.q3, t.q1))) AS avg_qualifying_gap
FROM GivenDriverRaces g
JOIN TeammateRaces t ON g.raceId = t.raceId AND g.constructorId = t.constructorId
JOIN drivers d ON t.driverId = d.driverId
WHERE d.forename || ' ' || d.surname != 'Fernando Alonso'
GROUP BY d.driverId
ORDER BY avg_qualifying_gap;
-------------------
--CURRENT TEAMS--
WITH latest_race as (SELECT r.raceid
FROM races as r, results re
WHERE r.raceid = re.raceid 
ORDER BY r.year DESC, r.round DESC
LIMIT 1)

SELECT c.name as constructor
FROM results r, constructors c
WHERE r.raceid = (SELECT * FROM latest_race) AND c.constructorid = r.constructorid
GROUP BY(constructor,r.constructorid)
ORDER BY r.constructorid
--TEAM PROFILE--
SELECT
    (SELECT COUNT(*) 
     FROM results r
     JOIN constructors c ON r.constructorId = c.constructorId
     WHERE c.name = 'Ferrari' AND r.position = 1) AS number_of_wins,
    
    (SELECT COUNT(*) 
     FROM results r
     JOIN constructors c ON r.constructorId = c.constructorId
     WHERE c.name = 'Ferrari' AND r.position IN (1, 2, 3)) AS number_of_podiums,

    (SELECT COUNT(*) 
     FROM results r
     JOIN constructors c ON r.constructorId = c.constructorId
     WHERE c.name = 'Ferrari' AND r.grid = 1) AS number_of_pole_positions,
    
    (SELECT COALESCE(SUM(r.points), 0)
     FROM results r
     JOIN constructors c ON r.constructorId = c.constructorId
     WHERE c.name = 'Ferrari') AS number_of_points,

    (SELECT COUNT(DISTINCT r.raceId) 
     FROM results r
     JOIN constructors c ON r.constructorId = c.constructorId
     WHERE c.name = 'Ferrari') AS number_of_race_entries
;

------------------------
--CURRENT CIRCUITS--
SELECT r.name, c.name
FROM circuits c, races r
WHERE r.year = 2023 and r.circuitid = c.circuitid
--QUALIFYING TIME OVER THE YEARS FOR A PARTICULAR CIRCUITREF--
SELECT r.year, MIN(LEAST(q.q1, COALESCE(q.q2, q.q1), COALESCE(q.q3, COALESCE(q.q2, q.q1)))) AS fastest_time 
FROM qualifying q JOIN races r ON q.raceId = r.raceId JOIN circuits c ON r.circuitId = c.circuitId
WHERE c.circuitid = 1 AND q.position = 1
GROUP BY r.year 
ORDER BY r.year ASC;
--MOST SUCCESSFUL DRIVER AT A CIRCUITREF--
SELECT d.driverid, d.forename||' '||d.surname as drivername,COUNT(*) as number_of_wins
FROM results r
JOIN races ra ON r.raceId = ra.raceId
JOIN circuits ci ON ra.circuitId = ci.circuitId
JOIN drivers d ON r.driverId = d.driverId
WHERE ci.circuitref = 'brands_hatch' AND r.position = 1
GROUP BY d.driverId, drivername
ORDER BY number_of_wins DESC, drivername
LIMIT 5;
--MOST SUCCESSFUL CONSTRUCTOR AT A CIRCUITREF--
SELECT c.constructorid, c.name as constructorname,COUNT(*) as number_of_wins
FROM results r
JOIN races ra ON r.raceId = ra.raceId
JOIN circuits ci ON ra.circuitId = ci.circuitId
JOIN constructors c ON r.constructorId = c.constructorId
WHERE ci.circuitref = 'spa' AND r.position = 1
GROUP BY c.constructorId, constructorname
ORDER BY number_of_wins DESC, constructorname
LIMIT 5;
-----------------------
--SEASON--
--LIST ALL SEASONS--
SELECT *
FROM seasons
ORDER BY seasons.year ASC
--BY SEASON DRIVER RESULTS--
WITH RaceResults AS (
    SELECT r.raceId, r.year, r.round
    FROM races r
    JOIN seasons s ON r.year = s.year
    WHERE s.year = 2004
    ORDER BY r.year DESC, r.round DESC
    LIMIT 1
)
SELECT ds.position, d.forename||' '||d.surname as name, ds.points as points
FROM driver_standings ds, drivers d, RaceResults rr
WHERE ds.raceId = rr.raceId and d.driverid = ds.driverid
ORDER BY position ASC;
--BY SEASON TEAM RESULTS--
WITH RaceResults AS (
    SELECT r.raceId, r.year, r.round
    FROM races r
    JOIN seasons s ON r.year = s.year
    WHERE s.year = 2022
    ORDER BY r.year DESC, r.round DESC
    LIMIT 1
)
SELECT c.name as name, cs.points as points
FROM constructor_standings cs, constructors c, RaceResults rr
WHERE cs.raceId = rr.raceId and c.constructorid = cs.constructorid
ORDER BY position ASC;
--ALL CHAMPIONS--
SELECT champions.year, drivers.forename||' '||drivers.surname as name
FROM champions, drivers
WHERE champions.driverid = drivers.driverid

--CHAMPIONS--
SELECT d.driverId, CONCAT(d.forename, ' ', d.surname) AS driver_name, COUNT(c.year) as championship_count
FROM champions c
JOIN drivers d ON c.driverId = d.driverId
GROUP BY d.driverId, driver_name
ORDER BY championship_count DESC;

