from classes.sql import SQL
sql = SQL()

class Author:
    
    authorO = None
    
    def __init__(self, idAuthor):
        self.authorO = sql.getAuthor(idAuthor)[0]