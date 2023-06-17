# Little Lemon Restaurant API Project

This repository contains the final API project for the Little Lemon restaurant. The purpose of this project is to create a fully functioning API that allows client application developers to build web and mobile applications for the restaurant. The API enables different roles to perform various tasks such as browsing menu items, placing orders, assigning delivery crew, and managing orders.

## Project Structure

The project follows a specific structure where all API endpoints are implemented within a single Django app called LittleLemonAPI. The dependencies are managed using pipenv in a virtual environment. Please refer to the video tutorial on creating a Django project using pipenv for guidance.

## Functionality and Views

The project supports both function-based and class-based views. It is important to adhere to proper API naming conventions throughout the project. Review the video tutorial on function-based and class-based views, as well as the video tutorial on naming conventions, for further understanding.

## User Groups

There are two user groups: "Manager" and "Delivery crew". Create these groups in the Django admin panel and assign users to these groups accordingly. Users who are not assigned to any group will be considered customers. Refer to the video tutorial on user roles for more information.

## Error Handling and Status Codes

Error messages should be displayed with appropriate HTTP status codes. This includes handling non-existing items, unauthorized API requests, and invalid data in POST, PUT, or PATCH requests. The following is a list of the expected status codes:

- 200 - Ok (for successful GET, PUT, PATCH, and DELETE calls)
- 201 - Created (for successful POST requests)
- 403 - Unauthorized (if authorization fails for the current user token)
- 401 - Forbidden (if user authentication fails)
- 400 - Bad request (if validation fails for POST, PUT, PATCH, and DELETE calls)
- 404 - Not found (if the request was made for a non-existing resource)

## API Endpoints

The following sections outline the required API routes for this project categorized by functionality.

### User Registration and Token Generation Endpoints

- `POST /api/users`: Creates a new user with a name, email, and password. No role is required.
- `GET /api/users/users/me/`: Displays information about the current user.
- `POST /token/login/`: Generates access tokens that can be used in other API calls. Requires a valid username and password.

Additional endpoints will be created by Djoser, which is covered in the video tutorial on the Introduction to Djoser library for better authentication.

### Menu Items Endpoints

#### Accessible by Customers and Delivery Crew

- `GET /api/menu-items`: Lists all menu items.
- `POST /api/menu-items`, `PUT /api/menu-items`, `PATCH /api/menu-items`, `DELETE /api/menu-items`: Denies access and returns a 403 - Unauthorized HTTP status code.
- `GET /api/menu-items/{menuItem}`: Lists a single menu item.
- `POST /api/menu-items/{menuItem}`, `PUT /api/menu-items/{menuItem}`, `PATCH /api/menu-items/{menuItem}`, `DELETE /api/menu-items/{menuItem}`: Returns a 403 - Unauthorized HTTP status code.

#### Accessible by Managers

- `GET /api/menu-items`: Lists all menu items.
- `POST /api/menu-items`: Creates a new menu item and returns a 201 - Created HTTP status code.
- `GET /api/menu-items/{menuItem}`: Lists a single menu item.
- `PUT /api/menu-items/{menuItem}`, `PATCH /api/menu-items/{menuItem}`: Updates a single menu item.
- `DELETE /api/menu-items/{menuItem}`: Deletes a menu item.

### User Group Management Endpoints

#### Accessible by Managers

- `GET /api/groups/manager/users`: Returns all managers.
- `POST /api/groups/manager/users`: Assigns the user in the payload to the manager group and returns a 201 - Created HTTP status code.
- `DELETE /api/groups/manager/users/{userId}`: Removes a particular user from the manager group and returns a 200 - Success HTTP status code. Returns 404 - Not found if the user is not found.
- `GET /api/groups/delivery-crew/users`: Returns all delivery crew.
- `POST /api/groups/delivery-crew/users`: Assigns the user in the payload to the delivery crew group and returns a 201 - Created HTTP status code.
- `DELETE /api/groups/delivery-crew/users/{userId}`: Removes a user from the delivery crew group and returns a 200 - Success HTTP status code. Returns 404 - Not found if the user is not found.

### Cart Management Endpoints

#### Accessible by Customers

- `GET /api/cart/menu-items`: Returns current items in the cart for the current user token.
- `POST /api/cart/menu-items`: Adds a menu item to the cart and sets the authenticated user as the user ID for these cart items.
- `DELETE /api/cart/menu-items`: Deletes all menu items created by the current user token.

### Order Management Endpoints

#### Accessible by Customers

- `GET /api/orders`: Returns all orders with order items created by the current user.
- `POST /api/orders`: Creates a new order item for the current user. Retrieves current cart items from the cart endpoints, adds those items to the order items table, and deletes all items from the cart for this user.
- `GET /api/orders/{orderId}`: Returns all items for the given order ID. Displays an appropriate HTTP error status code if the order ID does not belong to the current user.

#### Accessible by Managers

- `GET /api/orders`: Returns all orders with order items by all users.
- `PUT /api/orders/{orderId}`, `PATCH /api/orders/{orderId}`: Updates the order. Managers can set a delivery crew and update the order status to 0 or 1.
- `DELETE /api/orders/{orderId}`: Deletes the order.

#### Accessible by Delivery Crew

- `GET /api/orders`: Returns all orders with order items assigned to the delivery crew.
- `PATCH /api/orders/{orderId}`: Updates the order status to 0 or 1. The delivery crew can only update the order status.

## Additional Steps

- Implement proper filtering, pagination, and sorting capabilities for `/api/menu-items` and `/api/orders` endpoints. Review the video tutorials and related reading material on filtering, searching, and pagination for detailed instructions.

- Apply throttling for authenticated and unauthenticated users. Review the video tutorial and reading material on API throttling for guidance.

## Conclusion

This project provides an overview of the required API endpoints and their functionalities. Use this information as a guide to successfully develop the API project. Happy coding!
