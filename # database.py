# database.py 
import sqlite3
class LibraryDatabase: 
    def __init__(self, db_name="library.db"): 
        self._conn = sqlite3.connect(db_name) 
        self._create_tables() 
 
    def _create_tables(self): 
        with self._conn: 
            self._create_users_table() 
            self._create_books_table() 
            self._create_rentals_table() 
            self._create_authors_table() 
            self._create_genres_table() 
 
    def _create_users_table(self): 
        self._conn.execute(''' 
            CREATE TABLE IF NOT EXISTS Users ( 
                user_id INTEGER PRIMARY KEY, 
                username TEXT NOT NULL UNIQUE, 
                password TEXT NOT NULL 
            ) 
        ''') 
 
    def _create_books_table(self): 
        self._conn.execute(''' 
            CREATE TABLE IF NOT EXISTS Books ( 
                book_id INTEGER PRIMARY KEY, 
                title TEXT NOT NULL, 
                author TEXT NOT NULL, 
                publication_year INTEGER, 
                genre TEXT, 
                FOREIGN KEY (author) REFERENCES Authors(author), 
                FOREIGN KEY (genre) REFERENCES Genres(genre) 
            ) 
        ''') 
 
    def _create_rentals_table(self): 
        self._conn.execute(''' 
            CREATE TABLE IF NOT EXISTS Rentals ( 
                rental_id INTEGER PRIMARY KEY, 
                book_id INTEGER, 
                user_id INTEGER, 
                rental_date DATE NOT NULL, 
                return_date DATE, 
                FOREIGN KEY (book_id) REFERENCES Books(book_id), 
                FOREIGN KEY (user_id) REFERENCES Users(user_id) 
            ) 
        ''') 
 
    def _create_authors_table(self): 
        self._conn.execute(''' 
            CREATE TABLE IF NOT EXISTS Authors ( 
                author_id INTEGER PRIMARY KEY, 
                author TEXT NOT NULL UNIQUE 
            ) 
        ''') 
 
    def _create_genres_table(self): 
        self._conn.execute(''' 
            CREATE TABLE IF NOT EXISTS Genres ( 
                genre_id INTEGER PRIMARY KEY, 
                genre TEXT NOT NULL UNIQUE 
            ) 
        ''') 
    def create_author(self, author): 
        if not self._validate_input(author): 
            print("Invalid input. Author name is required.") 
            return 
 
        query = 'INSERT INTO Authors (author) VALUES (?)' 
        params = (author,) 
        self.execute_query(query, params) 
 
    def create_genre(self, genre): 
        if not self._validate_input(genre): 
            print("Invalid input. Genre name is required.") 
            return 
 
        query = 'INSERT INTO Genres (genre) VALUES (?)' 
        params = (genre,) 
        self.execute_query(query, params) 
 
    def create_rental(self, book_id, user_id, rental_date): 
        if not self._validate_input(book_id, user_id, rental_date): 
            print("Invalid input. Book ID, User ID, and rental date are required.") 
            return 
 
        query = 'INSERT INTO Rentals (book_id, user_id, rental_date) VALUES (?, ?, ?)' 
        params = (book_id, user_id, rental_date) 
        self.execute_query(query, params) 
 
    def update_book_info(self, book_id, title, author, publication_year, genre): 
        if not self._validate_input(book_id, title, author): 
            print("Invalid input. Book ID, title, and author are required.") 
            return 
 
        query = 'UPDATE Books SET title=?, author=?, publication_year=?, genre=? WHERE book_id=?' 
        params = (title, author, publication_year, genre, book_id) 
        self.execute_query(query, params) 
 
    def delete_user(self, user_id): 
        if not self._validate_input(user_id): 
            print("Invalid input. User ID is required.") 
            return 
 
        query = 'DELETE FROM Users WHERE user_id=?' 
        params = (user_id,) 
        self.execute_query(query, params) 
 
    def delete_book(self, book_id): 
        if not self._validate_input(book_id): 
            print("Invalid input. Book ID is required.") 
            return 
 
        query = 'DELETE FROM Books WHERE book_id=?' 
        params = (book_id,) 
        self.execute_query(query, params) 
 
    def get_all_books(self): 
        query = 'SELECT * FROM Books' 
        return self.execute_query(query) 
 
    def get_rented_books_by_user(self, user_id): 
        if not self._validate_input(user_id): 
            print("Invalid input. User ID is required.") 
            return 
 
        query = 'SELECT Books.title FROM Rentals JOIN Books ON Rentals.book_id = Books.book_id WHERE Rentals.user_id = ?' 
        params = (user_id,) 
        return self.execute_query(query, params) 
    def execute_query(self, query, params=()): 
        with self._conn: 
            try: 
                cursor = self._conn.execute(query, params) 
                return cursor.fetchall() 
            except sqlite3.Error as e: 
                print("SQLite error:", e) 
                return None 
 
    def _validate_input(self, *args): 
        return all(arg is not None and arg != "" for arg in args) 
 
    def add_user(self, username, password): 
        if not self._validate_input(username, password): 
            print("Invalid input. Username and password are required.") 
            return 
 
        query = 'INSERT INTO Users (username, password) VALUES (?, ?)' 
        hashed_password = hashlib.sha256(password.encode()).hexdigest() 
        params = (username, hashed_password) 
        self.execute_query(query, params) 
 
    def add_book(self, title, author, publication_year, genre): 
        if not self._validate_input(title, author): 
            print("Invalid input. Title and author are required.") 
            return 
 
        query = 'INSERT INTO Books (title, author, publication_year, genre) VALUES (?, ?, ?, ?)' 
        params = (title, author, publication_year, genre) 
        self.execute_query(query, params) 
 
    def rent_book(self, book_id, user_id, rental_date): 
        if not self._validate_input(book_id, user_id, rental_date): 
            print("Invalid input. Book ID, User ID, and rental date are required.") 
            return 
 
        query = 'INSERT INTO Rentals (book_id, user_id, rental_date) VALUES (?, ?, ?)' 
        params = (book_id, user_id, rental_date) 
        self.execute_query(query, params) 
 
    def get_rented_books_by_user(self, user_id): 
        if not self._validate_input(user_id): 
            print("Invalid input. User ID is required.") 
            return 
 
        query = 'SELECT Books.title FROM Rentals JOIN Books ON Rentals.book_id = Books.book_id WHERE Rentals.user_id = ?' 
        params = (user_id,) 
        return self.execute_query(query, params) 
    def save_user(self, user): 
        query = 'INSERT INTO Users (user_id, username, password) VALUES (?, ?, ?)' 
        params = (user.user_id, user.username, user._password) 
        self.execute_query(query, params) 
 
    def save_book(self, book): 
        query = 'INSERT INTO Books (book_id, title, author, publication_year, genre) VALUES (?, ?, ?, ?, ?)' 
        params = (book.item_id, book.title, book.author, book.publication_year, book.genre) 
        self.execute_query(query, params) 
 
    def save_author(self, author): 
        query = 'INSERT INTO Authors (author_id, author) VALUES (?, ?)' 
        params = (author.item_id, author.author) 
        self.execute_query(query, params) 
 
    def save_genre(self, genre): 
        query = 'INSERT INTO Genres (genre_id, genre) VALUES (?, ?)' 
        params = (genre.item_id, genre.genre) 
        self.execute_query(query, params) 
 
    def save_rental(self, rental): 
        query = 'INSERT INTO Rentals (rental_id, book_id, user_id, rental_date, return_date) VALUES (?, ?, ?, ?, ?)' 
        params = (rental.item_id, rental.book_id, rental.user_id, rental.rental_date, rental.return_date) 
        self.execute_query(query, params)