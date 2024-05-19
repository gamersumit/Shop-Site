Shop Site Project
Overview
This project is an online shop site built using Django and GraphQL. It offers functionalities for user authentication, item and category management, shopping cart operations, and order processing. The admin has control over the menu items, while users can interact with the cart and place orders.

Features
User Authentication:

User login and registration
Email verification
Menu Management:

Category and Item models
Only admins can create, update, and delete (CUD) categories and items
Shopping Cart:

Fetch cart items
Add items to cart
Unique cart for each user
Order Management:

Place orders using the cart
Cart is emptied after placing an order
GraphQL mutation for placing an order (PlaceOrder)
Query single and multiple orders
Batch Create Items:

Batch creation of items
Items can belong to multiple categories
Technologies Used
Django
GraphQL
DjangoObjectType (Graphene-Django)
PostgreSQL (or any preferred database)
Installation
Clone the repository:

bash
Copy code
git clone <repository_url>
cd shop-site
Create and activate a virtual environment:

bash
Copy code
python3 -m venv env
source env/bin/activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up the database:

bash
Copy code
python manage.py makemigrations
python manage.py migrate
Create a superuser:

bash
Copy code
python manage.py createsuperuser
Run the development server:

bash
Copy code
python manage.py runserver
Usage
User Authentication
Users can register, log in, and verify their email addresses.
Menu Management
Admin users can create, update, and delete categories and items through the admin interface.
Shopping Cart
Users can add items to their cart, view the cart, and update quantities.
Order Management
Users can place orders using the items in their cart.
The PlaceOrder mutation is used to place an order.
Users can query their single or multiple orders.
GraphQL API
Queries
Fetch Cart:

graphql
Copy code
query {
    cart {
        id
        items {
            id
            item {
                name
                price
            }
            quantity
        }
    }
}
Fetch Single Order:

graphql
Copy code
query($id: UUID!) {
    order(id: $id) {
        id
        orderedAt
        subtotalAmount
        taxAmount
        discountAmount
        totalAmount
        orderItems {
            id
            item {
                name
            }
            quantity
            price
        }
    }
}
Fetch Multiple Orders:

graphql
Copy code
query {
    orders {
        id
        orderedAt
        totalAmount
    }
}
Mutations
Place Order:

graphql
Copy code
mutation {
    placeOrder {
        order {
            id
            orderedAt
            totalAmount
        }
    }
}
Add to Cart:

graphql
Copy code
mutation($itemId: ID!, $quantity: Int!) {
    addToCart(itemId: $itemId, quantity: $quantity) {
        cart {
            id
            items {
                id
                item {
                    name
                    price
                }
                quantity
            }
        }
    }
}
Screenshots
Home Page

Menu Management

Shopping Cart

Order History

Contributing
Fork the repository.
Create a new branch for your feature or bugfix.
Commit your changes.
Push to your branch.
Create a pull request.
