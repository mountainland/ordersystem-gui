import requests
import json

class Ordersystem():
    def __init__(self, base_url):
        # Define base URL for API
        self.base_url = base_url

    def list_order_list_apis(self):
        """Retrieve a list of all orders"""
        url = f"{self.base_url}/orders/"
        response = requests.get(url)
        return response.json()

    def create_order_list_api(self, data):
        """Create a new order"""
        url = f"{self.base_url}/orders/"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data, headers=headers)
        return response.json()

    def retrieve_order_detail_api(self, order_id):
        """Retrieve a specific order by its id"""
        url = f"{self.base_url}/ordersystem/api/{order_id}/"
        response = requests.get(url)
        return response.json()

    def update_order_detail_api(self, order_id, data):
        """Update a specific order by its id"""
        url = f"{self.base_url}/ordersystem/api/{order_id}/"
        headers = {'Content-Type': 'application/json'}
        response = requests.put(url, data=json.dumps(data), headers=headers)
        return response.json()

    def destroy_order_detail_api(self, order_id):
        """Delete a specific order by its id"""
        url = f"{self.base_url}/ordersystem/api/{order_id}/"
        response = requests.delete(url)
        return response.status_code

    def list_product_list_apis(self):
        """Retrieve a list of all products"""
        url = f"{self.base_url}/products/"
        response = requests.get(url)
        return response.json()["products"]
        