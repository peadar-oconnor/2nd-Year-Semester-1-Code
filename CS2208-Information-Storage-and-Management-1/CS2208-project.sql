/* q1 */
CREATE TABLE Pub(
	PLN CHAR (5) NOT NULL,
	PubName VARCHAR (20),
	PCounty VARCHAR (15),
	PRIMARY KEY (PLN)
);

CREATE TABLE NeighbourCounty(
	County1 VARCHAR (15),
	County2 VARCHAR (15)
);

CREATE TABLE Person(
	PPSN INT NOT NULL,
	PName VARCHAR (15),
	PCounty VARCHAR (15),
	Age INT,
	DailyPubLimit INT,
	PRIMARY KEY (PPSN)
);

CREATE TABLE Visit(
	PLN CHAR (5) NOT NULL,
	PPSN INT NOT NULL,
	StartDateOfVisit DATETIME NOT NULL,
	EndDateOfVisit DATETIME NOT NULL,
	PRIMARY KEY (PLN, PPSN, StartDateOfVisit, EndDateOfVisit),
	FOREIGN KEY (PLN) REFERENCES Pub(PLN),
	FOREIGN KEY (PPSN) REFERENCES Person(PPSN)
	
);

CREATE TABLE Covid_Diagnosis(
	PPSN INT NOT NULL,
	DiagnosisDate DATE,
	IsolationEndDate DATE,
	PRIMARY KEY (PPSN),
	FOREIGN KEY (PPSN) REFERENCES Person(PPSN)
);

/* q2 */
INSERT INTO Pub
VALUES
	('L1234', 'Murphy''s', 'Cork'),
	('L2345', 'Joe''s', 'Limerick'),
	('L3456', 'BatBar', 'Kerry');
	
INSERT INTO NeighbourCounty
VALUES
	('Cork', 'Limerick'),
	('Limerick', 'Cork'),
	('Cork', 'Kerry'),
	('Kerry', 'Cork');
	
INSERT INTO Person
VALUES
	(1, 'Liza', 'Cork', 22, 5),
	(2, 'Alex', 'Limerick', 19, 7),
	(3, 'Tom', 'Kerry', 23, 10),
	(4, 'Peter', 'Cork', 39, 8);
	
INSERT INTO Visit
VALUES
	('L1234', 1, '2020-02-10 10:00:00', '2020-02-10 11:00:00'),
	('L1234', 1, '2020-08-12 11:00:00', '2020-08-12 11:35:00'),
	('L2345', 3, '2020-03-12 11:00:00', '2020-03-12 11:50:00');

INSERT INTO Covid_Diagnosis
VALUES
	(2, '2020-02-11', '2020-02-21')

/* q3 */
DELIMITER //
CREATE TRIGGER visit_infected
BEFORE UPDATE ON Visit
FOR EACH ROW
BEGIN
	IF (NEW.Visit.PPSN IN (SELECT PPSN FROM Covid_Diagnosis) AND NEW.Visit.StartDateOfVisit >= Covid_Diagnosis.DiagnosisDate AND NEW.Visit.StartDateOfVisit <= Covid_Diagnosis.IsolationEndDate) THEN
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Infected person cannot visit a Pub within Isolation Period.';
	END  IF;
END; //
DELIMITER ;

/* q4 */
DELIMITER //
CREATE PROCEDURE PubCounty(IN varPLN CHAR(5))
BEGIN
	SELECT Pub.PCounty
	FROM Pub, Visit
	WHERE Visit.PLN = Pub.PLN AND Visit.PLN = varPLN;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE PersonCounty(IN varPPSN INT)
BEGIN
	SELECT Person.PCounty
	FROM Visit, Person
	WHERE Visit.PPSN = Person.PPSN AND Visit.PPSN = varPPSN;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE FindNeighbour(IN varCounty VARCHAR(15))
BEGIN
	SELECT County2
	FROM NeighbourCounty
	WHERE County1 = varCounty;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER restrict_visit
BEFORE UPDATE ON Visit
FOR EACH ROW
BEGIN
	IF (PersonCounty(NEW.Visit.PPSN NOT IN (SELECT PubCounty(NEW.Visit.PLN)) OR NEW.Visit.PPSN NOT IN (SELECT FindNeighbour((SELECT PubCounty(NEW.Visit.PLN)))) THEN
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Pub is not within the restricted area that the person can visit.';
	END  IF;
END; //
DELIMITER ;

/* q5 */
DELIMITER //
CREATE TRIGGER daily_pub_limit_check
BEFORE UPDATE ON Visit
FOR EACH ROW
BEGIN
	IF ((SELECT COUNT(*) FROM Visit WHERE PPSN = New.Visit.PPSN AND StartDateOfVisit = DATE(NEW.Visit.StartDateOfVisit)) > (SELECT DailyPubLimit FROM Person WHERE PPSN = New.Visit.PPSN)) THEN
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Person cannot exceed their Daily Pub Limit of Visits.';
	END  IF;
END; //
DELIMITER ;


DELIMITER //
CREATE TRIGGER visit_same_time
BEFORE UPDATE ON Visit
FOR EACH ROW
BEGIN
	IF (NEW.Visit.StartDateOfVisit > (SELECT StartDateOfVisit FROM Visit WHERE PPSN = NEW.Visit.PPSN) AND NEW.Visit.StartDateOfVisit < (SELECT EndDateOfVisit FROM Visit WHERE PPSN = NEW.Visit.PPSN)) THEN
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'The same person cannot visit more than 1 Pub at the same time.';
	END  IF;
END; //
DELIMITER ;

/* q6 */
CREATE VIEW COVID_NUMBERS AS SELECT DISTINCT Person.PCounty AS 'county', COUNT(Covid_Diagnosis.PPSN) AS 'cases' FROM Person LEFT OUTER JOIN Covid_Diagnosis ON Person.PPSN = Covid_Diagnosis.PPSN GROUP BY Person.PCounty











