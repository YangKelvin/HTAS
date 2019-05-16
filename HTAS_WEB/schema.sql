DROP TABLE IF EXISTS USER;
DROP TABLE IF EXISTS PERMISSION;

CREATE TABLE PERMISSION (
    PermissionID INTEGER PRIMARY KEY AUTOINCREMENT,
    PermissionName VARCHAR(20)
);

CREATE TABLE USER (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Account VARCHAR(20),
    Password VARCHAR(20),
    PermissionID INTEGER,
    Email VARCHAR(50),
    FOREIGN KEY(PermissionID) REFERENCES PERMISSION(PermissionID)
);

INSERT INTO PERMISSION (PermissionName) VALUES ('Admin');
INSERT INTO PERMISSION (PermissionName) VALUES ('Normal');
