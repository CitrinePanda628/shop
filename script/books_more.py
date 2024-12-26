from flask import Blueprint, render_template, request
from faker import Faker

books_more = Blueprint('books_more', __name__)

faker = Faker()

def get_random_category():
    categories = ["Action", "Romance", "Poetry", "Fantasy", "Mystery", "Thriller", "Science Fiction", "Biography"]
    return faker.random.choice(categories)

def create_random_book():
    book = {
        'id': faker.uuid4(),
        'name': f"{faker.word().upper()} - {faker.word()}",
        'author': faker.name(),
        'price': round(faker.random.uniform(10, 40), 2),
        'rating': round(faker.random.uniform(3, 5), 1),
        'stock': faker.random_int(min=-10, max=100),
        'description': faker.sentence(nb_words=10),
        'category': get_random_category(),
        'img': f"https://picsum.photos/200?random={faker.random_int(min=1, max=1000)}"
    }
    return book

@books_more.route('/books', methods=['GET', 'POST'])
def generate_books():
    num_books = int(request.form.get('num_books'))
    books = [create_random_book() for _ in range(num_books)]
    return render_template('web.html', books=books, num_books=num_books)

@books_more.route('/book/<string:id>', methods=['GET'])
def book(id):
    selected_book = next((book for book in books if book['id'] == id), None)
    if selected_book:
        return render_template('book_details.html', book=selected_book)
    else:
        return "Book not found", 404
