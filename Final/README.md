# ESB Group Buying

ESB is a group buying platform that allows users to purchase products at a discounted price. The platform is controlled by the manufacturing firm ESB, with no middlemen involved, ensuring a direct producer-to-consumer process. ESB aims to simplify group buying while increasing sales through promotions.

## Distinctiveness and Complexity

-   Adopts a group purchase model, unlike traditional e-commerce sites.
-   This project has multiple product categories, including major and subcategories, as opposed to project 2, which only has a single category.
-   For _Users_:
    -   Account registration requires email verification to ensure account authenticity.
    -   Buyer eligibility based on complete account information.
    -   View ongoing and pending orders. Buyers can cancel the pending orders they joined, but once an order is in progress, cancellation is no longer allowed.
    -   Users can create orders for active products and join existing orders for active/inactive products.
    -   Users can search for products through the search bar.
-   For _Admin_(Manufacturer):
    -   Each order has target quantity and expiration dates; production only begins when targets are met.
    -   Admin can allow users to create orders for specific products or only join orders created by admin.
    -   Multiple images can be uploaded to a product instead of via URL.
    -   Admins can cancel or adjust customer orders at any time.

## Files Contain

-   **_`esb`_** App folder
    -   **_`static/esb`_** Static folder
        -   **_`image`_** Image folder that contains the images of products uploaded by admin
        -   `create.js` Contains 6 functions for uploading, displaying, deleting, and toggling images, as well as options to display products according to the selected category when creating products
        -   `layout.js` Contains 2 functions to view and edit account informations when users click the Settings
        -   `manage_products.js` This section contains 3 functions for deleting and toggling the product's status and displaying the description based on screen size
        -   `order_details.js` Contains 7 functions for managing buyer's and product's orders, including edit, save edit, and delete for both, as well as the ability to save edits by clicking the enter key
        -   `order.js` Set a interval to automatically update the current order quantity in this order every 10 seconds without reloading the page
        -   `product.js` Function for toggling images
        -   `styles.css` Used to define the appearance of a web page
    -   **_`templates/esb`_** Template folder
        -   `category.html` Users can search for products through broad and detailed classifications (large and fine categories)
        -   `categoryP.html` The search results display products based on the selected categories
        -   `create_order.html` Admin can use this page to create orders based on the products
        -   `create_product.html` Admin can create new products using this page
        -   `index.html` Home Page
        -   `inprogress.html` Display ongoing orders for easy user participation
        -   `layout.html` This is a template for all HTML files in this application
        -   `login.html` For login
        -   `manage_layout.html` Management templates for orders and products
        -   `manage_orders.html` Admin can view and check the status of all orders.
        -   `manage_products.html` Admin can view all products' details and delete products
        -   `myorder.html` Users can view their joined orders in this page.
        -   `order_details.html` Display order details, enabling Admin to edit order requirements, customer's ordered quantity, and delete product/customer orders
        -   `order.html` Display the order details to allow users to make an informed decision on whether to join the order or not
        -   `pagination.html` Contains reusable code for pagination functionality, which can be easily implemented in other HTML files.
        -   `pendings.html` Show orders that are still in pendings for user participation
        -   `product.html` Display product details, let users know the detailed information of the product
        -   `register.html` For register
        -   `search.html` Utilized to present the user's search product results
        -   `settings.html` This page is for setting account information, and completion of the content is required for users to participate in group buying
    -   `admin.py` Customize the management interface according to your preferences
    -   `models.py` Contains the models utilized by the web application
    -   `urls.py` Where we can set up URL to View function mappings
    -   `views.py` Where we can set up functions to trigger when a particular route is visited
-   `.env.example` Stores email credentials for automatic verification email).
-   `README.md` A guide that gives detailed description of a project.

## Installation

1. Install the required python libraries by running the following command:

```python
pip install -r requirements.txt
```

2. Create new database migration files for the _`esb`_ app and applies the changes to the database schema.

```
python manage.py makemigrations esb
python manage.py migrate
```

3. Open .env.example, set the email address and password

```
export EMAIL_HOST_USER="<PUT YOUR EMAIL HERE>"
export EMAIL_HOST_PASSWORD="<PUT YOUR EMAIL PASSWORD HERE>"
```

`EMAIL_HOST_USER` specifies the email account used to send user account activation emails for the application.

`EMAIL_HOST_PASSWORD` is used to set the password for the email account specified in _`EMAIL_HOST_USER`_ . It allows Django to authenticate with the email server in order to send emails.

4. Rename the `.env.example` file to `.env` and start the Django development server by running the following commands:

```
source .env-sample
python manage.py runserver
```
