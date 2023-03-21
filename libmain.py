import mysql.connector as sqltor

#mydb = sqltor.connect(host="localhost", user="root", password="root")
# this was the original, but for current computer we use the one below
mydb = sqltor.connect(host="localhost", user="root", password="iSQLr00t731!")
cursor = mydb.cursor()
if mydb.is_connected():
    print("You are successfully connected to the database!\n")
cursor.execute("create database if not exists lib_mang")
cursor.execute("use lib_mang")
cursor.execute("create table if not exists users(roll_no varchar(20) not null, primary key (roll_no), username "
               "varchar(20) not null ,password varchar(20) not null)")


def after_query():
    print("Here are all the books in the library:")

    cursor.execute("select * from books")
    books_output = cursor.fetchall()
    for row in books_output:
        print(row)


def after_login(user):
    cursor.execute(
        "create table if not exists books(book_name varchar(30) not null, primary key(book_name), no_of_books int, authors_name varchar(30))")
    permit = input("""login with admin permission to access special admin features.

or continue as user
Do you have admin permission? (y/n):  """)
    while user is not None:
        print("""
Press 0 to Log out
Press 1 to lend/issue book
Press 2 to return book
Press 3 to display your lending history
Press 4 to search books
Press 5 to search user
Press 6 to rate book
Press 7 to display ratings of book """)
        if permit.lower() == "y":
            print("""
Special Admin Features: 
Press 8 to add book
Press 9 to update book
press 10 to delete book
press 11 to see lending history of some or all people
Press 12 to display users who have not returned books """)
            ch2 = int(input("0  /  1  /  2  /  3  /  4  /  5  /  6  /  7  /  8  /  9  /  10  /  11  /  12  :  "))
            print("\n")
            if ch2 > 12:
                print("Error, enter value less than 12.")
                print("\n")
                continue

        elif permit.lower() == "n":
            ch2 = int(input("0  /  1  /  2  /  3  /  4  /  5  /  6  /  7  :  "))
            if ch2 > 7:
                print("Error, enter value less than 7.")
                print("\n")
                continue

        else:
                print("Invalid input, enter y or n only.")
                break

        # LEND/ISSUE A BOOK
        
        if ch2 == 1:
            print("""If you want to go back press 1
If you want to continue press 2""")
            b = int(input("Enter choice: "))
            if b == 1:
                continue

            elif b == 2:
                cursor.execute(
                    "create table if not exists transact_lib(roll_no varchar(20) not null, foreign key(roll_no) references users(roll_no), book_name varchar(30) not null, foreign key(book_name) references books(book_name), authors_name varchar(30), lend_date date, exp_return_date date,act_return_date date)")
                mydb.commit()
                print("\n")
                print("Proceeding to lend/issue book")

                roll_no = input("Enter roll no: ")
                book_name = str(input("Enter name of book: "))
                authors_name = str(input("Enter name of author of book: "))
                lend_date = str(input("Enter date book was issued/lent (yyyy-mm-dd): "))
                print("""Enter expected return date as after 21 days from lend date
If book not returned then enter actual return date same as lend date """)
                exp_return_date = str(input("Enter (expected) date of return (yyyy-mm-dd): "))
                act_return_date = str(input("Enter (actual) date of return (yyyy-mm-dd): "))

                cursor.execute("select * from books where book_name='" + book_name + "'")
                for (x, y, z) in cursor:
                    if y != 0:
                        cursor.execute(
                            "Insert into transact_lib values('" + roll_no + "','" + book_name + "','" + authors_name + "','" + lend_date + "','" + exp_return_date + "','" + act_return_date + "')")
                        cursor.execute("update books set no_of_books=no_of_books-1 where book_name='" + book_name + "'")
                        mydb.commit()
                        print("\n")
                        print("------BOOK HAS LENT/ISSUED------")
                        print("\n")

                    else:
                        print("\n")
                        print("There are no books named", book_name, "available right now")
                        print("\n")
                after_query()

            else:
                print("ERROR: enter 1 or 2 only! ")
            continue

        # RETURNING A BOOK
        
        elif ch2 == 2:
            print("RETURNING A BOOK")
            print("if you wanna go back press 1")
            print(" ")
            print("if you wanna continue press 2")
            print(" ")
            a = int(input("enter your choice:"))
            if a == 2:
                roll_no = input("Enter roll no: ")
                book_name = str(input("Enter book name:"))
                print("If book is returned on same day as lend date, enter date of returning as next day. ")
                date_of_return = str(input("Enter date of returning(yyyy-mm-dd):"))
                cursor.execute(
                    "update transact_lib set act_return_date='" + date_of_return + "' where book_name='" + book_name + "'and roll_no='" + roll_no + "'")
                mydb.commit()
                print("\n")
                print("-------BOOK HAS BEEN RETURNED------")
                print("\n")
            continue
        
        #DISPLAY LENDING HISTORY

        elif ch2 == 3:
            print("Proceeding to display lending history")
            print("\n")
            roll_no = input("Enter roll no: ")
            cursor.execute("select * from transact_lib where roll_no='" + roll_no + "'")
            print(roll_no, "'S LENDING HISTORY: ")
            for i in cursor:
                print("\n")
                print(i)
            continue    
                
        #SEARCH BOOKS
        
        elif ch2 == 4:
            print("Proceeding to search books")
            print("\n")
            print("""If you want to go back press 1
If you want to continue press 2""")
            b = int(input("Enter choice: "))
            if b == 1:
                continue

            elif b == 2:
                d = int(input("""Press 1 to display all books 
Press 2 to display information about a particular book: """))

                if d == 1:
                    cursor.execute("select * from books")
                    print("\n")
                    print("ALL BOOKS IN LIBRARY: ")
                    for i in cursor:
                        print("\n")
                        print(i)

                elif d == 2:
                    bookname = input("enter the name of the book, you need information about: ")
                    cursor.execute("select * from books where book_name like '" + f"%{bookname}%" + "'")
                    for i in cursor:
                        print("\n")
                        print("Information found:  ")
                        print("\n")
                        print(i)
            else:
                print("ERROR: enter 1 or 2 only ")
            continue
        
        # SEARCH PERSON
        
        elif ch2 == 5:
            print("proceeding to search users")
            print("\n")
            print("""If you want to go back press 1
If you want to continue press 2""")
            b = int(input("Enter choice: "))
            if b == 1:
                continue

            elif b == 2:
                    search_user = input("Enter the Name or Roll Number of the user you want to search: ")
                    if search_user.isdigit():
                        cursor.execute("select roll_no, username from users where roll_no ='" + search_user + "'")
                        print('Users Found:')
                        for i in cursor:
                            print("\n")
                            print(i)
                    else:
                        cursor.execute("select roll_no, username from users where username like '" + f"%{search_user}%" + "'")
                        print('Users Found:')
                        print("\n")
                        for i in cursor:
                            print(i)
            else:
                print("ERROR: enter 1 or 2 only ")
            continue
        
        #RATE BOOK
        elif ch2 == 6:
            print("""If you want to go back press 1
If you want to continue press 2 """)
            b=int(input("Enter choice: "))
            if b == 1:
                after_query()
                continue
    
            elif b == 2:
                cursor.execute(
                    "create table if not exists rate_book(bookname varchar(30) not null, foreign key(bookname) references books(book_name), rating double, no_of_raters int)")
                bookname=input("Enter name of book to be rated: ")
                value=float(input("Rate the book on a scale of 1 to 5: "))
                if float(value)>5.0:
                        print("ERROR: enter value below 5 only ")
                elif float(value)<1.0:
                        print("ERROR: enter value above 1 only ")
                elif float(value)<=5.0 and float(value)>=1.0:
                    cursor.execute("select * from rate_book where bookname='" + bookname + "'")
                    cot=cursor.fetchone()
                
                    if cot is not None:
                        (x,y,z)=cot
                        rating= value + z*y
                        z=z+1
                        y=rating / z
                        cursor.execute(
                            "update rate_book set rating={} where bookname='{}'".format(y,bookname))
                        cursor.execute(
                            "update rate_book set no_of_raters={} where bookname='{}'".format(z,bookname))
                        mydb.commit()
                        print("\n")
                        print("RATING ADDED SUCCESSFULLY")
                        continue
                
                    elif cot is None:
                        cursor.execute(
                            "insert into rate_book values('{}',{},{})".format(bookname,value,1))
                        mydb.commit()
                        print("\n")
                        print("RATING ADDED SUCCESSFULLY")
                        continue
                    else:
                        print("enter a number only")
            
            else:
                print("ERROR: enter 1 or 2 only ")
            continue
        
        #DISPLAY RATING
        elif ch2 == 7:
            print("""If you want to go back press 1
If you want to continue press 2 """)
            c=int(input("Enter choice: "))
            if c == 1:
                after_query()
                continue
            
            if c == 2:
                print("Do you want to display rating of particular book or all books?")
                print("""
Press 1 to display rating of a particular book
Press 2 to display rating of all books """)
                d=int(input("Enter choice: "))
                
                if d == 1:
                    print("Proceeding to display rating of particular book")
                    bookname=str(input("Enter book name: "))
                    cursor.execute(
                        "select * from rate_book where bookname='"+bookname+"'")
                    for i in cursor:
                        print("\n")
                        print("RATING OF",bookname,"IS: ")
                        print(i)
                    continue
                
                elif d == 2:
                    print("Proceeding to display ratings of all books")
                    cursor.execute("select * from rate_book")
                    print("RATING OF ALL BOOKS")
                    for j in cursor:
                        print("\n")
                        print(j)
                    continue
                
                else:
                    print("ERROR: enter 1 or 2 only ")
                continue
            
        
        # ADD A BOOK
        
        if ch2 == 8:
            print("""If you want to go back press 1
If you want to continue press 2""")
            b = int(input("Enter choice: "))
            if b == 1:
                continue
            elif b == 2:
                print("Proceeding to add books")
                print("\n")
                print("PLEASE FILL BOOK DETAILS")
                book_name = str(input("enter book name: "))
                no_of_books = input("enter number of books: ")
                authors_name = str(input("Enter the authors name: "))
                cursor.execute(
                    "insert into books values('" + book_name + "','" + no_of_books + "','" + authors_name + "')")
                mydb.commit()
                print("\n")
                print("------BOOK ADDED SUCESSFULLY------")
                after_query()
                continue

        # UPDATE BOOK DETAILS
        
        elif ch2 == 9:
            print("""If you want to go back press 1
If you want to continue press 2""")
            b = int(input("Enter choice: "))
            if b == 1:
                continue
            elif b == 2:
                print("Proceeding to update book details")
                print("\n")
                print("""press 1 to update book name
Press 2 to update quantity of books
Press 3 to update author name""")
                ch3 = int(input(" 1  /  2  /  3  :  "))
                present_bookname = input("Enter the BOOK NAME whose detais are to be updated: ")
                if ch3 == 1:
                    new_bookname = input("Enter new name for book: ")
                    cursor.execute(
                        "update books set book_name='" + new_bookname + "' where book_name='" + present_bookname + "'")
                    mydb.commit()
                    print("\n")
                    print("--------THE BOOK'S NAME HAVE BEEN UPDATED-------")

                elif ch3 == 2:
                    new_no_of_books = input("Enter new number of books (quantity) : ")
                    cursor.execute(
                        "update books set no_of_books='" + new_no_of_books + "' where book_name='" + present_bookname + "'")
                    mydb.commit()
                    print("\n")
                    print("--------THE NUMBER OF BOOKS HAVE BEEN UPDATED-------")

                elif ch3 == 3:
                    new_authors_name = input("Enter new author(s) name(s): ")
                    cursor.execute(
                        "update books set authors_name='" + new_authors_name + "' where book_name='" + present_bookname + "'")
                    mydb.commit()
                    print("\n")
                    print("--------THE AUTHOR'S NAME(S) HAVE BEEN UPDATED-------")

            else:
                print("ERROR: please enter number between 1 and 3")
            after_query()
            continue
        
        #DELETE A BOOK
        
        elif ch2 == 10:
            print("""If you want to go back press 1
               If you want to continue press 2""")
            b = int(input("Enter choice: "))
            if b == 1:
                continue
            elif b == 2:
                book_name = input("Enter the BOOK NAME to be deleted: ")
                cursor.execute("delete from transact_lib where book_name='" + book_name + "'")
                cursor.execute("delete from books where book_name='" + book_name + "'")
                print("\n")
                print("-----------"+book_name.upper()+" DELETED------------")
                after_query()
            continue

        #DISPLAY LENDING HISTORY OF SOME/ALL PEOPLE
        
        elif ch2 == 11:
            print("""If you want to go back press 1
If you want to continue press 2""")
            b = int(input("Enter choice: "))
            if b == 1:
                after_query()
            elif b == 2:
                print("Proceeding to display lending history")
                print("\n")
                print("Do you want to display only individual user's lending history or everyone's? ")
                c = int(input("""Press 1 to display individual user's lending history 
Press 2 to display everyone's lending history: """))

                if c == 1:
                    roll_no = input("Enter roll no: ")
                    cursor.execute("select * from transact_lib where roll_no='" + roll_no + "'")
                    for i in cursor:
                        print("\n")
                        print(roll_no, "'S LENDING HISTORY: ")
                        print("\n")
                        print(i)

                elif c == 2:
                    cursor.execute("select * from transact_lib")
                    print("\n")
                    print("EVERYONE'S LENDING HISTORY")
                    for j in cursor:
                        print("\n")
                        print(j)

                else:
                    print("ERROR: enter 1 or 2 only! ")

            else:
                print("ERROR: enter 1 or 2 only! ")
            continue
        
        #DISPLAY USERS WHO HAVE NOT RETURNED
        
        elif ch2 == 12:
            print("Proceeding to display list of users who have not returned book")
            print("\n")
            cursor.execute("select * from transact_lib where lend_date=act_return_date")
            print("USERS WHO HAVE NOT RETURNED")
            for k in cursor:
                print("\n")
                print(k)
            continue

        # LOGOUT
        
        elif ch2 == 0:
            print("Do you want to logout?")
            a = int(input("""Enter 1 to go back
Enter 2 to continue: """))

            if a == 1:
                continue
            elif a == 2:
                user = None
                print("\n")
                print("""----------YOU ARE LOGGED OUT-------------""")

        else:
            print("""Invalid input
                  """)


while True:
    print("\n")
    print("""press 1 to create a new account (signup)
Press 2 if you are a existing user (login)
Press 3 to delete account
Press 4 to exit """)

    ch1 = int(input(" 1  /  2  /  3  /  4  :  "))

    # user puts 1 or 2 to sign up or login
    
    # CREATE NEW ACCOUNT
    
    if ch1 == 1:
        print("\n")
        global roll_no
        roll_no = input("roll number: ")
        print("\n")
        global username
        username = input("USERNAME: ")
        print("Hello, please create a PASSWORD")
        password = input("PASSWORD: ")

        cursor.execute("insert into users values('" + roll_no + "','" + username + "','" + password + "')")
        # note: '"+  +"' syntax is used to add data in users table

        mydb.commit()
        print("YOUR ACCOUNT HAS BEEN CREATED")
        print("\n")
        print("now login into your account to continue\n")


    # LOGIN
    
    elif ch1 == 2:
        roll_no = input("roll number: ")
        username = input("USERNAME: ")
        cursor.execute("select username from users where username='" + username + "' and roll_no='" + roll_no + "'")
        pot = cursor.fetchone()

        if pot is not None:
            print("hello", username, "please insert PASSWORD")
            password = input("PASSWORD: ")
            cursor.execute("select password from users where password='" + password + "'")

            login = cursor.fetchone()

            if login is not None:
                print("\n")
                print("""----------YOU ARE LOGGED IN-------------
                      
                      """)

                after_login(login)
                
            if login is  None:
                print("Invalid password for roll no ",roll_no,". Please retry.")
        
        if pot is None:
                print("Invalid username for roll no ",roll_no,". Please retry.")
                
    #DELETE ACCOUNT            

    elif ch1 == 3:
        print("Delete account?")
        a = int(input("""Enter 1 to go back
Enter 2 to continue: """))

        if a == 1:
            cursor.execute("select * from users")
            for i in cursor:
                print(i)
            

        elif a == 2:
            cursor.execute("select * from users")
            for i in cursor:
                print(i)

            print("Enter deleting details: ")
            roll_no = input("Enter roll no: ")
            username = input("Enter username: ")
            password = input("Enter password: ")
            cursor.execute("""delete from users where roll_no='"+roll_no+"'
                             and username='"+username+"' and password='"+password+"'""")
            mydb.commit()

            print("\n")
            print("--------ACCOUNT DELETED SUCCESSFULLY-------")
            print("\n")

            cursor.execute("select * from users")
            for i in cursor:
                print(i)
            continue
        
    #EXIT
    
    elif ch1 == 4:
        break

    else:
        print("""invalid input
                 """)
