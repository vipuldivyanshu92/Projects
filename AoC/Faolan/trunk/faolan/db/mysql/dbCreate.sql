/******************************************************************************/
/*************************** Age Of Conan Database ****************************/
/*****************************  By Ashura75013 ********************************/
CREATE SCHEMA faolandb;

CREATE USER faolan IDENTIFIED BY 'faolan';

USE faolandb;

GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP
ON faolandb.*
TO faolan@localhost
IDENTIFIED BY 'faolan';

GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP
ON faolandb.*
TO 'faolan'@'%'
IDENTIFIED BY 'faolan';

-- Accounts table
CREATE TABLE Accounts (
account_id INT UNSIGNED NOT NULL,
username VARCHAR(50) NOT NULL,
password VARCHAR(32) NOT NULL,
mail VARCHAR(100),
kind TINYINT UNSIGNED NOT NULL,
cookie INT UNSIGNED, 
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

Create table Body(
char_id smallint(5) not null,
arm double(3,2) not null,
chest double(3,2) not null,
bosom double(3,2) not null,
stomach double(3,2) not null,
arse double(3,2) not null,
thigh double(3,2) not null,
leg double(3,2) not null) engine=MyISAM;

Create table Face(
char_id tinyint(5) not null,
EyebrowScale double(3,2) not null,
CheekDepth double(3,2) not null,
CheekHeight double(3,2) not null,
CheekWidth double(3,2) not null,
ChinLength double(3,2) not null,
ChinWidth double(3,2) not null,
EarAngle double(3,2) not null,
Ears double(3,2) not null,
EyesAngle double(3,2) not null,
EyesVerticalPos double(3,2) not null,
EyesHorizontalPos double(3,2) not null,
EyesDepth double(3,2) not null,
JawWidth double(3,2) not null,
FaceLength double(3,2) not null,
MouthVerticalPos double(3,2) not null,
MouthWidth double(3,2) not null,
NoseAngle double(3,2) not null,
NoseCurve double(3,2) not null,
Crooked_Nose double(3,2) not null,
NoseLength double(3,2) not null,
NoseWidth double(3,2) not null) engine = MyISAM;

Create table maps($
map_id INT NOT NULL,
map_name VARCHAR(150));

Alter table maps add constraint pk_maps Primary key(map_id);