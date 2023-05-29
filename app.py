from flask import Flask, jsonify, request
from status_codes import Codes
from products import products


app = Flask(__name__)

api_v1 = '/products_api/v1/'

@app.route(api_v1 + 'products')
def getProducts():
    return jsonify({
        'status': Codes.OK,
        'products': products
    })

@app.route(api_v1 + 'products/<string:product_name>')
def getProduct(product_name):
    productFound = searchProduct(product_name)
    if len(productFound) > 0:
        return jsonify({
            'status': Codes.OK,
            'product': productFound
        })
    return jsonify({
        'status': Codes.OK,
        'message': 'No product found.'
    })

@app.route(api_v1 + 'products', methods=['POST'])
def addProduct():
    jsonData = request.json
    productExists = searchProduct(jsonData['name'])
    if not len(productExists) > 0:
        newProduct = {
            'name': jsonData['name'], 
            'description': jsonData['description'], 
            'price': jsonData['price'], 
            'quantity': jsonData['quantity']
        }
        products.append(newProduct)
        return jsonify({
            'status': Codes.OK,
            'products': products
        })
    return jsonify({
            'status': Codes.BAD,
            'message': 'Product already exists.'
            })

@app.route(api_v1 + 'products/<string:product_name>', methods=['PUT'])
def updateProduct(product_name):
    jsonData = request.json
    productFound = searchProduct(product_name)
    if len(productFound) > 0:
        productFound[0]['name'] = jsonData['name']
        productFound[0]['description'] = jsonData['description']
        productFound[0]['price'] = jsonData['price']
        productFound[0]['quantity'] = jsonData['quantity']
        return jsonify({
            'status': Codes.OK,
            'product': productFound[0]
        })
    return jsonify({
            'status': Codes.BAD,
            'message': 'Product not found.'
            })

@app.route(api_v1 + 'products/<string:product_name>', methods=['DELETE'])
def deleteProduct(product_name):
    productFound = searchProduct(product_name)
    if len(productFound) > 0:
        products.remove(productFound[0])
        return jsonify({
            'status': Codes.OK,
            'products': products
        })
    return jsonify({
        'status': Codes.BAD,
        'message': "Product not found."
    })

def searchProduct(product_name):
    productFound = [product for product in products if product['name'] == product_name]
    return productFound

if __name__ == '__main__':
    app.run(debug=True, port=4000)