# models.py
import hashlib 
class User: 
    def __init__(self, user_id, username, password): 
        self._user_id = user_id 
        self._username = username 
        self._password = self._hash_password(password) 
 
    def _hash_password(self, password): 
        return hashlib.sha256(password.encode()).hexdigest() 
 
    @property 
    def user_id(self): 
        return self._user_id 
 
    @property 
    def username(self): 
        return self._username 
 

 
class LibraryItem: 
    def __init__(self, item_id, title, author): 
        self._item_id = item_id 
        self._title = title 
        self._author = author 
 
    @property 
    def item_id(self): 
        return self._item_id 
 
    @property 
    def title(self): 
        return self._title 
 
    @property 
    def author(self): 
        return self._author 
 

 
class Book(LibraryItem): 
    def __init__(self, book_id, title, author, publication_year, genre): 
        super().__init__(book_id, title, author) 
        self._publication_year = publication_year 
        self._genre = genre 
 
    @property 
    def publication_year(self): 
        return self._publication_year 
 
    @property 
    def genre(self): 
        return self._genre 