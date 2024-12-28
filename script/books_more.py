from flask import Blueprint, render_template, request, session, redirect, url_for
from faker import Faker

books_more = Blueprint('books_more', __name__)
faker = Faker()

# Static image links for the books
STATIC_IMAGES = [f"https://picsum.photos/id/{i}/200/200" for i in range(1, 101)]

def get_random_category():
    categories = ["Action", "Romance", "Poetry", "Fantasy", "Mystery", "Thriller", "Science Fiction", "Biography"]
    return faker.random.choice(categories)

def create_random_book(index):
    book = {
        'id': faker.uuid4(),
        'name': f"{faker.word().upper()} - {faker.word()}",
        'author': faker.name(),
        'price': round(faker.random.uniform(10, 40), 2),
        'rating': round(faker.random.uniform(3, 5), 1),
        'stock': faker.random_int(min=0, max=100),
        'description': faker.sentence(nb_words=10),
        'category': get_random_category(),
        'img': STATIC_IMAGES[index % len(STATIC_IMAGES)]
    }
    return book

@books_more.route('/books', methods=['GET', 'POST'])
def generate_books():
    if request.method == 'POST':
        num_books = int(request.form.get('num_books', 10))
        session['books'] = [create_random_book(i) for i in range(num_books)]
    
    books = session.get('books', [])
    return render_template('home/web.html', books=books, num_books=len(books))

@books_more.route('/book/<string:id>', methods=['GET'])
def book(id):
    books = session.get('books', [])
    selected_book = next((book for book in books if book['id'] == id), None)
    if selected_book:
        return render_template('home/book_details.html', book=selected_book)
    else:
        return "Book not found", 404

@books_more.route('/add-to-cart/<string:id>', methods=['POST'])
def add_to_cart(id):
    books = session.get('books', [])
    selected_book = next((book for book in books if book['id'] == id), None)
    if selected_book:
        cart = session.get('cart', [])
        cart.append(selected_book)
        session['cart'] = cart
        return render_template('home/cart.html', cart=cart)
    else:
        return "Book not found", 404

@books_more.route('/cart', methods=['GET'])
def view_cart():
    cart = session.get('cart', [])
    return render_template('home/cart.html', cart=cart)

@books_more.route('/logout', methods=['GET'])
def logout():
    session.clear()  # Clear the session for logout
    return redirect(url_for('books_more.generate_books'))


@books_more.route('/remove-from-cart/<string:id>', methods=['POST'])
def remove_from_cart(id):
    cart = session.get('cart', [])
    cart = [book for book in cart if book['id'] != id]
    session['cart'] = cart
    return redirect(url_for('books_more.view_cart'))



@books_more.route('/purchase', methods=['POST'])
def purchase():
    cart = session.get('cart', [])
    books = session.get('books', [])

    # Process each book in the cart
    for cart_item in cart:
        # Find the book in the books list
        selected_book = next((book for book in books if book['id'] == cart_item['id']), None)
        if selected_book:
            # Decrease stock of the book by 1
            selected_book['stock'] -= 1

    # Clear the cart after purchase (or leave it as is, depending on your preference)
    session['cart'] = []

    # Redirect to cart view after purchase
    return redirect(url_for('books_more.view_cart'))



@books_more.route('/filter/<string:filter>', methods=['POST'])
def filter(filter):
    books = session.get('books', [])
    


@books_more.route('/search/<string:filter>', methods=['POST'])
def search(search):
    books = session.get('books', [])
