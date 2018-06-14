from BeautifulSoup import BeautifulSoup
import os

class BookContent:
    
    content = []
    
    def __init__(self, bfile, lang):
        
        self.content = []
        
        langBook = ''
        
        if lang == 'es':
            langBook ='_es'
        
        path = unicode('books/' + bfile + langBook +'.xml')
        
        try:
            data = open(path, 'r').read()
        except:
            path = unicode('books/' + bfile +'.xml')
            data = open(path, 'r').read()
        
        soup = BeautifulSoup(data)
        
        for text in soup.findAll('text'):
            self.content.append(unicode(text.string))