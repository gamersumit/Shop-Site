# Shop Site Project : 

<h3>Overview</h3>

This project is an online shop site built using Django and GraphQL. It offers functionalities for user authentication, item and category management, shopping cart operations, and order processing. The admin has control over the menu items, while users can interact with the cart and place orders.

<h4>Note: </h4> This project provides only the backend functionalities. A separate frontend application would be needed to interact with this backend.

<h3> Features </h3>
<ol>
<li><h4> User Authentication:</h4></li>
<ul>
<li><h5> User login and registration </h5></li>
<li><h5> Email verification </h5></li
</ul>
<li><h4> Menu Management: </h4></li>
<ul>
<h5> Category and Item models </h5>
<h5> Only admins can create, update, and delete (CUD) categories and items </h5>
</ul>    
</ol>

<h4>   3. Shopping Cart: </h4>

<h5>      > Fetch cart items </h5>
<h5>      > Add items to cart </h5>
<h5>      > Unique cart for each user </h5>

<h4>   4. Order Management: </h4>

<h5>      > Place orders using the cart</h5>
<h5>      > Cart is emptied after placing an order</h5>
<h5>      > GraphQL mutation for placing an order (PlaceOrder)</h5>
<h5>      > Query single and multiple orders</h5>


<h4>   5. Batch Create Items:</h4>

<h5>      > Batch creation of items</h5>
<h5>      > Items can belong to multiple categories</h5>


<h3> Technologies Used </h3>

<h5>   > Django</h5>
<h5>   > GraphQL</h5>
<h5>   > DjangoObjectType (Graphene-Django)</h5>
<h5>   > SQL </h5>


<h3> Installation(MAC/LINUX/WINDOWS) :- </h3>
<h5>   1. Clone the repository:</h5>    
<h6>      => git clone <repository_url></h6>
<h6>      => cd shop-site</h6>

<h5>   2. Create and activate a virtual environment: </h5>
<h6>      MAC => python3 -m venv env</h6>
<h6>      LINUX/WIN => python -m venv env</h6>
<h6>      MAC/LINUX => source env/bin/activate</h6>
<h6>      WIN => env/script/activate</h6>

<h5>   3. Install dependencies:</h5>
<h6>      WIN/LINUX => pip install -r requirements.txt</h6>
<h6>      MAC => pip3 install -r requirements.txt</h6>

<h5>   4. Make .env file</h5>

<h5>   5. Set up the database:</h5>
<h6>      => python manage.py makemigrations</h6>
<h6>      => python manage.py migrate</h6>


<h5>   6. Create a superuser:</h5>
<h6>      => python manage.py createsuperuser</h6>

<h5>   7. Run the development server:</h5>
<h6>      => python manage.py runserver</h6>

<h2>Usage:</h2>
<h4>  User Authentication <h4>
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
