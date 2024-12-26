from flask import Blueprint, render_template, request, redirect, url_for, session
from faker import Faker

books_more = Blueprint('books_more', __name__)

faker = Faker()

# Function to get a random category
def get_random_category():
    categories = ["Action", "Romance", "Poetry", "Fantasy", "Mystery", "Thriller", "Science Fiction", "Biography"]
    return faker.random.choice(categories)

# Function to create a random book
def create_random_book():
    id = faker.uuid4()
    img = f"https://picsum.photos/200?random={id[:8]}"  # Using part of the UUID for a unique image
    book = {
        'id': id,
        'name': f"{faker.word().upper()} - {faker.word()}",
        'author': faker.name(),
        'price': round(faker.random.uniform(10, 40), 2),
        'rating': round(faker.random.uniform(3, 5), 1),
        'stock': faker.random_int(min=-10, max=100),
        'description': faker.sentence(nb_words=10),
        'category': get_random_category(),
        'img': img
    }
    return book

# Route to generate books and display them
@books_more.route('/books', methods=['GET', 'POST'])
def generate_books():
    if request.method == 'POST':  # If it's a POST request, regenerate books
        num_books = int(request.form.get('num_books', 10))  # Default to 10 books if not specified
        session['books'] = [create_random_book() for _ in range(num_books)]  # Store books in session
    
    books = session.get('books', [])  # Get books from session (default to empty list)
    return render_template('home/web.html', books=books, num_books=len(books))

# Route to show details of a single book
@books_more.route('/book/<string:id>', methods=['GET'])
def book(id):
    books = session.get('books', [])  # Get books from session
    selected_book = next((book for book in books if book['id'] == id), None)
    if selected_book:
        return render_template('home/book_details.html', book=selected_book)
    else:
        return "Book not found", 404  # Return a 404 if the book isn't found
