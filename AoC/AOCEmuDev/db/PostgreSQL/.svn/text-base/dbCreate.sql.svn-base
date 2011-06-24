/******************************************************************************/
/*************************** Age Of Conan Database ****************************/
/*****************************  By Ashura75013 ********************************/
CREATE SCHEMA aocemudb;

CREATE USER aocemu WITH PASSWORD 'aocemu' CREATEDB;

GRANT ALL PRIVILEGES
ON DATABASE aocemudb
TO aocemu;

-- Accounts table
CREATE TABLE aocemudb.Accounts (
account_id smallint NOT NULL,
username varchar(50) NOT NULL,
password varchar(32) NOT NULL,
mail varchar(100),
last_connection DATE,
last_ip varchar(15),
date_creation DATE,
date_modif DATE,
date_delete DATE);

ALTER TABLE aocemudb.Accounts ADD CONSTRAINT pk_accounts PRIMARY KEY(account_id);

-- Races table
CREATE TABLE aocemudb.Races (
race_id smallint UNSIGNED NOT NULL,
race_name VARCHAR(25) NOT NULL,
race_desc TEXT);

ALTER TABLE aocemudb.Races ADD CONSTRAINT pk_races PRIMARY KEY(race_id);

-- Archetypes table
CREATE TABLE aocemudb.Archetypes (
arche_id smallint NOT NULL,
arche_name varchar(50) NOT NULL,
arche_desc TEXT);

ALTER TABLE aocemudb.Archetypes ADD CONSTRAINT pk_archetypes PRIMARY KEY(arche_id);

-- Classes table
CREATE TABLE aocemudb.Classes (
class_id smallint NOT NULL,
class_name varchar(50) NOT NULL,
class_desc TEXT);

ALTER TABLE aocemudb.Classes ADD CONSTRAINT pk_classes PRIMARY KEY(class_id);

-- Link between Races, Archetypes and Classes
CREATE TABLE aocemudb.Race_Arche_Class (
race_id smallint NOT NULL,
arche_id smallint NOT NULL,
class_id smallint NOT NULL);

ALTER TABLE aocemudb.Race_Arche_Class ADD CONSTRAINT pk_race_arche_class PRIMARY KEY(race_id, arche_id, class_id);
ALTER TABLE aocemudb.Race_Arche_Class ADD CONSTRAINT fk_RAC_race FOREIGN KEY(race_id) REFERENCES aocemudb.Races(race_id);
ALTER TABLE aocemudb.Race_Arche_Class ADD CONSTRAINT fk_RAC_arche FOREIGN KEY(arche_id) REFERENCES aocemudb.Archetypes(arche_id);
ALTER TABLE Race_Arche_Class ADD CONSTRAINT fk_RAC_class FOREIGN KEY(class_id) REFERENCES aocemudb.Classes(class_id);