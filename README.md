<h1>Shop Site Project</h1>

<h3>Overview</h3>
<p>
This project is an online shop site built using Django and GraphQL. It offers functionalities for user authentication, item and category management, shopping cart operations, and order processing. The admin has control over the menu items, while users can interact with the cart and place orders.
</p>
<h4>Note:</h4>
<p>
This project provides only the backend functionalities. A separate frontend application would be needed to interact with this backend.
</p>
<h3>ScreenShots</h3>
<table>
  <tr>
    <td>
      <img src="Screenshots/1.jpg" width="200">
    </td>
    <td style="padding-left: 20px;">
      <img src="Screenshots/2.jpg" width="200">
    </td>
    <td style="padding-left: 20px;">
      <img src="Screenshots/3.jpg" width="200">
    </td>
    <td style="padding-left: 20px;">
      <img src="Screenshots/4.jpg" width="200">
    </td>
  </tr>
</table>
<h3>Features</h3>
<ol>
    <li>
        <h4>User Authentication:</h4>
        <ul>
            <li><h5>User login and registration</h5></li>
            <li><h5>Email verification</h5></li>
        </ul>
    </li>
    <li>
        <h4>Menu Management:</h4>
        <ul>
            <li><h5>Category and Item models</h5></li>
            <li><h5>Only admins can create, update, and delete (CUD) categories and items</h5></li>
        </ul>
    </li>
    <li>
        <h4>Shopping Cart:</h4>
        <ul>
            <li><h5>Fetch cart items</h5></li>
            <li><h5>Add items to cart</h5></li>
            <li><h5>Unique cart for each user</h5></li>
        </ul>
    </li>
    <li>
        <h4>Order Management:</h4>
        <ul>
            <li><h5>Place orders using the cart</h5></li>
            <li><h5>Cart is emptied after placing an order</h5></li>
            <li><h5>GraphQL mutation for placing an order (PlaceOrder)</h5></li>
            <li><h5>Query single and multiple orders</h5></li>
        </ul>
    </li>
    <li>
        <h4>Batch Create Items:</h4>
        <ul>
            <li><h5>Batch creation of items</h5></li>
            <li><h5>Items can belong to multiple categories</h5></li>
        </ul>
    </li>
</ol>

<h3>Technologies Used</h3>
<ul>
    <li><h5>Django</h5></li>
    <li><h5>GraphQL</h5></li>
    <li><h5>DjangoObjectType (Graphene-Django)</h5></li>
    <li><h5>SQL</h5></li>
</ul>

<h3>Installation (MAC/LINUX/WINDOWS):</h3>
<ol>
    <li>
        <h5>Clone the repository:</h5>
        <ul>
            <li><h6>git clone &lt;repository_url&gt;</h6></li>
            <li><h6>cd shop-site</h6></li>
        </ul>
    </li>
    <li>
        <h5>Create and activate a virtual environment:</h5>
        <ul>
            <li><h6>MAC: python3 -m venv env</h6></li>
            <li><h6>LINUX/WIN: python -m venv env</h6></li>
            <li><h6>MAC/LINUX: source env/bin/activate</h6></li>
            <li><h6>WIN: env\Scripts\activate</h6></li>
        </ul>
    </li>
    <li>
        <h5>Install dependencies:</h5>
        <ul>
            <li><h6>WIN/LINUX: pip install -r requirements.txt</h6></li>
            <li><h6>MAC: pip3 install -r requirements.txt</h6></li>
        </ul>
    </li>
    <li>
        <h5>Make .env file</h5>
    </li>
    <li>
        <h5>Set up the database:</h5>
        <ul>
            <li><h6>python manage.py makemigrations</h6></li>
            <li><h6>python manage.py migrate</h6></li>
        </ul>
    </li>
    <li>
        <h5>Create a superuser:</h5>
        <ul>
            <li><h6>python manage.py createsuperuser</h6></li>
        </ul>
    </li>
    <li>
        <h5>Run the development server:</h5>
        <ul>
            <li><h6>python manage.py runserver</h6></li>
        </ul>
    </li>
</ol>

<h2>Usage:</h2>
<h4>User Authentication</h4>
<p>Users can register, log in, and verify their email addresses.</p>

<h4>Menu Management</h4>
<p>Admin users can create, update, and delete categories and items through the admin interface.</p>

<h4>Shopping Cart</h4>
<p>Users can add items to their cart, view the cart, and update quantities.</p>

<h4>Order Management</h4>
<p>Users can place orders using the items in their cart. The PlaceOrder mutation is used to place an order. Users can query their single or multiple orders.</p>

<h3>GraphQL API</h3>

<h4>Queries</h4>

<h5>Fetch Cart:</h5>
<pre><code>query {
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
}</code></pre>

<h5>Fetch Single Order:</h5>
<pre><code>query($id: UUID!) {
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
}</code></pre>

<h5>Fetch Multiple Orders:</h5>
<pre><code>query {
orders {
    id
    orderedAt
    totalAmount
}
}</code></pre>

<h4>Mutations</h4>

<h5>Place Order:</h5>
<pre><code>mutation {
placeOrder {
    order {
        id
        orderedAt
        totalAmount
    }
}
}</code></pre>

<h5>Add to Cart:</h5>
<pre><code>mutation($itemId: ID!, $quantity: Int!) {
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
}</code></pre>


<h3>Contributing</h3>
<ol>
    <li>Fork the repository.</li>
    <li>Create a new branch for your feature or bugfix.</li>
    <li>Commit your changes.</li>
    <li>Push to your branch.</li>
    <li>Create a pull request.</li>
</ol>

