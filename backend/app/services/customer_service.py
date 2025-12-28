"""
Customer Service
"""
from app.database.connection import SessionLocal
from app.models.customer import Customer

class CustomerService:
    def get_all(self):
        """Get all customers"""
        db = SessionLocal()
        try:
            customers = db.query(Customer).all()
            return [self._to_dict(c) for c in customers]
        finally:
            db.close()
    
    def create(self, data: dict):
        """Create customer"""
        db = SessionLocal()
        try:
            customer = Customer(**data)
            db.add(customer)
            db.commit()
            db.refresh(customer)
            return self._to_dict(customer)
        finally:
            db.close()
    
    def update(self, customer_id: int, data: dict):
        """Update customer"""
        db = SessionLocal()
        try:
            customer = db.query(Customer).filter(Customer.id == customer_id).first()
            if not customer:
                raise Exception("Customer not found")
            
            for key, value in data.items():
                setattr(customer, key, value)
            
            db.commit()
            db.refresh(customer)
            return self._to_dict(customer)
        finally:
            db.close()
    
    def delete(self, customer_id: int):
        """Delete customer"""
        db = SessionLocal()
        try:
            customer = db.query(Customer).filter(Customer.id == customer_id).first()
            if customer:
                db.delete(customer)
                db.commit()
        finally:
            db.close()
    
    def _to_dict(self, customer):
        """Convert customer to dict"""
        return {
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone,
            'address': customer.address,
            'city': customer.city,
            'state': customer.state,
            'country': customer.country,
            'gstin': customer.gstin,
            'contact_person': customer.contact_person,
            'notes': customer.notes
        }
