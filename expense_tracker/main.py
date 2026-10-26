import platform
import os
from util import render_screen,loading_animation
from util import ExpenseTracker
from util import categories

# Clears the screen based on the operating system
def clear_screen():
    command = 'cls' if platform.system() == 'Windows' else 'clear'
    os.system(command)

def word_count(text):
    count = 0
    split_words = text.split()
    count += len(split_words)
    return count    


def main():
    loading_animation()
    e_t = ExpenseTracker()

    while True:
        clear_screen()
        render_screen()

        print()
        user_input = input("OPTION IN : ")
        print()

        if user_input == "0":
            print("GoodBye !!!")
            break

        elif user_input == "1":
            while True:
                try:
                    amount = float(input("Amount : "))
                    break
                except ValueError:
                    print("Invalid Amount, try again...")
                    print()

            while True:
                try:

                    descrip = input("Description : ")
                    if word_count(descrip) > 0:
                        break
                    else:
                        raise Exception("Word Count [0]. Invalid Description, try again...")
                except Exception as e:
                    print(f"{e}")
                    print()
            print()
            e_t.add_exp(amount,descrip)

        elif user_input == "2":
            if e_t.display_exp():
                print()
                id = input("Expense ID : ")
                e_t.delete_exp(id)


        elif user_input == "3":
            if e_t.display_exp():
                print()
                id = input("Expense ID : ")
                print()
                amount = input("Amount : ")
                if amount:
                    try:
                        amount = float(amount)
                    except ValueError:
                        print("Invalid Amount...[None]")
                        amount = None
                try:
                    print()
                    descrip = input("Description : ")
                    if word_count(descrip) > 0:
                        pass
                    else:
                        descrip = None
                        raise Exception("Word Count [0]. Invalid Description [None]...")
                except Exception as e:
                    print(f"{e}")
                print()

                e_t.update_exp(id,amount,descrip)

        elif user_input == "4":
            e_t.get_exp()

        elif user_input == "5":
            if e_t.display_exp():
                print()
                id = input("Expense ID : ")
                print()
                e_t.load_exp(id)

        elif user_input == "6":
            e_t.summ_m()

        elif user_input == "7":
            print(f"Categories : {categories}")
            print()
            categ = input("Category : ")
            print()
            e_t.summ_categ(categ)

        elif user_input == "8":
            e_t.summ_day()

        print()
        input("Enter to continue : ")


if __name__ == "__main__":
    main()