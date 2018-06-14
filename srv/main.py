from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from flaskext.mysql import MySQL
from classes.auth import Auth
from classes.sql import SQL
from classes.user import User
from classes.hasher import Hasher
from classes.book import Book
from classes.bookcontent import BookContent
import os, hashlib, json

app = Flask(__name__)
CORS(app)
auth = Auth('pukabooksrv')
sql = SQL()
hasher = Hasher()
os.system("sudo service mysql restart")

# Load xml data into array
    # data = open('../test4.xml', 'r').read()
    # test = data
    # soup = BeautifulSoup(test)
    
    # qwe = []
    
    # paraph = ''
    # for asd in soup.findAll('token'):
    #     # qwe.append(asd.string)
    #     paraph += ' ' + asd.string
    #     if asd.string.endswith('.'):
    #         # print(paraph)
    #         qwe.append(paraph)
    #         paraph = ''
# print(json.loads(request.data)['test1'])

# https://python-server-vicjod.c9users.io:8081/phpmyadmin/ -> phpmyadm

# @app.route('/route', methods=['GET', 'POST', "PUT", "DELETE"]) -> Define 
@app.route('/login', methods=['POST'])
def login():
    result = auth.checkData()
    
    if result['auth']:
        user = User()
        
        userInfo = {
            'id' : user.idUser,
            'user' : user.user,
            'pass' : user.password,
            'email': user.email,
            'guser' : user.gUser,
        }
        
        result['userinfo'] = userInfo
        
    return jsonify({'result' : result})
    
@app.route('/register', methods=['POST'])
def register():
    result = {}
    
    user = auth.getUserPass64Decode(auth.getArraydcd())
    isRegister = sql.checkUser(user[0], user[1])
    
    username = json.loads(request.data)['username']
    
    if isRegister == False:
        result['register'] = sql.registerUser(user[0], user[1], username)
        
    return jsonify({'result' : result})
    
@app.route('/login/google', methods=['POST'])
def loginGoogle():
    result = {}
    
    gUser = auth.getUserPass64Decode(auth.getArraydcd())
    isRegister = sql.checkUser(gUser[0], gUser[1])
    
    username = json.loads(request.data)['username']
    
    if isRegister == True:
        result = auth.checkData()
        user = User()
        
        userInfo = {
            'id' : user.idUser,
            'user' : user.user,
            'pass' : user.password,
            'email': user.email,
            'guser' : user.gUser,
        }
        
        result['userinfo'] = userInfo
        
    elif sql.registerUser(gUser[0], gUser[1], username, 1) == True:
        result = auth.checkData()
        user = User()
    
        userInfo = {
            'id' : user.idUser,
            'user' : user.user,
            'pass' : user.password,
            'email': user.email,
            'guser' : user.gUser,
        }
            
        result['userinfo'] = userInfo

    return jsonify({'result' : result})
    
@app.route('/updateuser', methods=['POST'])
def updateUser():
    result = auth.checkData()
    
    if result['auth']:
        section = json.loads(request.data)['section']
        data = json.loads(request.data)['data']
        user = User()
        print(section, data)
        result['update'] = sql.updateUser(data, section, user.idUser)
    
    return jsonify({'result' : result})

@app.route('/books/<section>', methods=['POST'])
def getBooks(section):
    result = auth.checkData()
    if result['auth']:
        if section == "home":
            user = User()
            lastbook = sql.getHomeBook(user.idUser)
            
            if lastbook :
                result['lastbook'] = lastbook[0]
                result['books'] = sql.getSimilarBooksByBook(lastbook[0]['id'])
        elif section == "explore":
            result['books'] = sql.getAllBooks()
        elif section == "author":
            idAuthor = json.loads(request.data)['authorcode']
            result['books'] = sql.getBooksByAuthor(idAuthor)
        elif section == "readings":
            user = User()
            result['books'] = sql.getReadingsBooks(user.idUser)
        elif section == "readlater":
            user = User()
            result['books'] = sql.getReadLaterBooks(user.idUser)
    
    return jsonify({'result': result})
    
@app.route('/book/<code>', methods=['POST'])
def getBookDetails(code):
    result = auth.checkData()
    if result['auth']:
        book = Book(code)
        result['book'] = book.bookO
        result['author'] = book.authorO
    
    return jsonify({'result': result})
    
@app.route('/searchbooks/<section>/<filt>', methods=['POST'])
def searchBooksBy(section, filt):
    result = auth.checkData()
    if result['auth']:
        words = json.loads(request.data)['words']
        if section == 'explore':
            result['books'] = sql.searchBooks(filt, words)
        elif section == 'readlater':
            user = User()
            result['books'] = sql.searchReadLater(words, user.idUser)
        elif section == 'readings':
            user = User()
            result['books'] = sql.searchPendings(words, user.idUser)
    return jsonify({'result': result})
    
@app.route('/readlater/<section>', methods=['POST'])
def readLater(section):
    result = auth.checkData()
    if result['auth']:
        idBook = json.loads(request.data)['idbook']
        user = User()
        if section == 'check':
            result['isReadLater'] = sql.checkReadLater(user.idUser, idBook)
            result['books'] = sql.getSimilarBooksByBook(idBook)
        elif section == 'add':
            result['addReadLater'] = sql.addReadLater(user.idUser, idBook)
        elif section == 'remove':
            result['removeReadLater'] = sql.removeReadLater(user.idUser, idBook)
    return jsonify({'result': result})
    
@app.route('/read/<idbook>/<lang>', methods=['POST'])
def eReader(idbook, lang):
    result = auth.checkData()
    
    if result['auth']:
        user = User()
        result['alines'] = sql.getAlines(idbook, user.idUser)[0]['alines']
        
        bfile = sql.getBfile(idbook)[0]['bfile']
        bookcontent = BookContent(bfile, lang)
        result['content'] = bookcontent.content
    return jsonify({'result': result})
    
@app.route('/updatelines/<idbook>/<alines>', methods=['POST'])
def updateAlines(idbook, alines):
    result = auth.checkData()
    
    if result['auth']:
        user = User()
        result['update'] = sql.updateAlines(idbook, user.idUser, alines)
    
    return jsonify({'result': result})
      
@app.route('/images/<section>', methods=['GET'])
def authorImages(section):
    file = "images/" + section + "/" + request.args.get('image') + ".jpg"
    return send_file(file)


if __name__ == '__main__':
    app.run(host = os.getenv('IP','0.0.0.0'), port = int(os.getenv('PORT',8080)))
