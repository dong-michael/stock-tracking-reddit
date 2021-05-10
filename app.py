from search_subreddit import *
from chart import *

search = search_subreddit()


def menu():
    has_quit = False
    

    while not has_quit:
        user_command = input("""\n Please select from the following options:
        1) Fetch stock ticker data from wallstreetbets
        2) Visualize Data from wallstreetbets
        3) Clear data gathered
        Q) Quit
         """).lower()

        if user_command == "1":
            print("Let's what everyone's talking about today!")
            retrieve_data()
        elif user_command == "2":
            print("Let's visualize the data we have collected so far..")
            visualize_all_data()
        elif user_command == "3":
            print("Let's start fresh!")
            clear_table()
        elif user_command == "q":
            print("Thank you and please invest responsibly!")
            has_quit = True
        


def retrieve_data():
    print("\n Retrieving data from wallstreetbets from May 1, 2021 onwards. Please be patient.")
    search.extract_data_from_subreddit()
    print(" \n Up to 100 entries retrieved and recorded.")

def visualize_all_data():
    stocks_stored = search.get_mention_from_table()
    visualize_data(stocks_stored).show()

def clear_table():
    search.clear_mention_table()

menu()

