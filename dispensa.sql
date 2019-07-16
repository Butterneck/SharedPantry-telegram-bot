DROP TABLE IF EXISTS Users, Prodotti, User_Prodotti;

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
    User_Id INT NOT NULL,
    Prodotto_Id INT NOT NULL,
	Data Date NOT NULL,
	Quantity INT NOT NULL,

    FOREIGN KEY(User_Id) REFERENCES Users(Id),
    FOREIGN KEY(Prodotto_Id) REFERENCES Prodotti(Id)
);
