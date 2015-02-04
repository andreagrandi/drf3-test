# Welcome to Drf3test

Drf3test is a very simple API implemented using [Django Rest Framework](http://www.django-rest-framework.org/)

## API

### Orders

* **POST** `/shop/order` - **Place an Order**

Create the "order" record with general informations, create the "order_details"
records with the details of the order. During this transaction any stamp earned by the user is
added to the database and at the end voucher(s) are created if there are enough stamps available
for that user.

Example:

    [{"product": 1, "quantity": 26}, {"product": 2, "quantity": 30}]

Response:
    
    {'success': true}


### Stamps

* **GET** `/shop/stamps` - **Get Stamps**

This API method returns the total number of Stamps available for a user and allows to create
a new one.

Example:

    GET /shop/stamps

Response:

    {'stamps': 12}

* **POST** `/shop/stamps` - **Add a Stamp to the current user**

Example:

    POST /shop/stamps

Response:

    {'stamp': 1, 'success': true}

### Vouchers

This API method returns the total number of Vouchers available for the user, allows the creation
of a new Voucher and finally permits to mark a specific Voucher as redeemed.

**NOTE:** the POST method doesn't consume any Stamps when adding a new Voucher. Stamps are consumed
to generate a Voucher only during an Order placement. For consistency, when we manually add
a Stamp we don't check if a widget was ordered. This check is only made during Order placement.

* **GET** `/shop/vouchers` - **Get Vouchers**

Example: 

    /shops/vouchers

Response:
    
    {'vouchers': 10}

* **POST** `/shop/vouchers` - **Create a Voucher**

Example: 

    /shops/voucher

Response: 

    {'voucher': 1, 'success': true}

* **PUT** `/shop/vouchers` - **Set a Voucher as redeemed**

Example: 

    /shops/voucher

Response: 

    {'voucher': 1, 'success': true}

## Client

Under drftestclient/ folder of the project there is a very simple client written using **requests**
library. To use it you first need to set the **token** (available in private) in the env variable:

    export DRFTEST_TOKEN='abc123'

At this point start a Python shell and you can start using the client like this:

    import drftestclient
    drftestclient.place_order()
    drftestclient.get_stamps()
    drftestclient.get_vouchers()
