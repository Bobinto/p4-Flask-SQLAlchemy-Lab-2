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

def test_serialization(client):

    customer = Customer(name="Test Customer")
    item = Item(name="Test Item", price=10.0)
    review = Review(comment="Great item!", customer=customer, item=item)
    
    db.session.add_all([customer, item, review])
    db.session.commit()

    # Test serialization
    serialized_customer = customer.to_dict()
    assert serialized_customer['name'] == "Test Customer"
    assert 'reviews' not in serialized_customer

    serialized_item = item.to_dict()
    assert serialized_item['name'] == "Test Item"
    assert 'reviews' not in serialized_item 

    serialized_review = review.to_dict()
    assert serialized_review['comment'] == "Great item!"
    assert 'customer' not in serialized_review  
    assert 'item' not in serialized_review  
