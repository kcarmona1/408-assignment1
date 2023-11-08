import sqlite3
import csv
import requests
import random

# -- import feature --

conn = sqlite3.connect('./StudentDB.db')
mycursor = conn.cursor()

def import_data():
    advisors = ["Foobar", "Farboo", "Foofoo", "Barbar"]
    with open('./students.csv', 'r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        i = 1
        for row in reader:
            random_advisor = random.choice(advisors)
            mycursor.execute("INSERT INTO Student VALUES (?,?,?,?,?,?,?,?,?,?,?,?);",
                             (i, row[0], row[1], row[8], row[7], random_advisor, row[2], row[3], row[4], row[5], row[6],0))
            i += 1
        conn.commit()
    print('Data import complete.')

# -- other features --

# function to display all active students in the database
def display_all():
    mycursor.execute("SELECT StudentID, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber FROM Student WHERE isDeleted = 0")
    rows = mycursor.fetchall()
    for row in rows:
         print(row)

# function to add a student given all attributes
def add_student(firstName, lastName, gpa, major, facultyAdvisor, address, city, state, zipcode, number):
    mycursor.execute("SELECT MAX(StudentID) FROM Student")
    maxID = mycursor.fetchone()
    mycursor.execute("INSERT INTO Student VALUES (?,?,?,?,?,?,?,?,?,?,?,?);",
                     ((maxID[0]+1), firstName, lastName, gpa, major, facultyAdvisor, address, city, state, zipcode, number, 0))
    conn.commit()

# function to update student information (major, faculty advisor, or phone number) given the student, field, and updated info
def update_students(student, field, info):
    if field == 1:
        mycursor.execute("UPDATE Student SET Major = ? WHERE StudentId = ?", (info, student,))
    if field == 2:
        mycursor.execute("UPDATE Student SET FacultyAdvisor = ? WHERE StudentId = ?", (info, student,))
    if field == 3:
        mycursor.execute("UPDATE Student SET MobilePhoneNumber = ? WHERE StudentId = ?", (info, student,))
    conn.commit()

# function to soft delete a student given the studentid
def delete_student(studentid):
    mycursor.execute("UPDATE Student SET isDeleted = ? WHERE StudentId = ?", (1, studentid,))
    conn.commit()

# display students by the desired category and specific option in that category
def display_by(field, info):
    if field == 1:
        mycursor.execute(
            "SELECT StudentID, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber FROM Student WHERE isDeleted = 0 AND Major = ?",
            (info,))
        rows = mycursor.fetchall()
        for row in rows:
            print(row)

    if field == 2:
        mycursor.execute(
            "SELECT StudentID, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber FROM Student WHERE isDeleted = 0 AND GPA = ?",
            (info,))
        rows = mycursor.fetchall()
        for row in rows:
            print(row)

    if field == 3:
        mycursor.execute(
            "SELECT StudentID, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber FROM Student WHERE isDeleted = 0 AND City = ?",
            (info,))
        rows = mycursor.fetchall()
        for row in rows:
            print(row)

    if field == 4:
        mycursor.execute(
            "SELECT StudentID, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber FROM Student WHERE isDeleted = 0 AND State = ?",
            (info,))
        rows = mycursor.fetchall()
        for row in rows:
            print(row)

    if field == 5:
        mycursor.execute(
            "SELECT StudentID, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber FROM Student WHERE isDeleted = 0 AND FacultyAdvisor = ?",
            (info,))
        rows = mycursor.fetchall()
        for row in rows:
            print(row)

# application menu

print("Welcome to the Student Database Management System.")
exit_command = False

while exit_command == False:
    print("Please choose an option:")
    print("1: Display all students")
    print("2: Add a new student")
    print("3: Update a students Major, Advisor, or Phone Number")
    print("4: Delete a student")
    print("5: Search student by Major, GPA, City, State, or Advisor")
    print("6: Import students.csv to populate database (Select only once to avoid duplicate records imported)")
    print("7: Exit")
    print("")

    user_option = input()

    if user_option == "1":
        print("StudentID, First Name, Last Name, GPA, Major, Faculty Advisor, Address, City, State, Zip Code, Phone Number")
        display_all()
        print("\nActive students displayed.\n")
        continue

    if user_option == "2":
        firstName, lastName, gpa, major, facultyAdvisor, address, city, state, zipcode, number = 0,0,0,0,0,0,0,0,0,0
        print("Please provide the following student information:")
        firstName = str(input("First Name: ")).title()
        lastName = str(input("Last Name: ")).title()
        major = str(input("Major: ")).title()
        facultyAdvisor = str(input("Faculty Advisor: ")).title()
        address = str(input("Address: ")).title()
        city = str(input("City: ")).title()
        state = str(input("State: ")).title()
        zipcode = str(input("Zip Code: "))
        number = str(input("Phone Number: "))
        while True:
            try:
                gpa = float(input("GPA: "))
            except ValueError:
                print("Invalid input. Please enter a valid GPA (Ex. 4.0, 3.2, etc).")
                continue
            else:
                break

        add_student(firstName, lastName, gpa, major, facultyAdvisor, address, city, state, zipcode, number)
        print('\nNew student has been added.\n')
        continue

    if user_option == "3":
        while True:
            try:
                studentID = int(input("Enter a StudentID: "))
            except ValueError:
                print("Invalid input. Please try again.")
                continue
            else:
                break
        print("Choose a field to update:")
        while True:
            try:
                field = int(input("(1) Major\n(2) Faculty Advisor\n(3) Phone Number\n"))
                print(field)
                if field == 1 or field == 2 or field == 3:
                    break
                else:
                    print("Invalid input. Please enter a valid selection (1, 2, 3).")
                    continue
            except ValueError:
                print("Invalid input. Please enter a valid selection (1, 2, 3).")
                continue
            else:
                break
        info = input("Enter the updated student information for the field you have chosen:\n").title()
        update_students(studentID, field, info)
        print("\nStudent information has been updated.\n")
        continue

    if user_option == "4":
        while True:
            try:
                student = int(input("Enter the StudentID you would like to delete: "))
                mycursor.execute("SELECT EXISTS(SELECT * FROM STUDENT WHERE StudentID = ?);", (student,))
                exists = mycursor.fetchone()
                if exists == 0:
                    print("That StudentID does not exist in the database. Please try again.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a valid ID.")
                continue
            else:
                break
        delete_student(student)
        print("\nStudent has been deleted.\n")
        continue

    if user_option == "5":
        print("Choose a field to search:")
        while True:
            try:
                field = int(input("(1) Major, (2) GPA, (3) City, (4) State, (5) Advisor\n"))
                if field == 1 or field == 2 or field == 3 or field ==4 or field == 5:
                    break
                else:
                    print("Invalid input. Please enter a valid selection (1, 2, 3, 4, 5).")
                    continue
            except ValueError:
                print("Invalid input. Please enter a valid selection (1, 2, 3, 4, 5).")
                continue
            else:
                break
        info = input("Input the information for the field you would like to search: ").title()
        display_by(field, info)
        print("\nStudents with desired criteria have been displayed.\n")
        continue

    if user_option == "6":
        import_data()
        continue

    if user_option == "7":
        print("Thank you for using the Student Database Management System. Goodbye!")
        mycursor.close()
        exit_command = True
    else:
        print("Invalid option. Please try again.\n")


