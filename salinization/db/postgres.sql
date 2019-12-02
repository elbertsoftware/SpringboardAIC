SET search_path = dev;

CREATE TABLE station(
	id SERIAL PRIMARY KEY,
	code VARCHAR(20) NOT NULL,
	name TEXT NOT NULL,
	note TEXT,
	province VARCHAR(20),
	x REAL,
	y REAL,
	z INTEGER,
	lat VARCHAR(16),
	lon VARCHAR(16)
);

CREATE TABLE province(
	id SERIAL PRIMARY KEY,
	code VARCHAR(20) NOT NULL,
	name TEXT NOT NULL
);

CREATE TABLE station_alias(
	id SERIAL PRIMARY KEY,
	code VARCHAR(20) NOT NULL,
	alias TEXT NOT NULL
);