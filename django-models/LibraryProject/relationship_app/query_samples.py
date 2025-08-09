import os
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# 1. Query all books by a specific author
def books_by_author():
    author_name = input("Enter author name: ")
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        print(f"\nBooks by {author_name}:")
        for book in books:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print(f"No author found with name '{author_name}'")

# 2. List all books in a library
def books_in_library():
    library_name = input("\nEnter library name: ")
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"\nBooks in library '{library_name}':")
        for book in books:
            print(f"- {book.title}")
    except Library.DoesNotExist:
        print(f"No library found with name '{library_name}'")

# 3. Retrieve the librarian for a library
def librarian_for_library():
    library_name = input("\nEnter library name to find its librarian: ")
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)  # <- ✅ Using get with filter
        print(f"\nLibrarian for '{library_name}': {librarian.name}")
    except Library.DoesNotExist:
        print(f"No library found with name '{library_name}'")
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to '{library_name}'")

# Menu
if __name__ == "__main__":
    print("Choose an option:")
    print("1. List all books by a specific author")
    print("2. List all books in a library")
    print("3. Find the librarian for a library")

    choice = input("Enter 1, 2 or 3: ")

    if choice == "1":
        books_by_author()
    elif choice == "2":
        books_in_library()
    elif choice == "3":
        librarian_for_library()
    else:
        print("Invalid choice. Exiting.")
