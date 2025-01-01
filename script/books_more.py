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
        num_books = int(request.form.get('num_books', session.get('num_books', 10)))
        session['num_books'] = num_books
        session['books'] = [create_random_book(i) for i in range(num_books)]
        session['filtered_books'] = session['books']
        print(f"Books generated and stored in session: {session['books']}")  # Debug log
    elif not session.get('books'):
        num_books = session.get('num_books', 10)
        session['books'] = [create_random_book(i) for i in range(num_books)]
        session['filtered_books'] = session['books']
        print(f"Default books initialized: {session['books']}")  # Debug log

    books = session.get('filtered_books', session.get('books', []))
    num_books = len(books)
    return render_template('home/web.html', books=books, num_books=num_books)


@books_more.route('/book/<string:id>', methods=['GET'])
def book(id):
    books = session.get('books', [])
    selected_book = next((book for book in books if book['id'] == id), None)

    # Debugging: Check if selected_book is None
    if selected_book is None:
        print(f"Book with ID {id} not found.")  # Debug log

    if selected_book:
        return render_template('home/book_details.html', book=selected_book)
    else:
        return "Book not found", 404  # Return a message if book is not found


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
    session.clear()  
    return redirect(url_for('auth.login'))


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

    for cart_item in cart:
        selected_book = next((book for book in books if book['id'] == cart_item['id']), None)
        if selected_book:
            selected_book['stock'] -= 1
    session['cart'] = []

    # Redirect to cart view after purchase
    return redirect(url_for('books_more.view_cart'))




@books_more.route('/filter', methods=['GET'])
def filter_books():
    # Retrieve all books from the session
    all_books = session.get('books', [])
    if not all_books:
        return "No books available to filter", 400  # Ensure there are books to filter

    # Get filter criteria from request arguments
    category = request.args.get('category', '').strip()
    rating = request.args.get('rating', '').strip()
    price = request.args.get('price', '').strip()

    # Start with all books as the base for filtering
    filtered_books = all_books

    # Apply category filter
    if category:
        filtered_books = [book for book in filtered_books if book['category'].lower() == category.lower()]

    # Apply rating filter
    if rating:
        try:
            rating_value = float(rating)
            filtered_books = [book for book in filtered_books if book['rating'] >= rating_value]
        except ValueError:
            return "Invalid rating value", 400  # Handle invalid rating input

    # Apply price filter
    if price:
        try:
            price_ranges = {
                "1": (0, 10),
                "2": (10, 20),
                "3": (20, 30),
                "4": (30, 40),
                "5": (40, float('inf'))
            }
            min_price, max_price = price_ranges.get(price, (0, float('inf')))
            filtered_books = [book for book in filtered_books if min_price <= book['price'] < max_price]
        except (ValueError, KeyError):
            return "Invalid price range value", 400  # Handle invalid price input

    # Update session with the filtered books
    session['filtered_books'] = filtered_books

    # Render the template with the filtered books and slider values
    return render_template(
        'home/web.html', 
        books=filtered_books, 
        num_books=len(filtered_books), 
        category=category, 
        rating=rating, 
        price=price
    )
