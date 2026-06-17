from PySide6.QtCore import QObject

class TempQueue(QObject):
    """Temporary queue manager that stores orders in memory only"""
    def __init__(self):
        super(TempQueue, self).__init__()
        self.queue = []  # List to store temporary orders
        self.next_id = 1  # Auto-increment ID for temporary orders
    
    def add_order(self, customer_data):
        """Add new order to temporary queue"""
        order = {
            'temp_id': self.next_id,
            'customer_id': customer_data.get('customer_id'),
            'name': customer_data['name'],
            'phone_number': customer_data['phone_number'],
            'address': customer_data['address'],
            'formula_name': customer_data['formula_name'],
            'amount': customer_data['amount'],
            'car_number': customer_data['car_number'],
            'child_cement': customer_data['child_cement'],
            'comment': customer_data['comment']
        }
        self.queue.append(order)
        self.next_id += 1
        return order
    
    def get_all_orders(self):
        """Get all orders in queue"""
        return self.queue
    
    def remove_order(self, temp_id):
        """Remove order from queue by temp_id"""
        self.queue = [order for order in self.queue if order['temp_id'] != temp_id]
    
    def clear_queue(self):
        """Clear all orders from queue"""
        self.queue = []
        self.next_id = 1
    
    def get_order_by_temp_id(self, temp_id):
        """Get specific order by temp_id"""
        for order in self.queue:
            if order['temp_id'] == temp_id:
                return order
        return None
