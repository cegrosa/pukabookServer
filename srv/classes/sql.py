from flask import Flask, jsonify
from flaskext.mysql import MySQL
from hasher import Hasher
import hashlib, string

class SQL:
    
    app = Flask(__name__)
    mysql = MySQL()
    hasher = Hasher()
    
    def __init__(self):
        self.app.config['MYSQL_DATABASE_USER'] = 'vicjod'
        self.app.config['MYSQL_DATABASE_PASSWORD'] = ''
        self.app.config['MYSQL_DATABASE_DB'] = 'library'
        self.app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        
    def checkUser(self, email, password):
        self.mysql.init_app(self.app)
        
        query = "SELECT * FROM `users`"
        
        cur = self.mysql.connect().cursor()
        cur.execute(query)
        
        try:
            r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
            if len(r) == 0:
                print('No username/password')
            else:
                for row in r:
                    emailUser = unicode(row['email'])
                    passwordUser = unicode(row['password'])
                    
                    if self.hasher.compareStrings(email, emailUser) and password == passwordUser:
                        return True
                return False
        except:
            print('Error CheckUser')
            
    def getUser(self, email, password):
        self.mysql.init_app(self.app)
        
        query = "SELECT * FROM `users`"
        
        cur = self.mysql.connect().cursor()
        cur.execute(query)
        
        try:
            r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
            if len(r) == 0:
                print('No username/password')
            else:
                for row in r:
                    emailUser = unicode(row['email'])
                    passwordUser = unicode(row['password'])
                    
                    if self.hasher.compareStrings(email, emailUser) and password == passwordUser:
                        user = {}
                        user['iduser'] = row['id']
                        user['user'] = unicode(row['user'])
                        user['guser'] = row['guser']
                        
                        return user
                return False
        except:
            print('Error getUser')
            
    def registerUser(self, email, password, username, gUser = 0):
        self.mysql.init_app(self.app)
        
        query = '''
            INSERT INTO `users`(`id`, `user`, `password`, `email`, `guser`) VALUES
                (NULL,''' + "'" + username  + "', '" + password + "', '" + email + "', " + str(gUser) + ")"
        
        try:
            con = self.mysql.connect()
            cur = con.cursor()
            cur.execute(query)
            con.commit()
            return True
        except:
            return False
            
    def updateUser(self, data, section, idUser):
        self.mysql.init_app(self.app)
        
        column = ""
        idUserStr = str(idUser)
        
        if section == 'email':
            column = '`email`'
        elif section == 'user':
            column = '`user`'
        elif section == 'pass':
            column = '`user`'
        
        query = "UPDATE `users` SET " + section + " = '" + data + "' WHERE id = " + idUserStr
        
        try:
            con = self.mysql.connect()
            cur = con.cursor()
            cur.execute(query)
            con.commit()
            return True
        except:
            return False
    
            
    def getHomeBook(self, idUser):
        self.mysql.init_app(self.app)

        query = '''
            SELECT `books`.`id` ,  `books`.`photo` , 
                    `books`.`bfile` ,  `books`.`bname`
                FROM  `books` 
                    INNER JOIN  `readings` ON  `books`.`id` =  `readings`.`idbook` 
                WHERE  `readings`.`iduser` =''' + str(idUser) + '''
                ORDER BY  `readings`.`lastreading` DESC
                LIMIT 1'''
        
        cur = self.mysql.connect().cursor()
        cur.execute(query)
        
        try:
            r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
            if len(r) == 0:
                print('No books')
            else:
                return r
        except:
            print('Error getHomeBooks')
        
        
    def getAllBooks(self):
        self.mysql.init_app(self.app)
        
        query = '''SELECT  `id` ,  `photo` ,  `bname` FROM  `books` 
                        ORDER BY `id` DESC'''
        
        cur = self.mysql.connect().cursor()
        cur.execute(query)
        
        try:
            r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
            if len(r) == 0:
                print('No books')
            else:
                return r
        except:
            print('Error getAllBooks')
            
    def getReadingsBooks(self, iduser):
        self.mysql.init_app(self.app)
        
        idUserStr = str(iduser)
        
        query = '''SELECT  `books`.`id` , `books`.`photo` ,  `books`.`bname` FROM  `books`
                    	INNER JOIN `readings` on `books`.`id` = `readings`.`idbook`
                    		WHERE `readings`.`iduser` like ''' + idUserStr + '''
                    	ORDER BY  `readings`.`lastreading` DESC'''
        
        cur = self.mysql.connect().cursor()
        cur.execute(query)
        
        try:
            r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
            if len(r) == 0:
                print('No books')
            else:
                return r
        except:
            print('Error getReadingsBooks')
            
    def getReadLaterBooks(self, iduser):
        self.mysql.init_app(self.app)
        
        idUserStr = str(iduser)
        
        query = '''SELECT  `books`.`id` ,  `books`.`photo` ,  `books`.`bname` FROM  `books`
                    	INNER JOIN `read_later` on `books`.`id` = `read_later`.`idbook`
                    		WHERE `read_later`.`iduser` like ''' + idUserStr
        
        cur = self.mysql.connect().cursor()
        cur.execute(query)
        
        try:
            r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
            if len(r) == 0:
                print('No books')
            else:
                return r
        except:
            print('Error getReadingsBooks')
            
    def getBook(self, idBook):
        self.mysql.init_app(self.app)
        
        query = '''SELECT `books`.`id`, `books`.`photo`, `books`.`bname`,
                    `books`.`synopsis`, `genres`.`genre`, `books`.`idauthor` 
                    	FROM `books`
                    		INNER JOIN `genres` ON `books`.`idgenre` = `genres`.`id` 
                		WHERE `books`.`id` = ''' + idBook
        
        cur = self.mysql.connect().cursor()
        cur.execute(query)
        
        try:
            r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
            if len(r) == 0:
                print('No book')
            else:
                return r
        except:
            print('Error getBook')
            
    def getAuthor(self, idAuthor):
        self.mysql.init_app(self.app)
    
        query = "SELECT * FROM `author` WHERE `id` = " + str(idAuthor)
        
        cur = self.mysql.connect().cursor()
        cur.execute(query)
        
        try:
            r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
            if len(r) == 0:
                print('No author')
            else:
                return r
        except:
            print('Error getAuthor')
            
    def getSimilarBooksByBook(self, idBook):
        self.mysql.init_app(self.app)
        
        idBookStr = str(idBook)
        
        query = '''
            SELECT t.`id`, t.`photo`, t.`bname`, t.`synopsis`, `genres`.`genre`, t.`idauthor`  from
            	((SELECT * FROM `books` as book WHERE `idgenre` like (SELECT `idgenre` from `books` WHERE `id` = ''' + idBookStr + ''')) UNION
            	(SELECT * FROM `books` as book WHERE `idauthor` like (SELECT `idauthor` from `books` where `id` = ''' + idBookStr + ''')) UNION
            	(SELECT * FROM `books` as book WHERE `idcollect` like (SELECT `idcollect` from `books` where `id` = ''' + idBookStr + '''))) as t
            		INNER JOIN `genres` ON t.`idgenre` = `genres`.`id`
            		WHERE t.`idgenre` = `genres`.`id`
            		    AND t.`id` NOT LIKE ''' + idBookStr + '''
            		ORDER BY RAND()
            		LIMIT 6
        '''
        
        cur = self.mysql.connect().cursor()
        cur.execute(query)
        
        try:
            r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
            if len(r) == 0:
                print('No Books')
            else:
                return r
        except:
            print('Error getSimilarBooksByBook')

    def getBooksByAuthor(self, idAuthor):
        self.mysql.init_app(self.app)
        
        idAuthorStr = str(idAuthor)
        
        query = "SELECT * FROM `books` WHERE `idauthor` =" + idAuthorStr + '''
                ORDER BY RAND()
         		LIMIT 6'''
        
        cur = self.mysql.connect().cursor()
        cur.execute(query)
        
        try:
            r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
            if len(r) == 0:
                print('No Books')
            else:
                return r
        except:
            print('Error getBooksByAuthor')
            
    def searchBooks(self, column, words):
        self.mysql.init_app(self.app)
        
        if column  == "name":
            query = "SELECT * FROM `books` WHERE `bname` like '%" + words + "%'"
        elif column == "genre":
            query = '''
                SELECT * FROM `books` WHERE `idgenre` like
                    (SELECT `id` FROM `genres` WHERE `genre` like '%''' + words + "%')"
        elif column == "author":
            query = '''
                SELECT * FROM `books` WHERE `idauthor` like
                    (SELECT `id` FROM `author` WHERE `first` like '%''' + words + "%' OR `last` like '%" + words + "%')"
        elif column == "collection":
            query = '''
                SELECT * FROM `books` WHERE `idcollect` like
                    (SELECT `id` FROM `collections` WHERE `namecollection` like '%''' + words + "%')"
        
        cur = self.mysql.connect().cursor()
        cur.execute(query)
        
        try:
            r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
            if len(r) == 0:
                print('No Books')
            else:
                return r
        except:
            print('Error searchBooks')
            
    def searchReadLater(self, words, idUser):
        self.mysql.init_app(self.app)
        
        idUserStr = str(idUser)
        
        query = '''
            SELECT * FROM `books`
            	INNER JOIN `read_later` ON `books`.`id` = `read_later`.`idbook`
            	WHERE `read_later`.`iduser` = ''' + idUserStr + '''
            		AND `books`.`bname` like''' + "'%" + words + "%'"
        
        cur = self.mysql.connect().cursor()
        cur.execute(query)
        
        try:
            r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
            if len(r) == 0:
                print('No Books')
            else:
                return r
        except:
            print('Error searchBooks')
            
    def searchPendings(self, words, idUser):
        self.mysql.init_app(self.app)
        
        idUserStr = str(idUser)
        
        query = '''
            SELECT * FROM `books`
            	INNER JOIN `readings` ON `books`.`id` = `readings`.`idbook`
            	WHERE `readings`.`iduser` = ''' + idUserStr + '''
            		AND `books`.`bname` like''' + "'%" + words + "%'"
        
        cur = self.mysql.connect().cursor()
        cur.execute(query)
        
        try:
            r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
            if len(r) == 0:
                print('No Books')
            else:
                return r
        except:
            print('Error searchBooks')
            
            
    def checkReadLater(self, idUser, idBook):
        self.mysql.init_app(self.app)
        
        idBookStr = str(idBook)
        idUserStr = str(idUser)
        
        query = '''
            SELECT * FROM `read_later` WHERE
                `iduser` like ''' + idUserStr + ''' AND
                `idbook` like ''' + idBookStr
        
        cur = self.mysql.connect().cursor()
        cur.execute(query)
        
        try:
            r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
            if len(r) == 0:
                return False
            else:
                return True
        except:
            print('Error checkReadLater')
         
            
    def addReadLater(self, idUser, idBook):
        self.mysql.init_app(self.app)
        
        idBookStr = str(idBook)
        idUserStr = str(idUser)
        
        query = '''
            INSERT INTO `read_later`(`id`, `iduser`, `idbook`)
                VALUES (NULL, ''' + idUserStr + ", " + idBookStr + ")"
        
        try:
            con = self.mysql.connect()
            cur = con.cursor()
            cur.execute(query)
            con.commit()
            return True
        except:
            return False
      
            
    def removeReadLater(self, idUser, idBook):
        self.mysql.init_app(self.app)
        
        idBookStr = str(idBook)
        idUserStr = str(idUser)
        
        query = '''
            DELETE FROM `read_later` WHERE 
                `iduser` like ''' + idUserStr + ''' AND
                `idbook` like ''' + idBookStr
        
        try:
            con = self.mysql.connect()
            cur = con.cursor()
            cur.execute(query)
            con.commit()
            return True
        except:
            return False
    
    def getBfile(self, idbook):
        self.mysql.init_app(self.app)
        
        idBookStr = str(idbook)
        
        query = "SELECT `bfile` FROM `books` WHERE `id` =" + idBookStr
        
        cur = self.mysql.connect().cursor()
        cur.execute(query)
        
        try:
            r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
            if len(r) == 0:
                print('No Books')
            else:
                return r
        except:
            print('Error getSimilarBooksByBook')
            
    def getAlines(self, idbook, iduser):
        self.mysql.init_app(self.app)
        
        idBookStr = str(idbook)
        idUserStr = str(iduser)
        
        query = '''
            SELECT `alines` FROM `readings`
            	WHERE `iduser` = ''' + idUserStr + '''
            	AND `idbook` = ''' + idBookStr
        
        cur = self.mysql.connect().cursor()
        cur.execute(query)
        
        try:
            r = [dict((cur.description[i][0], value)
                  for i, value in enumerate(row)) for row in cur.fetchall()]
            if len(r) == 0:
                return self.insertAlines(idbook,iduser)
            else:
                self.updateDateLastReading(idbook, iduser)
                return r
        except:
            print('Error getAlines')
            
    def insertAlines(self, idbook, iduser):
        self.mysql.init_app(self.app)
        
        idBookStr = str(idbook)
        idUserStr = str(iduser)
        
        query = '''
            INSERT INTO `readings`(`id`, `iduser`, `idbook`, `alines`, `lastreading`)
	            VALUES (NULL''' + ", " + idUserStr + ", " + idBookStr + ", 0, NOW())"
        
        try:
            con = self.mysql.connect()
            cur = con.cursor()
            cur.execute(query)
            con.commit()
            return self.getAlines(idbook,iduser)
        except:
            return False
            
    def updateDateLastReading(self, idbook, iduser):
        self.mysql.init_app(self.app)
        
        idBookStr = str(idbook)
        idUserStr = str(iduser)
        
        query = '''
            UPDATE `readings` SET `lastreading`= NOW()
                WHERE 
                `iduser` like ''' + idUserStr + ''' AND
                `idbook` like ''' + idBookStr
        
        try:
            con = self.mysql.connect()
            cur = con.cursor()
            cur.execute(query)
            con.commit()
            return True
        except:
            return False
            
    def updateAlines(self, idbook, iduser, alines):
        self.mysql.init_app(self.app)
        
        idBookStr = str(idbook)
        idUserStr = str(iduser)
        alinesStr = str(alines)
        
        query = '''
            UPDATE `readings` SET `alines`=''' + alines + '''
                WHERE 
                `iduser` like ''' + idUserStr + ''' AND
                `idbook` like ''' + idBookStr
        
        try:
            con = self.mysql.connect()
            cur = con.cursor()
            cur.execute(query)
            con.commit()
            return True
        except:
            return False
        