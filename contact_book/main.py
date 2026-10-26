from util import render_screen,loading_animation
from util import ContactBook
import os
import platform

# Clears the screen based on the operating system
def clear_screen():
    command = 'cls' if platform.system() == 'Windows' else 'clear'
    os.system(command)

def main():
    loading_animation()
    c_book = ContactBook()

    while True:
        clear_screen()
        render_screen()

        print()
        user_input = input("OPTION IN : ")
        print()

        if user_input == "0":
            print("GoodBye !!!....")
            break

        elif user_input == "1":
            f_name = input("First Name : ")
            l_name = input("Lst Name : ")
            phone = ""
            try:
                print()
                phone = int(input("Phone : "))
            except ValueError:
                print("Invalid Number..")
            print()
            email = input("Email : ")
            note = input("Notes : ")
            c_book.add_cont(f_name,l_name,phone,email,note)

        elif user_input == "2":
            if c_book.displ():
                print()
                id = input("Contact ID : ")
                c_book.delete_cont(id)

        elif user_input == "3":
            if c_book.displ():
                print()
                id = input("Contact ID : ")
                f_name = input("First Name : ")
                l_name = input("Lst Name : ")
                phone = ""
                try:
                    print()
                    phone = int(input("Phone : "))
                except ValueError:
                    print("Invalid Number..")
                print()
                email = input("Email : ")
                note = input("Notes : ")
                c_book.update_cont(id,f_name,l_name,phone,email,note)

        elif user_input == "4":
            c_book.get_cont()

        elif user_input == "5":
            if c_book.displ():
                print()
                id = input("Contact ID :")
                c_book.fav(id)

        elif user_input == "6":
            if c_book.displ():
                print()
                id = input("Contact ID :")
                c_book.unfav(id)

        elif user_input == "7":
            if c_book.displ():
                print()
                id = input("Contact ID : ")
                c_book.filt(id=id)

        elif user_input == "8":
            c_book.filt(favorite=True)

        elif user_input == "9":
            name = input("Input First [&/Or] Last name : ")
            c_book.filt(name=name)

        elif user_input == "10":
            phone = input("Phone : ")
            c_book.filt(phone=phone)

        elif user_input == "11":
            email = input("Email : ")
            c_book.filt(email=email)

        elif user_input == "12":
            c_book.stat()


        print()
        input("Enter to continue : ")

if __name__ == "__main__":
    main()