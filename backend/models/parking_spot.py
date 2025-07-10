from app import db

class ParkingSpot(db.Model):
    __tablename__ = 'parking_spots'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(1), default='A') # A - Available, O - Occupied
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    reservations = db.relationship('Reservation', backref='spot', lazy=True)
