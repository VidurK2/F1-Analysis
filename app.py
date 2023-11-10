from flask import g, Flask, render_template, request
import asyncpg
from jinja2 import filters
import datetime

async def get_db():
    if 'db' not in g:
        g.db = await asyncpg.connect(host =  "10.2.95.122", database = "yajaman_warriors", user = "yajaman_warriors", password = "e2a474ac")

    return g.db

async def close_db():
    db = g.pop("db", None)

    if db is not None:
        await db.close()

app = Flask("app")

@app.route("/admin")
async def admin_page():
    return render_template("admin_form.html")


@app.route("/admin/insert", methods=["GET", "POST"])
async def insert_data():
    if request.method == "POST":
        table_name = request.form.get("table_name")


        if table_name == "drivers":
            driverid = request.form.get("driverid")
            driverref = request.form.get("driverref")
            number = request.form.get("number")
            code = request.form.get("code")
            forename = request.form.get("forename")
            surname = request.form.get("surname")
            nationality = request.form.get("nationality")

            d: asyncpg.Connection = await get_db()

            await d.execute("INSERT INTO drivers (driverid, driverref, number, code, forename, surname, nationality) VALUES ($1, $2, $3, $4, $5, $6, $7)", int(driverid), driverref, int(number), code, forename, surname, nationality)

            await close_db()

        elif table_name == "champions":
            year = request.form.get("year")
            driverid = request.form.get("driverid")

            d: asyncpg.Connection = await get_db()
            await d.execute("INSERT INTO champions (year, driverid) VALUES ($1, $2)", int(year), int(driverid))
            await close_db()


        elif table_name == "circuits":
            circuitid = request.form.get("circuitid")
            circuitref = request.form.get("circuitref")
            name = request.form.get("name")
            location = request.form.get("location")
            country = request.form.get("country")

            d: asyncpg.Connection = await get_db()
            await d.execute("INSERT INTO circuits (circuitid, circuitref, name, location, country) VALUES ($1, $2, $3, $4, $5)", int(circuitid), circuitref, name, location, country)
            await close_db()



        elif table_name == "constructor_champions":
            year = request.form.get("year")
            constructorid = request.form.get("constructorid")

            d: asyncpg.Connection = await get_db()
            await d.execute("INSERT INTO constructor_champions (year, constructorid) VALUES ($1, $2)", int(year), int(constructorid))
            await close_db()
        
        elif table_name == "constructor_standings":
            constructorstandingsid = request.form.get("constructorstandingsid")
            raceid = request.form.get("raceid")
            constructorid = request.form.get("constructorid")
            points = request.form.get("points")
            position = request.form.get("position")

            d: asyncpg.Connection = await get_db()
            await d.execute("INSERT INTO constructor_standings (constructorstandingsid, raceid, constructorid, points, position) VALUES ($1, $2, $3, $4, $5)", int(constructorstandingsid), int(raceid), int(constructorid), float(points), int(position))
            await close_db()

        elif table_name == "constructors":
            constructorid = request.form.get("constructorid")
            constructorref = request.form.get("constructorref")
            name = request.form.get("name")
            nationality = request.form.get("nationality")

            d: asyncpg.Connection = await get_db()
            await d.execute("INSERT INTO constructors (constructorid, constructorref, name, nationality) VALUES ($1, $2, $3, $4)", int(constructorid), constructorref, name, nationality)
            await close_db()

        elif table_name == "driver_standings":
            driverstandingsid = request.form.get("driverstandingsid")
            raceid = request.form.get("raceid")
            driverid = request.form.get("driverid")
            points = request.form.get("points")
            position = request.form.get("position")
            
            d: asyncpg.Connection = await get_db()
            await d.execute("INSERT INTO driver_standings (driverstandingsid, raceid, driverid, points, position) VALUES ($1, $2, $3, $4, $5)", int(driverstandingsid), int(raceid), int(driverid), float(points), int(position))
            await close_db()

        elif table_name == "qualifying":
            qualifyid = request.form.get("qualifyid")
            raceid = request.form.get("raceid")
            driverid = request.form.get("driverid")
            constructorid = request.form.get("constructorid")
            position = request.form.get("position")
            q1 = request.form.get("q1")
            q2 = request.form.get("q2")
            q3 = request.form.get("q3")
            print(q1,q2,q3)
            if q1 != '':
                q1 = datetime.datetime.strptime(q1, "%H:%M:%S.%f").time()
            else:
                q1 = None
            if q2 != '':
                q2 = datetime.datetime.strptime(q2, "%H:%M:%S.%f").time()
            else:
                q2 = None
            if q3 != '':
                q3 = datetime.datetime.strptime(q3, "%H:%M:%S.%f").time()
            else:
                q3 = None
            
            d: asyncpg.Connection = await get_db()
            await d.execute("INSERT INTO qualifying (qualifyid, raceid, driverid, constructorid, position, q1, q2, q3) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)", int(qualifyid), int(raceid), int(driverid), int(constructorid), int(position), q1,q2,q3)
            await close_db()


        elif table_name == "races":
            raceid = request.form.get("raceid")
            year = request.form.get("year")
            round = request.form.get("round")
            circuitid = request.form.get("circuitid")
            name = request.form.get("name")

            d: asyncpg.Connection = await get_db()
            await d.execute("INSERT INTO races (raceid, year, round, circuitid, name) VALUES ($1, $2, $3, $4, $5)", int(raceid), int(year), int(round), int(circuitid), name)
            await close_db()



        elif table_name == "results":
            resultid = request.form.get("resultid")
            raceid = request.form.get("raceid")
            driverid = request.form.get("driverid")
            constructorid = request.form.get("constructorid")
            grid = request.form.get("grid")
            position = request.form.get("position")
            points = request.form.get("points")
            laps = request.form.get("laps")
            fastestlap = request.form.get("fastestlap")
            if fastestlap == '':
                fastestlap = None
            else:
                fastestlap = int(fastestlap)
            fastestlap_time = request.form.get("fastestlap_time")
            if fastestlap_time != '':
                fastestlap_time = datetime.datetime.strptime(fastestlap_time, "%H:%M:%S.%f").time()
            else:
                fastestlap_time = None
            statusid = request.form.get("statusid")
            
            d: asyncpg.Connection = await get_db()
            await d.execute("INSERT INTO results (resultid, raceid, driverid, constructorid, grid, position, points, laps, fastestlap, fastestlap_time, statusid) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)", int(resultid), int(raceid), int(driverid), int(constructorid), int(grid), int(position), float(points), int(laps), fastestlap, fastestlap_time, int(statusid))
            await close_db()

        elif table_name == "seasons":
            year = request.form.get("year")            
            
            d: asyncpg.Connection = await get_db()
            await d.execute("INSERT INTO seasons (year) VALUES ($1)", int(year))
            await close_db()

        elif table_name == "status":
            statusid = request.form.get("statusid")  
            status = request.form.get("status")            
            
            d: asyncpg.Connection = await get_db()
            await d.execute("INSERT INTO status (statusid, status) VALUES ($1, $2)", int(statusid), status)
            await close_db()

        return f"Data inserted successfully into the {table_name} table"
    
    return render_template("admin_form.html")

@app.route("/teams/search")
async def search_teams():
    query = request.args.get("query")

    if not query:
        return "Please enter a search query."

    d: asyncpg.Connection = await get_db()
    result = await d.fetch(
        "SELECT constructorid, name FROM constructors WHERE LOWER(name) LIKE LOWER('%' || $1 || '%')",
    query
    )
    await close_db()

    return render_template("team_search_results.html", query=query,results=result)

@app.route("/drivers/search")
async def search_drivers():
    query = request.args.get("query")

    if not query:
        return "Please enter a search query."

    d: asyncpg.Connection = await get_db()
    result = await d.fetch("SELECT driverid, forename || ' ' || surname AS name FROM drivers WHERE LOWER(forename || ' ' || surname) LIKE LOWER($1)  OR LOWER(forename) = LOWER($1) OR LOWER(surname) = LOWER($1)",
    query
    )
    print(result)
    await close_db()

    return render_template("search_results.html", query=query,results=result)

@app.route("/")
async def index(): #The function syntax needs to be corrected, but this is a good starting point
    d: asyncpg.Connection = await get_db() 
    result = await d.fetch("SELECT r.year, r.name as race, c.name as circuit, c.country, r.raceid, c.circuitid FROM races as r, results re, circuits c WHERE r.raceid = re.raceid AND c.circuitid = r.circuitid GROUP BY (race, c.name, c.country, r.year, r.round,r.raceid,c.circuitid) ORDER BY r.year DESC, r.round DESC LIMIT 10;")
    await close_db()
    return render_template('index.html', results=result)

@app.route("/drivers")
async def drivers(): #The function syntax needs to be corrected, but this is a good starting point
    d: asyncpg.Connection = await get_db() 
    result = await d.fetch("WITH latest_race as (SELECT r.raceid FROM races as r, results re WHERE r.raceid = re.raceid ORDER BY r.year DESC, r.round DESC LIMIT 1) SELECT d.driverid, d.forename||' '||d.surname as driver, c.constructorid, c.name as constructor FROM results r, constructors c, drivers d WHERE r.raceid = (SELECT * FROM latest_race) AND c.constructorid = r.constructorid AND d.driverid = r.driverid ORDER BY r.constructorid")
    await close_db()
    return render_template('drivers.html', results=result)

@app.route("/drivers/all")
async def drivers_all(): #The function syntax needs to be corrected, but this is a good starting point
    d: asyncpg.Connection = await get_db() 
    result = await d.fetch("SELECT d.driverid, d.forename||' '||d.surname as name FROM drivers d ORDER BY name ASC")
    await close_db()
    return render_template('all_drivers.html', results=result)

@app.route("/drivers/<driverid>")
async def driver_profile(driverid):
    d: asyncpg.Connection = await get_db()
    dname = await d.fetch("SELECT forename||' '||surname FROM drivers WHERE driverid = $1",int(driverid))
    if dname == []:
        return "404 not found"
    result = await d.fetch("SELECT(SELECT COUNT(*) FROM results r JOIN drivers d ON r.driverId = d.driverId WHERE d.driverid = $1 AND r.position = 1) AS number_of_wins, (SELECT COUNT(*) FROM results r JOIN drivers d ON r.driverId = d.driverId WHERE d.driverid = $1 AND r.position IN (1, 2, 3)) AS number_of_podiums, (SELECT COUNT(*) FROM results r JOIN drivers d ON r.driverId = d.driverId WHERE d.driverid = $1 AND r.grid = 1) AS number_of_pole_positions, (SELECT COALESCE(SUM(r.points), 0) FROM results r JOIN drivers d ON r.driverId = d.driverId WHERE d.driverid = $1) AS number_of_points, (SELECT SUM(CASE WHEN r.position = 1 THEN 25 WHEN r.position = 2 THEN 18 WHEN r.position = 3 THEN 15 WHEN r.position = 4 THEN 12 WHEN r.position = 5 THEN 10 WHEN r.position = 6 THEN 8 WHEN r.position = 7 THEN 6 WHEN r.position = 8 THEN 4 WHEN r.position = 9 THEN 2 WHEN r.position = 10 THEN 1 ELSE 0 END) AS total_normalised_points FROM results r JOIN drivers d ON r.driverId = d.driverId WHERE d.driverid = $1) AS number_of_points_normalised, (SELECT COUNT(*) FROM results r JOIN drivers d ON r.driverId = d.driverId WHERE d.driverid = $1) AS number_of_race_starts, (SELECT c.name FROM results AS r, drivers as d, races as ra, constructors as c WHERE r.driverid = d.driverid AND d.driverid = $1 AND r.raceid = ra.raceid AND c.constructorid = r.constructorid GROUP BY (ra.year, ra.round,d.driverid, c.constructorid, c.name) ORDER BY ra.year DESC, ra.round DESC LIMIT 1) AS team, (SELECT COUNT(*) FROM champions C JOIN drivers d ON d.driverId = c.driverId WHERE d.driverid = $1) AS number_of_championships, (SELECT c.constructorid FROM results AS r, drivers as d, races as ra, constructors as c WHERE r.driverid = d.driverid AND d.driverid = $1 AND r.raceid = ra.raceid AND c.constructorid = r.constructorid GROUP BY (ra.year, ra.round,d.driverid, c.constructorid, c.name) ORDER BY ra.year DESC, ra.round DESC LIMIT 1) as teamid;",int(driverid))
    teammates = await d.fetch("WITH GivenDriverRaces AS (SELECT r.raceId, r.constructorId,q1, q2, q3 FROM results r JOIN qualifying q ON r.raceId = q.raceId AND r.driverId = q.driverId JOIN drivers d ON r.driverId = d.driverId WHERE d.driverid = $1),TeammateRaces AS (SELECT r.raceId, r.constructorId, r.driverId,q1, q2, q3 FROM results r JOIN qualifying q ON r.raceId = q.raceId AND r.driverId = q.driverId WHERE EXISTS (SELECT 1 FROM GivenDriverRaces gdr WHERE gdr.raceId = r.raceId AND gdr.constructorId = r.constructorId)) SELECT d.driverid, d.forename || ' ' || d.surname AS teammate_name,AVG(LEAST(g.q1, COALESCE(g.q2, g.q1), COALESCE(g.q3, g.q1)) - LEAST(t.q1, COALESCE(t.q2, t.q1), COALESCE(t.q3, t.q1))) AS avg_qualifying_gap FROM GivenDriverRaces g JOIN TeammateRaces t ON g.raceId = t.raceId AND g.constructorId = t.constructorId JOIN drivers d ON t.driverId = d.driverId WHERE d.driverid != $1 GROUP BY d.driverId;",int(driverid))
    if teammates == []:
        teammates = await d.fetch("SELECT DISTINCT d2.driverid, d2.forename || ' ' || d2.surname AS teammate_name, 'NO DATA' FROM results r1 JOIN results r2 ON r1.raceId = r2.raceId AND r1.constructorId = r2.constructorId AND r1.driverId != r2.driverId JOIN drivers d2 ON r2.driverId = d2.driverId WHERE r1.driverId = $1 ORDER BY d2.driverid",int(driverid))
    

    await close_db()
    return render_template('driver_profile.html',driverid=driverid, results=result, name=dname, teammate = teammates, type=type, custom_time_filter = filters.custom_time_filter)
    
@app.route("/drivers/<driverid>/results")
async def driver_results(driverid):
    d: asyncpg.Connection = await get_db()
    result = await d.fetch("SELECT ra.raceid, ra.year, ra.name AS race, CASE WHEN r.position IS NULL AND (r.statusid = 81 OR r.statusid = 97) THEN '-' WHEN r.position IS NULL THEN 'NC' ELSE CAST(r.position AS VARCHAR) END AS position, CASE WHEN r.statusId = 81 OR r.statusid = 97 THEN 'DNQ' WHEN r.statusId != 1 THEN 'DNF' ELSE '' END AS status FROM results r JOIN races ra ON r.raceId = ra.raceId JOIN drivers d ON r.driverId = d.driverId LEFT JOIN status s ON r.statusId = s.statusId WHERE d.driverid=$1 ORDER BY ra.year ASC, ra.round ASC;",int(driverid))
    await close_db()
    return render_template('driver_results.html',results =result)
    return [1,2,3]

@app.route("/teams")
async def teams():
    d: asyncpg.Connection = await get_db()
    result = await d.fetch("WITH latest_race as (SELECT r.raceid FROM races as r, results re WHERE r.raceid = re.raceid  ORDER BY r.year DESC, r.round DESC LIMIT 1) SELECT r.constructorid, c.name as constructor FROM results r, constructors c WHERE r.raceid = (SELECT * FROM latest_race) AND c.constructorid = r.constructorid GROUP BY(constructor,r.constructorid) ORDER BY r.constructorid")
    await close_db()
    return render_template('teams.html',results = result)

@app.route("/teams/all")
async def teams_all():
    d: asyncpg.Connection = await get_db()
    result = await d.fetch("SELECT c.constructorid, c.name as name FROM constructors c ORDER BY name ASC")
    await close_db()
    return render_template('all_teams.html',results = result)

@app.route("/teams/<teamid>")
async def team_profile(teamid):
    d: asyncpg.Connection = await get_db()
    cname = await d.fetch("SELECT name FROM constructors WHERE constructorid = $1",int(teamid))
    result = await d.fetch("SELECT(SELECT COUNT(*) FROM results r JOIN constructors c ON r.constructorId = c.constructorId WHERE c.constructorid = $1 AND r.position = 1) AS number_of_wins,(SELECT COUNT(*) FROM results r JOIN constructors c ON r.constructorId = c.constructorId WHERE c.constructorid = $1 AND r.position IN (1, 2, 3)) AS number_of_podiums, (SELECT COUNT(*) FROM results r JOIN constructors c ON r.constructorId = c.constructorId WHERE c.constructorid = $1 AND r.grid = 1) AS number_of_pole_positions, (SELECT COALESCE(SUM(r.points), 0) FROM results r JOIN constructors c ON r.constructorId = c.constructorId WHERE c.constructorid = $1) AS number_of_points,(SELECT COUNT(DISTINCT r.raceId) FROM results r JOIN constructors c ON r.constructorId = c.constructorId WHERE c.constructorid = $1) AS number_of_race_entries;",int(teamid))
    championships = await d.fetch("SELECT COUNT(*) as champion_count FROM constructor_champions WHERE constructorid = $1;",int(teamid))
    await close_db()
    return render_template ('team_profile.html',results=result,name=cname, championships = championships)

@app.route("/seasons")
async def seasons():
    d: asyncpg.Connection = await get_db()
    result = await d.fetch("SELECT * FROM seasons ORDER BY year DESC")
    await close_db()
    return render_template('seasons.html',results = result)

@app.route("/seasons/<year>")
async def season(year):
    d: asyncpg.Connection = await get_db()
    result = await d.fetch("WITH RaceResults AS (SELECT r.raceId, r.year, r.round FROM races r JOIN seasons s ON r.year = s.year WHERE s.year = $1 ORDER BY r.year DESC, r.round DESC LIMIT 1) SELECT ds.driverid, ds.position, d.forename||' '||d.surname as name, ds.points as points FROM driver_standings ds, drivers d, RaceResults rr WHERE ds.raceId = rr.raceId and d.driverid = ds.driverid ORDER BY position ASC;",int(year))
    result2 = await d.fetch("WITH RaceResults AS (SELECT r.raceId, r.year, r.round FROM races r JOIN seasons s ON r.year = s.year WHERE s.year = $1 ORDER BY r.year DESC, r.round DESC LIMIT 1) SELECT cs.constructorid, cs.position, c.name as name, cs.points as points FROM constructor_standings cs, constructors c, RaceResults rr WHERE cs.raceId = rr.raceId and c.constructorid = cs.constructorid ORDER BY position ASC;",int(year))
    result4 = await d.fetch("SELECT r.round, r.year, r.name as race, c.name as circuit, c.country, r.raceid, c.circuitid FROM races as r, results re, circuits c WHERE r.raceid = re.raceid AND c.circuitid = r.circuitid AND r.year = $1 GROUP BY (race, c.name, c.country, r.year, r.round,r.raceid,c.circuitid) ORDER BY r.round ASC;",int(year))
    await close_db()
    return render_template('season.html', results = result, teamresults=result2, raceresults=result4, name = year)

@app.route("/circuits")
async def circuits():
    d: asyncpg.Connection = await get_db()
    result = await d.fetch("SELECT c.circuitid, c.name, c.country FROM circuits c, races r GROUP BY (c.circuitid, c.name,c.country) ORDER BY name ASC;")
    await close_db()
    return render_template('all_circuits.html', results = result)

@app.route("/circuits/<circuitid>")
async def circuit(circuitid):
    d: asyncpg.Connection = await get_db()
    cname = await d.fetch("SELECT name, location, country from circuits WHERE circuitid = $1",int(circuitid))
    times = await d.fetch("SELECT * FROM(SELECT r.year, MIN(LEAST(q.q1, COALESCE(q.q2, q.q1), COALESCE(q.q3, COALESCE(q.q2, q.q1)))) AS fastest_time FROM qualifying q JOIN races r ON q.raceId = r.raceId JOIN circuits c ON r.circuitId = c.circuitId WHERE c.circuitid = $1 AND q.position = 1 GROUP BY r.year ORDER BY r.year ASC) AS tmp WHERE fastest_time IS NOT NULL ORDER BY year ASC;",int(circuitid))
    years= [item['year'] for item in times]
    time = [item['fastest_time'].minute*60+item['fastest_time'].second+item['fastest_time'].microsecond*0.000001 for item in times]
    bestdrivers = await d.fetch("SELECT d.driverid, d.forename||' '||d.surname as drivername,COUNT(*) as number_of_wins FROM results r JOIN races ra ON r.raceId = ra.raceId JOIN circuits ci ON ra.circuitId = ci.circuitId JOIN drivers d ON r.driverId = d.driverId WHERE ci.circuitid = $1 AND r.position = 1 GROUP BY d.driverId, drivername ORDER BY number_of_wins DESC, drivername LIMIT 5;",int(circuitid))
    bestteams = await d.fetch("SELECT c.constructorid, c.name as constructorname,COUNT(*) as number_of_wins FROM results r JOIN races ra ON r.raceId = ra.raceId JOIN circuits ci ON ra.circuitId = ci.circuitId JOIN constructors c ON r.constructorId = c.constructorId WHERE ci.circuitid = $1 AND r.position = 1 GROUP BY c.constructorId, constructorname ORDER BY number_of_wins DESC, constructorname LIMIT 5;",int(circuitid))
    await close_db()
    return render_template('circuit_profile.html', datas = time, year = years, name=cname, drivers=bestdrivers, teams=bestteams)

@app.route("/records")
async def records():
    d: asyncpg.Connection = await get_db()
    result = await d.fetch("SELECT d.driverId, CONCAT(d.forename, ' ', d.surname) AS driver_name, COUNT(c.year) as championship_count FROM champions c JOIN drivers d ON c.driverId = d.driverId GROUP BY d.driverId, driver_name ORDER BY championship_count DESC LIMIT 5;")
    result2 = await d.fetch("SELECT d.driverId, CONCAT(d.forename, ' ', d.surname) AS driver_name, COUNT(r.position) AS wins FROM drivers d JOIN results r ON d.driverId = r.driverId WHERE r.position = 1 GROUP BY d.driverId, driver_name HAVING COUNT(r.position) >= 1 ORDER BY wins DESC LIMIT 5;")
    result3 = await d.fetch("SELECT d.driverId, CONCAT(d.forename, ' ', d.surname) AS driver_name, COUNT(r.grid) AS pole_positions_count FROM drivers d JOIN results r ON d.driverId = r.driverId WHERE r.grid = 1 GROUP BY d.driverId HAVING COUNT(r.grid) >= 1 ORDER BY pole_positions_count DESC LIMIT 5;")
    result4 = await d.fetch("SELECT c.constructorid, c.name AS constructor_name, COUNT(cc.year) AS championship_count FROM constructor_champions cc JOIN constructors c ON cc.constructorid = c.constructorid GROUP BY c.name,c.constructorid ORDER BY championship_count DESC LIMIT 5;")
    result5 = await d.fetch("SELECT d.constructorid, d.name as name, COUNT(r.position) AS wins FROM constructors d JOIN results r ON d.constructorId = r.constructorId WHERE r.position = 1 GROUP BY d.constructorId, name HAVING COUNT(r.position) >= 1 ORDER BY wins DESC LIMIT 5;")
    result6 = await d.fetch("SELECT d.constructorid, d.name as name, COUNT(r.grid) AS poles FROM constructors d JOIN results r ON d.constructorId = r.constructorId WHERE r.grid = 1 GROUP BY d.constructorId, name HAVING COUNT(r.grid) >= 1 ORDER BY poles DESC LIMIT 5;")
    await close_db()
    return render_template('records.html', champs = result, winners = result2, polesitters = result3, teamchamps = result4, teamwinners = result5, teampoles = result6)

@app.route("/records/championships")
async def champions():
    d: asyncpg.Connection = await get_db()
    result = await d.fetch("SELECT d.driverId, CONCAT(d.forename, ' ', d.surname) AS driver_name, COUNT(c.year) as championship_count FROM champions c JOIN drivers d ON c.driverId = d.driverId GROUP BY d.driverId, driver_name ORDER BY championship_count DESC;")
    await close_db()
    return render_template('all_champs.html', champs = result)

@app.route("/records/teamchampionships")
async def teamchampions():
    d: asyncpg.Connection = await get_db()
    result = await d.fetch("SELECT c.constructorid, c.name AS constructor_name, COUNT(cc.year) AS championship_count FROM constructor_champions cc JOIN constructors c ON cc.constructorid = c.constructorid GROUP BY c.name,c.constructorid ORDER BY championship_count DESC;")
    await close_db()
    return render_template('all_teamchamps.html', champs = result)

@app.route("/records/wins")
async def winners():
    d: asyncpg.Connection = await get_db()
    result = await d.fetch("SELECT d.driverId, CONCAT(d.forename, ' ', d.surname) AS driver_name, COUNT(r.position) AS wins FROM drivers d JOIN results r ON d.driverId = r.driverId WHERE r.position = 1 GROUP BY d.driverId, driver_name HAVING COUNT(r.position) >= 1 ORDER BY wins DESC;")
    await close_db()
    return render_template('all_winners.html', winners = result)

@app.route("/records/teamwins")
async def teamwinners():
    d: asyncpg.Connection = await get_db()
    result = await d.fetch("SELECT d.constructorid, d.name as name, COUNT(r.position) AS wins FROM constructors d JOIN results r ON d.constructorId = r.constructorId WHERE r.position = 1 GROUP BY d.constructorId, name HAVING COUNT(r.position) >= 1 ORDER BY wins DESC;")
    await close_db()
    return render_template('all_teamwinners.html', winners = result)

@app.route("/records/poles")
async def poles():
    d: asyncpg.Connection = await get_db()
    result = await d.fetch("SELECT d.driverId, CONCAT(d.forename, ' ', d.surname) AS driver_name, COUNT(r.grid) AS pole_positions_count FROM drivers d JOIN results r ON d.driverId = r.driverId WHERE r.grid = 1 GROUP BY d.driverId HAVING COUNT(r.grid) >= 1 ORDER BY pole_positions_count DESC;")
    await close_db()
    return render_template('all_polesitters.html', polesitters = result)

@app.route("/records/teampoles")
async def teampoles():
    d: asyncpg.Connection = await get_db()
    result = await d.fetch("SELECT d.constructorid, d.name as name, COUNT(r.grid) AS poles FROM constructors d JOIN results r ON d.constructorId = r.constructorId WHERE r.grid = 1 GROUP BY d.constructorId, name HAVING COUNT(r.grid) >= 1 ORDER BY poles DESC;")
    await close_db()
    return render_template('all_teampolesitters.html', polesitters = result)

@app.route("/races/<raceid>")
async def race(raceid):
    d: asyncpg.Connection = await get_db()
    racename = await d.fetch("SELECT races.year, races.name from races WHERE races.raceid = $1",int(raceid))
    result = await d.fetch("SELECT COALESCE(CAST(r.position as varchar),'NC'), d.forename||' '||d.surname, d.driverid, c.name AS constructor_name, c.constructorid, r.points FROM results r JOIN races ra ON r.raceId = ra.raceId JOIN drivers d ON r.driverId = d.driverId JOIN constructors c ON r.constructorId = c.constructorId WHERE ra.raceid = $1 ORDER BY r.position ASC;",int(raceid))
    standingsd = await d.fetch("WITH RaceResults AS (SELECT r.raceId, r.year, r.round FROM races r JOIN seasons s ON r.year = s.year WHERE r.raceid = $1) SELECT d.driverid, ds.position, d.forename||' '||d.surname as fullname, ds.points as ppoints, c.constructorid, c.name FROM driver_standings ds, drivers d, RaceResults rr, results re, races r,constructors c WHERE ds.raceId = rr.raceId AND d.driverid = ds.driverid AND c.constructorid = re.constructorid AND ds.driverid = re.driverid AND r.raceid = rr.raceid AND r.raceid = re.raceid GROUP BY (d.driverid, ds.position, fullname, ppoints, c.constructorid, c.name) ORDER BY position ASC;",int(raceid))
    standingsc = await d.fetch("WITH RaceResults AS (SELECT r.raceId, r.year, r.round FROM races r JOIN seasons s ON r.year = s.year WHERE r.raceid = $1) SELECT d.constructorid, ds.position, d.name as name, ds.points as points FROM constructor_standings ds, constructors d, RaceResults rr WHERE ds.raceId = rr.raceId and d.constructorid = ds.constructorid ORDER BY position ASC;",int(raceid))
    await close_db()
    return render_template('race.html', results = result, name=racename, drivers = standingsd, teams = standingsc)