--- useful SQL scripts

--- drop table

DROP TABLE busdata;

--- create table

CREATE TABLE busdata (DateTime timestamp DEFAULT current_timestamp, 
Angle double precision,
EndPoint VARCHAR(50),
IterationEnd VARCHAR(50),
IterationStart VARCHAR(50),
RouteCode VARCHAR(50),
RouteId integer,
RouteName VARCHAR(200),
StartPoint VARCHAR(50),
State smallint,
TimeToPoint smallint,
VehicleId integer,
VehicleName VARCHAR(50),
X double precision,
Y double precision,
LowFloor BOOL);

--- user privileges

GRANT ALL PRIVILEGES ON TABLE busdata TO _username_;


--- drop all connections
select pg_terminate_backend(pid) from pg_stat_activity where datname='busdata';