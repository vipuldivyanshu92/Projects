/******************************************************************************/
/*************************** Age Of Conan Database ****************************/
/*****************************  By Ashura75013 ********************************/
CREATE SCHEMA aocemudb;

CREATE USER faolan WITH PASSWORD 'faolan' CREATEDB;

GRANT ALL PRIVILEGES
ON DATABASE faolandb
TO faolan;

-- Accounts table
CREATE TABLE faolandb.Accounts (
account_id smallint NOT NULL,
username varchar(50) NOT NULL,
password varchar(32) NOT NULL,
mail varchar(100),
last_connection DATE,
last_ip varchar(15),
date_creation DATE,
date_modif DATE,
date_delete DATE);

ALTER TABLE faolandb.Accounts ADD CONSTRAINT pk_accounts PRIMARY KEY(account_id);

-- Races table
CREATE TABLE faolandb.Races (
race_id smallint UNSIGNED NOT NULL,
race_name VARCHAR(25) NOT NULL,
race_desc TEXT);

ALTER TABLE faolandb.Races ADD CONSTRAINT pk_races PRIMARY KEY(race_id);

-- Archetypes table
CREATE TABLE faolandb.Archetypes (
arche_id smallint NOT NULL,
arche_name varchar(50) NOT NULL,
arche_desc TEXT);

ALTER TABLE faolandb.Archetypes ADD CONSTRAINT pk_archetypes PRIMARY KEY(arche_id);

-- Classes table
CREATE TABLE faolandb.Classes (
class_id smallint NOT NULL,
class_name varchar(50) NOT NULL,
class_desc TEXT);

ALTER TABLE faolandb.Classes ADD CONSTRAINT pk_classes PRIMARY KEY(class_id);

-- Link between Races, Archetypes and Classes
CREATE TABLE faolandb.Race_Arche_Class (
race_id smallint NOT NULL,
arche_id smallint NOT NULL,
class_id smallint NOT NULL);

ALTER TABLE faolandb.Race_Arche_Class ADD CONSTRAINT pk_race_arche_class PRIMARY KEY(race_id, arche_id, class_id);
ALTER TABLE faolandb.Race_Arche_Class ADD CONSTRAINT fk_RAC_race FOREIGN KEY(race_id) REFERENCES faolandb.Races(race_id);
ALTER TABLE faolandb.Race_Arche_Class ADD CONSTRAINT fk_RAC_arche FOREIGN KEY(arche_id) REFERENCES faolandb.Archetypes(arche_id);
ALTER TABLE Race_Arche_Class ADD CONSTRAINT fk_RAC_class FOREIGN KEY(class_id) REFERENCES faolandb.Classes(class_id);

Create table faolandb.Body(
  char_id smallint NOT NULL,
  arm NUMERIC(3,2) NOT NULL,
  chest NUMERIC(3,2) NOT NULL,
  bosom NUMERIC(3,2) NOT NULL,
  stomach NUMERIC(3,2) NOT NULL,
  arse NUMERIC(3,2) NOT NULL,
  thigh NUMERIC(3,2) NOT NULL,
  leg NUMERIC(3,2) NOT NULL);

Create table faolandb.Face(
char_id smallint not null,
EyebrowScale NUMERIC(3,2) not null,
CheekDepth NUMERIC(3,2) not null,
CheekHeight NUMERIC(3,2) not null,
CheekWidth NUMERIC(3,2) not null,
ChinLength NUMERIC(3,2) not null,
ChinWidth NUMERIC(3,2) not null,
EarAngle NUMERIC(3,2) not null,
Ears NUMERIC(3,2) not null,
EyesAngle NUMERIC(3,2) not null,
EyesVerticalPos NUMERIC(3,2) not null,
EyesHorizontalPos NUMERIC(3,2) not null,
EyesDepth NUMERIC(3,2) not null,
JawWidth NUMERIC(3,2) not null,
FaceLength NUMERIC(3,2) not null,
MouthVerticalPos NUMERIC(3,2) not null,
MouthWidth NUMERIC(3,2) not null,
NoseAngle NUMERIC(3,2) not null,
NoseCurve NUMERIC(3,2) not null,
Crooked_Nose NUMERIC(3,2) not null,
NoseLength NUMERIC(3,2) not null,
NoseWidth NUMERIC(3,2) not null) engine = MyISAM;
