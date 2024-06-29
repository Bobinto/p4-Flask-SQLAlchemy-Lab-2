import pytest
from server.app import app
from server.models import db, Customer, Item, Review

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_association_proxy(client):
    # Create a customer, item, and review
    customer = Customer(name="Test Customer")
    item = Item(name="Test Item", price=10.0)
    review = Review(comment="Great item!", customer=customer, item=item)
    
    db.session.add_all([customer, item, review])
    db.session.commit()

    # Verify association proxy
    assert len(customer.items) == 1
    assert customer.items[0].name == "Test Item"
