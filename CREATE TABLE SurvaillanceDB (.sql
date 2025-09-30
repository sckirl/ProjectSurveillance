CREATE TABLE SurveillanceDB (
    surveillanceID CHAR(36) PRIMARY KEY,
    surveillanceTime DATETIME,
    surveillanceImg VARBINARY(MAX),
    surveillanceMap VARBINARY(MAX),
    latitude VARCHAR(20),
    longitude VARCHAR(20),
    altitude VARCHAR(20)
);

-- Query table
SELECT * FROM SurveillanceDB

DROP TABLE SurveillanceDB