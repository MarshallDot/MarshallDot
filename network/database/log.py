import logging


def logger():
    db = logging.getLogger("database")
    db.setLevel(logging.DEBUG)
    dbHand = logging.FileHandler(filename='./logs/database.log',
                                 encoding='utf-8', mode='w')
    dbHand.setFormatter(logging.Formatter('%(asctime)s, %(process)s, %(levelname)s, %(name)s: %(message)s'))
    db.addHandler(dbHand)
