/******************************************************************************/
/*************************** Age Of Conan Database ****************************/
/*****************************  By Ashura75013 ********************************/
CREATE SCHEMA aocemudb;

CREATE USER aocemu IDENTIFIED BY 'aocemu';

USE aocemudb;

GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP
ON aocemudb.*
TO aocemu@localhost
IDENTIFIED BY 'aocemu';

GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP
ON aocemudb.*
TO 'aocemu'@'%'
IDENTIFIED BY 'aocemu';

-- Accounts table
CREATE TABLE Accounts (
account_id SMALLINT UNSIGNED NOT NULL,
username VARCHAR(50) NOT NULL,
password VARCHAR(32) NOT NULL,
mail VARCHAR(100),
last_connection DATE,
last_ip VARCHAR(15),
date_creation DATE,
date_modif DATE,
date_delete DATE);

ALTER TABLE Accounts ADD CONSTRAINT pk_accounts PRIMARY KEY(account_id);

-- Races table
CREATE TABLE Races (
race_id TINYINT UNSIGNED NOT NULL,
race_name VARCHAR(25) NOT NULL,
race_desc TEXT);

ALTER TABLE Races ADD CONSTRAINT pk_races PRIMARY KEY(race_id);

-- Archetypes table
CREATE TABLE Archetypes (
arche_id TINYINT UNSIGNED NOT NULL,
arche_name VARCHAR(50) NOT NULL,
arche_desc TEXT);

ALTER TABLE Archetypes ADD CONSTRAINT pk_archetypes PRIMARY KEY(arche_id);

-- Classes table
CREATE TABLE Classes (
class_id TINYINT UNSIGNED NOT NULL,
class_name VARCHAR(50) NOT NULL,
class_desc TEXT);

ALTER TABLE Classes ADD CONSTRAINT pk_classes PRIMARY KEY(class_id);

-- Link between Races, Archetypes and Classes
CREATE TABLE Race_Arche_Class (
race_id TINYINT UNSIGNED NOT NULL,
arche_id TINYINT UNSIGNED NOT NULL,
class_id TINYINT UNSIGNED NOT NULL);

ALTER TABLE Race_Arche_Class ADD CONSTRAINT pk_race_arche_class PRIMARY KEY(race_id, arche_id, class_id);
ALTER TABLE Race_Arche_Class ADD CONSTRAINT fk_RAC_race FOREIGN KEY(race_id) REFERENCES Races(race_id);
ALTER TABLE Race_Arche_Class ADD CONSTRAINT fk_RAC_arche FOREIGN KEY(arche_id) REFERENCES Archetypes(arche_id);
ALTER TABLE Race_Arche_Class ADD CONSTRAINT fk_RAC_class FOREIGN KEY(class_id) REFERENCES Classes(class_id);