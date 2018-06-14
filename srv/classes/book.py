from classes.sql import SQL
from classes.author import Author
import json
sql = SQL()

class Book:
    
    bookO = None
    authorO = None
    
    def __init__(self, idBook):
        self.bookO = sql.getBook(idBook)[0]
        self.authorO = Author(self.bookO['idauthor']).authorO
        