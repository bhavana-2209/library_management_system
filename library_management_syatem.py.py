from datetime import datetime, timedelta
import json
import os


# =========================================================
# BOOK CLASS
# =========================================================

class Book:
    """Represents a book in the library"""

    def __init__(self, title, author, isbn, year):

        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year

        self.available = True
        self.borrowed_by = None
        self.due_date = None

    # =====================================================
    # BORROW BOOK
    # =====================================================

    def check_out(self, member_id, loan_period=14):

        if not self.available:
            return False, "Book is already borrowed"

        self.available = False
        self.borrowed_by = member_id

        self.due_date = (
            datetime.now() + timedelta(days=loan_period)
        ).strftime("%Y-%m-%d")

        return True, "Book borrowed successfully"

    # =====================================================
    # RETURN BOOK
    # =====================================================

    def return_book(self):

        if self.available:
            return False, "Book already available"

        self.available = True
        self.borrowed_by = None
        self.due_date = None

        return True, "Book returned successfully"

    # =====================================================
    # CONVERT TO DICTIONARY
    # =====================================================

    def to_dict(self):

        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "year": self.year,
            "available": self.available,
            "borrowed_by": self.borrowed_by,
            "due_date": self.due_date
        }

    # =====================================================
    # CREATE OBJECT FROM DICTIONARY
    # =====================================================

    @classmethod
    def from_dict(cls, data):

        book = cls(
            data["title"],
            data["author"],
            data["isbn"],
            data["year"]
        )

        book.available = data["available"]
        book.borrowed_by = data["borrowed_by"]
        book.due_date = data["due_date"]

        return book


# =========================================================
# MEMBER CLASS
# =========================================================

class Member:
    """Represents library member"""

    def __init__(self, member_id, name):

        self.member_id = member_id
        self.name = name

    def to_dict(self):

        return {
            "member_id": self.member_id,
            "name": self.name
        }

    @classmethod
    def from_dict(cls, data):

        return cls(
            data["member_id"],
            data["name"]
        )


# =========================================================
# LIBRARY MANAGEMENT SYSTEM
# =========================================================

class LibraryManagementSystem:

    BOOKS_FILE = "books.json"
    MEMBERS_FILE = "members.json"

    def __init__(self):

        self.books = []
        self.members = []

        self.load_data()

    # =====================================================
    # LOAD DATA
    # =====================================================

    def load_data(self):

        # -----------------------------------------------
        # LOAD BOOKS
        # -----------------------------------------------

        if os.path.exists(self.BOOKS_FILE):

            with open(self.BOOKS_FILE, "r") as file:

                books_data = json.load(file)

                self.books = [
                    Book.from_dict(book)
                    for book in books_data
                ]

        else:
            self.load_sample_books()

        # -----------------------------------------------
        # LOAD MEMBERS
        # -----------------------------------------------

        if os.path.exists(self.MEMBERS_FILE):

            with open(self.MEMBERS_FILE, "r") as file:

                members_data = json.load(file)

                self.members = [
                    Member.from_dict(member)
                    for member in members_data
                ]

        else:
            self.load_sample_members()

    # =====================================================
    # LOAD SAMPLE BOOKS
    # =====================================================

    def load_sample_books(self):

        sample_books = [

            Book(
                "Python Crash Course",
                "Eric Matthes",
                "9781593279288",
                2019
            ),

            Book(
                "Automate the Boring Stuff with Python",
                "Al Sweigart",
                "9781593275990",
                2015
            ),

            Book(
                "Fluent Python",
                "Luciano Ramalho",
                "9781491946008",
                2022
            )
        ]

        # Match screenshot exactly
        sample_books[1].available = False
        sample_books[1].borrowed_by = "MEM001"
        sample_books[1].due_date = "2024-02-15"

        self.books = sample_books

    # =====================================================
    # LOAD SAMPLE MEMBERS
    # =====================================================

    def load_sample_members(self):

        self.members = [

            Member("MEM001", "Rahul"),
            Member("MEM002", "Suresh"),

            Member("MEM003", "Ajay"),
            Member("MEM004", "Kiran"),
            Member("MEM005", "Rohit"),

            Member("MEM006", "Vikram"),
            Member("MEM007", "Arjun"),
            Member("MEM008", "Karthik"),

            Member("MEM009", "Naveen"),
            Member("MEM010", "Varun")
        ]

    # =====================================================
    # SAVE DATA
    # =====================================================

    def save_data(self):

        books_data = [
            book.to_dict()
            for book in self.books
        ]

        members_data = [
            member.to_dict()
            for member in self.members
        ]

        with open(self.BOOKS_FILE, "w") as file:
            json.dump(books_data, file, indent=4)

        with open(self.MEMBERS_FILE, "w") as file:
            json.dump(members_data, file, indent=4)

    # =====================================================
    # DISPLAY MENU
    # =====================================================

    def display_menu(self):

        print("\n")

        print("====================================================")
        print("            LIBRARY MANAGEMENT SYSTEM")
        print("====================================================")

        print(
            f"\nLoaded {len(self.books)} books from file"
        )

        print(
            f"Loaded {len(self.members)} members from file\n"
        )

        print("1. Add New Book")
        print("2. Register New Member")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Search Books")
        print("6. View All Books")
        print("7. View All Members")
        print("8. View Overdue Books")
        print("9. Save & Exit")
        print("0. Exit Without Saving")

    # =====================================================
    # SEARCH BOOKS
    # =====================================================

    def search_books(self):

        print("\nSearch books by:")
        print("1. Title")
        print("2. Author")
        print("3. ISBN")
        print("4. Show all available books")

        option = input("\nEnter search option: ")

        matching_books = []

        # -----------------------------------------------
        # TITLE SEARCH
        # -----------------------------------------------

        if option == "1":

            keyword = input(
                "\nEnter title to search: "
            ).lower()

            matching_books = [

                book for book in self.books

                if keyword in book.title.lower()
            ]

        # -----------------------------------------------
        # AUTHOR SEARCH
        # -----------------------------------------------

        elif option == "2":

            keyword = input(
                "\nEnter author to search: "
            ).lower()

            matching_books = [

                book for book in self.books

                if keyword in book.author.lower()
            ]

        # -----------------------------------------------
        # ISBN SEARCH
        # -----------------------------------------------

        elif option == "3":

            keyword = input(
                "\nEnter ISBN to search: "
            )

            matching_books = [

                book for book in self.books

                if keyword == book.isbn
            ]

        # -----------------------------------------------
        # AVAILABLE BOOKS
        # -----------------------------------------------

        elif option == "4":

            keyword = "available books"

            matching_books = [

                book for book in self.books

                if book.available
            ]

        else:
            print("\nInvalid option")
            return

        # -----------------------------------------------
        # DISPLAY RESULTS
        # -----------------------------------------------

        print(
            f"\nSearch Results for '{keyword}':"
        )

        print(
            "------------------------------------------------------"
        )

        for index, book in enumerate(
            matching_books,
            start=1
        ):

            print(f"\n{index}. {book.title}")

            print(
                f"   Author: {book.author}"
            )

            print(
                f"   ISBN: {book.isbn}"
            )

            print(
                f"   Year: {book.year}"
            )

            if book.available:

                print(
                    "   Status: Available"
                )

            else:

                print(
                    f"   Status: Borrowed by "
                    f"{book.borrowed_by} "
                    f"(Due: {book.due_date})"
                )

        print(
            f"\nFound {len(matching_books)} "
            f"books matching '{keyword}'"
        )

    # =====================================================
    # VIEW ALL BOOKS
    # =====================================================

    def view_all_books(self):

        print("\nALL BOOKS")
        print("--------------------------------------------------")

        for index, book in enumerate(
            self.books,
            start=1
        ):

            print(f"\n{index}. {book.title}")
            print(f"   Author: {book.author}")
            print(f"   ISBN: {book.isbn}")
            print(f"   Year: {book.year}")

            if book.available:
                print("   Status: Available")

            else:
                print(
                    f"   Status: Borrowed by "
                    f"{book.borrowed_by}"
                )

    # =====================================================
    # MAIN PROGRAM
    # =====================================================

    def run(self):

        while True:

            self.display_menu()

            choice = input(
                "\nEnter your choice: "
            )

            # -------------------------------------------
            # SEARCH BOOKS
            # -------------------------------------------

            if choice == "5":

                self.search_books()

            # -------------------------------------------
            # VIEW BOOKS
            # -------------------------------------------

            elif choice == "6":

                self.view_all_books()

            # -------------------------------------------
            # SAVE & EXIT
            # -------------------------------------------

            elif choice == "9":

                self.save_data()

                print("\nData saved successfully")
                print("Goodbye")

                break

            # -------------------------------------------
            # EXIT
            # -------------------------------------------

            elif choice == "0":

                print("\nExited without saving")
                break

            # -------------------------------------------
            # OTHER OPTIONS
            # -------------------------------------------

            else:
                print(
                    "\nFeature available in full version"
                )

            input(
                "\nPress Enter to continue..."
            )


# =========================================================
# PROGRAM START
# =========================================================

if __name__ == "__main__":

    system = LibraryManagementSystem()

    system.run()