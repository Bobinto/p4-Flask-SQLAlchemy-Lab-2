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

def test_review(client):
    # Create a customer, item, and review
    customer = Customer(name="Test Customer")
    item = Item(name="Test Item", price=10.0)
    review = Review(comment="Great item!", customer=customer, item=item)
    
    db.session.add_all([customer, item, review])
    db.session.commit()

    # Verify review
    saved_review = Review.query.first()
    assert saved_review.comment == "Great item!"
    assert saved_review.customer.name == "Test Customer"
    assert saved_review.item.name == "Test Item"
