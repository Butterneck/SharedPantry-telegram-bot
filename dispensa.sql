CREATE TABLE Users(
	Username VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE Prodotti(
  Name VARCHAR(255) NOT NULL,
  Price FLOAT NOT NULL,
  Quantity INT NOT NULL
);

CREATE TABLE User_Prodotti(
  User_Id INT NOT NULL,
  Prodotto_Id INT NOT NULL,
	Data Date NOT NULL,
	Quantity INT NOT NULL,

  FOREIGN KEY(User_Id) REFERENCES Users(Id),
  FOREIGN KEY(Prodotto_Id) REFERENCES Prodotti(Id)
);
