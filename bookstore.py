import sqlite3
import time
import tabulate
import datetime


# define a method to generate database result when everytime back to the main menu to check the latest.
def table_view():
    # always print out the existing database record.
    print('\nExisting books:')
    view = cursor.execute('''SELECT * FROM book''')
    view = tabulate.tabulate(view.fetchall(), headers=('ID', 'Title', 'Author', 'Qty'))
    return print(f'{view}\nTable generated by {datetime.datetime.now()}\n')


# a function to verify if there is record exist,
# A row data will be return if existed, otherwise return 'None'.
def search_by_id(id):
    view = cursor.execute('''SELECT * FROM book WHERE ID = ?''', (id,)).fetchone()
    return view


def table_add(title, author, qty):
    cursor.execute('''INSERT INTO book (TITLE, AUTHOR, QTY) VALUES (?,?,?)''', (title, author, qty))
    return print('New book added.')


def table_update(id, field, data):
    # this code is to check if there is row exist according to the id number which unique primary key,
    # to ensure there is actual row updated since sqlite3 would not prompt error code if row not exist.
    if search_by_id(id) is None:
        print('Record not exist, please try again.')
        time.sleep(2)
    else:
        if field == '1':
            cursor.execute('''UPDATE book SET TITLE = ? WHERE ID = ?''', (data, id))
        elif field == '2':
            cursor.execute('''UPDATE book SET AUTHOR = ? WHERE ID = ?''', (data, id))
        elif field == '3':
            cursor.execute('''UPDATE book SET QTY = ? WHERE ID = ?''', (data, id))
        return print('Record updated.')


# search for deletion
def table_delete(id):
    if search_by_id(id) is None:
        print('Record not exist, please try again.')
        time.sleep(2)
    else:
        cursor.execute('''DELETE FROM book WHERE ID = ?''', (id,))
        return print('Record deleted.')


# search for searching by non-ID.
def table_search(field, data):
    if field == '1':
        if search_by_id(data) is None:
            print('Record not exist, please try again.')
            time.sleep(2)
        else:
            view = cursor.execute('''SELECT * FROM book WHERE ID = ?''', (search_data,))
            view = tabulate.tabulate(view.fetchall(), headers=('ID', 'Title', 'Author', 'Qty'))
            return print(f'The search result : \n{view}\nTable generated by {datetime.datetime.now()}\n')
    elif field == '2':
        view = cursor.execute('''SELECT * FROM book WHERE TITLE LIKE ?''', (f'%{search_data}%',))
        view = tabulate.tabulate(view.fetchall(), headers=('ID', 'Title', 'Author', 'Qty'))
        return print(f'The search result : \n{view}\nTable generated by {datetime.datetime.now()}\n')
    elif field == '3':
        view = cursor.execute('''SELECT * FROM book WHERE AUTHOR LIKE ?''', (f'%{search_data}%',))
        view = tabulate.tabulate(view.fetchall(), headers=('ID', 'Title', 'Author', 'Qty'))
        return print(f'The search result : \n{view}\nTable generated by {datetime.datetime.now()}\n')
    elif field == '4':
        view = cursor.execute('''SELECT * FROM book WHERE QTY LIKE ?''', (search_data,))
        view = tabulate.tabulate(view.fetchall(), headers=('ID', 'Title', 'Author', 'Qty'))
        return print(f'The search result : \n{view}\nTable generated by {datetime.datetime.now()}\n')


db = sqlite3.connect('books_db')
cursor = db.cursor()

# create TABLE book and with table existence exception.
try:
    cursor.execute(
        '''CREATE TABLE book (ID integer PRIMARY KEY, TITLE varchar(200), AUTHOR varchar(200), QTY integer)''')
    db.commit()
except sqlite3.OperationalError:
    print('** TABLE book already existed. **')

cursor = db.cursor()
# prepare pre-define data for table initializing.
book = [(3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
        (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40),
        (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
        (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
        (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)]

# input pre-define data to TABLE book.
try:
    cursor.executemany('''INSERT INTO book VALUES (?,?,?,?)''', book)
    db.commit()
except sqlite3.IntegrityError:
    print('** INSERT data already existed. **')

print('** If you would like to test the table creation SQL, please delete the \'books_db\' as needed. **\n')
time.sleep(5)

while True:
    cursor = db.cursor()
    table_view()
    time.sleep(2)
    user_action = input('''Please select your action
    1 - Enter new book
    2 - Update a book
    3 - Delete a book
    4 - Search a book
    0 - Exit system without save
    00 - Save and exit system
    Action : ''')

    if user_action == '1':
        new_title = input('Provide new book title : ')
        new_author = input('Provide new book author name : ')
        try:
            new_qty = int(input('Provide book quantity : '))
        except ValueError:
            print('Wrong input, please input a number as quantity.')
            time.sleep(2)
            continue
        table_add(new_title, new_author, new_qty)
    elif user_action == '2':
        try:
            update_id = int(input('Which record to be updated? (ID number) : '))
        except ValueError:
            print('Wrong input, please confirm the ID number.')
            time.sleep(2)
            continue

        update_field = input('''Which field to be updated :
        1 - Title
        2 - Author
        3 - Quantity
        Action : ''')
        if update_field == '1':
            update_data = input('Please input new title : ')
            table_update(update_id, update_field, update_data)
        elif update_field == '2':
            update_data = input('Please input new author : ')
            table_update(update_id, update_field, update_data)
        elif update_field == '3':
            try:
                update_data = int(input('Please input new quantity : '))
                table_update(update_id, update_field, update_data)
            except ValueError:
                print('Wrong input, please input a number as quantity.')
                time.sleep(2)
                continue
        else:
            print('Wrong input. Please confirm your required action.')
            time.sleep(2)
    elif user_action == '3':
        try:
            delete_id = int(input('Which ID of record to be deleted : '))
            table_delete(delete_id)
        except ValueError:
            print('Wrong input, please input a number as ID.')
            time.sleep(2)
            continue
    elif user_action == '4':
        search_field = input('''Search by which field : 
        1 - ID
        2 - Title
        3 - Author
        4 - Quantity
        Action : ''')
        if search_field == '1':
            try:
                search_data = int(input('What is the book ID : '))
                table_search(search_field, search_data)
                time.sleep(2)
            except ValueError:
                print('Wrong input, please input a number as ID.')
                time.sleep(2)
                continue
        elif search_field == '2' or search_field == '3':
            search_data = input('What key word to search : ')
            table_search(search_field, search_data)
            time.sleep(2)
        elif search_field == '4':
            search_data = input('What quantity to search : ')
            table_search(search_field, search_data)
            time.sleep(2)
    elif user_action == '0':
        db.rollback()
        db.close()
        exit()
    elif user_action == '00':
        db.commit()
        db.close()
        exit()
    else:
        print('Wrong input')