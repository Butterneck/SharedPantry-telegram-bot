DROP TABLE IF EXISTS Users, Prodotti, User_Prodotti, Debits, Activator;

CREATE TABLE Users(
    Id SERIAL PRIMARY KEY,
	Username VARCHAR(255) NOT NULL UNIQUE,
	Chat_Id INT NOT NULL UNIQUE
);

CREATE TABLE Prodotti(
    Id SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Price FLOAT NOT NULL,
    Quantity INT NOT NULL
);

CREATE TABLE User_Prodotti(
    Id SERIAL PRIMARY KEY,
    User_Id INT NOT NULL REFERENCES Users(Id) ON DELETE NO ACTION ,
    Prodotto_Id INT NOT NULL REFERENCES Prodotti(Id) ON DELETE NO ACTION,
	Data Date NOT NULL,
	Quantity INT NOT NULL
);

CREATE TABLE Debits(
    Id SERIAL PRIMARY KEY,
    User_Id INT NOT NULL,
    Quantity INT NOT NULL,
    Month INT NOT NULL,
    Paid INT NOT NULL,

    FOREIGN KEY(User_Id) REFERENCES Users(Id)
);

CREATE TABLE Activator(
    Id SERIAL PRIMARY KEY,
    Activator INT NOT NULL
);
