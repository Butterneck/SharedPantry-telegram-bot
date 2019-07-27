# Cianostavernabot

Bot available at [t.me/cianostavernabot](http://t.me/cianostavernabot/)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

To run these bot you need

```
python 3.7 or higher
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
pip install -r requirements.txt
```

Per far funzionare il bot

```
python bot.py
```

## Running the tests

To test run

```
pytest
```

## Deployment

Both the bot and the database are hosted on Heroku. The deployment is manually triggerable after the test phase ended in the pipeline

## Built With

- [Python-telegram-bot](https://python-telegram-bot.org/) - The Telegram API wrapper used
- [Heroku](https://www.heroku.com) - Hosting space for the bot and the database

## Contributing

### TODOS:

- Edit messagges in order to make the conversation experience even fancier
- General code refactoring

### Version 1.0 - Available now!

The first version of this awesome bot is finally here.

Features:

- Password authentication ~ /start
- Items shop with price and quantity ~ /prendi
- Always check your bill ~ /conto
- Manage pantry ~ /gestisci
  - Add new items
  - Edit items quantity
  - Remove items
- On the last day of the month pantry owner receives a message with every user's bill and every user get his bill
- Daily backup

## Authors

- [**Butterneck**](https://gitlab.com/Butterneck)

- [**jjocram**](https://gitlab.com/jjocram)

## License

## Acknowledgments
