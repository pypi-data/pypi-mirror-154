# Flask SQLAlchemy Extension

## Install

```commandline
pip install flask-sqlalchemy-extension
```

## Usage

1. Create you own model and extend with mixins.

**model.py**
```python
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy_extension.mixins import SerializeMixin, DeserializeMixin, QueryMixin

db = SQLAlchemy()


class Category(SerializeMixin, DeserializeMixin, QueryMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)


class Product(SerializeMixin, DeserializeMixin, QueryMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def in_stock(self):
        return self.quantity > 0


class ProductCategory(SerializeMixin, DeserializeMixin, QueryMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', backref=db.backref('categories', lazy=True), lazy='joined')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('products', lazy=True), lazy='joined')
```

2. Create you own queries with complex_query function

```python
# Select all products with price lower or equal 100.
products = Product.complex_query(filter_by=dict(
    price__lte=100
))
# Select all products with price lower or equal 100 and name (case insensitive) contains `phone`.
products = Product.complex_query(filter_by=dict(
    price__lte=100,
    name__ilike='phone'
))
# Select all products, order result with price field by ascending.
products = Product.complex_query(order_by=dict(
    price='ASC'
))
```

3. Use new special functions in REST controller to operate with models.

```python
from flask import Flask, g, request
from flask_sqlalchemy_extension.func import serialize

from model import Product, db  # import your model here 


def create_app():
    app = Flask(__name__)
    # place here your create app code
    return app


app = create_app()
db.init()


# First create Before Request handler, that determinate attribute 
# to manipulate with data from URL Query part.
# e.g. http://<host>/<route>?page=5&per_page=100,
#      http://<host>/<route>?filter_by_age__gte=18
#      http://<host>/<route>?order_by_price=desc
#      http://<host>/<route>?include_something
@app.before_request
def app_context():
    g.per_page = int(request.args.get('per_page', 20))
    g.page = int(request.args.get('page', 1))

    filter_type = request.args.get('filter_type', 'and')
    filter_by = dict((k[len('filter_by_'):], v) for k, v in request.args.items()
                     if k.startswith('filter_by_') and len(k) > len('filter_by_'))
    order_by = dict((k[len('order_by_'):], v) for k, v in request.args.items()
                    if k.startswith('order_by_') and len(k) > len('order_by_'))
    g.complex_query = dict(
        filter_type=filter_type,
        filter_by=filter_by,
        order_by=order_by
    )

    g.includes = list(k[len('include_'):] for k, v in request.args.items()
                      if k.startswith('include_') and len(k) > len('include_'))


# Second create app.route handler and use new extension for easy querying data by filters, ordering,
# spliting by pages and allow include not default serializable or computed fields in response
@app.route('/products', methods=['GET'])
def get_products():
    return serialize(Product.complex_query(**g.complex_query).paginate(page=g.page, per_page=g.per_page),
                     include=g.includes)


# And you can define Create or Update data handler, that allow transfer a json-serializable object and
# easy deserialize it and save in DB. 
# Don't forget check constrains by call check_constrains() methods to prevent DB error with not-null fields.
@app.route('/product', methods=['POST'])
@app.route('/product/<int:id>', methods=['PUT'])
def create_or_update_product(id=None):
    if id is not None:
        product = Product.query.filter_by(id=id).first_or_404()
    else:
        product = Product()
    product.deserialize(request.json).check_constrains()
    db.session.add(product)
    db.session.commit()
    return product.serialize(include=g.includes)
```

## Web API

### Pagination

Pagination with REST accept URL Query attributes `page` (default is 1 in example) and `per_page` (default is 20 in example).
e.g. URL query: `http://<host>/products?page=2&per_page=10`

Return response:
```json
{
  "pagination": {
    "has_next": <bool>, // has next page (true or false)
    "next_num": <int>,  // next page number (int or None)
    "has_prev": <bool>, // has previous page (true or false)
    "prev_num": <int>,  // previous page number (int or None)
    "page": <int>,      // current page number (int)
    "page_range": [<int>, ..., <int>] // list of available pages (by default 5 pages left and 5 pages right of current page)
  },
  "items": [<obj>, ...] // list of objects in current page
}
```

### Filtering

Filtering with REST accept URL Query attributes starts with `filter_by_`.
Pass field name and filtering modifier split by two underlines after prefix.

Nested filters allowed, split child field from parent with two underline.

Use two and more filters will be added by `and` operator. For override this pass `filter_type=or` in URL Query. 

| Filtering modifier | Meaning                         |
|--------------------|---------------------------------|
| `__gte`            | greater or equal                |
| `__gt`             | strict greater                  |
| `__lt`             | strict lower                    |
| `__lte`            | lower or equal                  |
| `__neq` or `__ne`  | not equal                       |
| `__like`           | pattern search                  |
| `__like`           | case insensitive pattern search |
| `__ieq`            | case insensitive equal          |
| `__eq` or empty    | strict equal                    |

Examples: 
1. `http://<host>/products?filter_by_price__lte=100`.
Select all products with price lower or equal 100.
2. `http://<host/products?filter_by_price__lte=100&filter_by_name__ilike=phone`.
Select all products with price lower or equal 100 and name (case insensitive) contains `phone`.

### Includes

Includes with REST accept URL Query attributes starts with `include_`.  Pass field name to include after prefix.

Nested includes allowed, split child field name from parent with dot.

Example:
1. `http://<host>/products?include_categories.category&include_in_stock`
Select all products, include product categories and computed field `in_stock`.

### Ordering

Ordering with REST accept attributes starts with `order_by_` and value `DESC` or `ASC`. 

Nesting ordering allowed. Split child field name from parent with two underlines.

Example:
1. `http://<host>/products?order_by_price=ASC`
Select all products, order result with price field by ascending.
