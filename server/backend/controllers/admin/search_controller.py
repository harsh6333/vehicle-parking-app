from backend.models.parking_lot import ParkingLot
from backend.models.parking_spot import ParkingSpot
from backend.models.user import User
from flask import jsonify
from sqlalchemy import or_, func
from backend.extensions import db

class SearchController:
    def search_lots(self, query, page, per_page, sort_by, sort_order):
        if not query:
            return jsonify({"msg": "Query is required"}), 400

        sort_column = getattr(ParkingLot, sort_by, ParkingLot.prime_location_name)
        sort_column = sort_column.desc() if sort_order == "desc" else sort_column.asc()

        lots_query = ParkingLot.query.filter(
            or_(
                func.lower(ParkingLot.prime_location_name).like(f"%{query.lower()}%"),
                ParkingLot.pin_code.like(f"%{query}%")
            )
        ).order_by(sort_column)

        paginated = lots_query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            "results": [
                {
                    "id": lot.id,
                    "prime_location_name": lot.prime_location_name,
                    "pin_code": lot.pin_code,
                    "price": float(lot.price),
                    "total_spots": lot.number_of_spots
                } for lot in paginated.items
            ],
            "total": paginated.total,
            "page": paginated.page,
            "pages": paginated.pages
        }), 200

    def search_spots(self, status, lot_id=None):
        if status not in ["available", "occupied"]:
            return jsonify({"msg": "Invalid status. Use 'available' or 'occupied'."}), 400

        query = ParkingSpot.query
        if lot_id:
            query = query.filter_by(lot_id=lot_id)

        spots = query.all()
        filtered_spots = []

        for spot in spots:
            is_occupied = any(
                r.parking_timestamp and not r.leaving_timestamp for r in spot.reservations
            )

            if (status == "occupied" and is_occupied) or (status == "available" and not is_occupied):
                filtered_spots.append({
                    "id": spot.id,
                    "lot_id": spot.lot_id,
                    "location": spot.lot.prime_location_name if spot.lot else "Unknown",
                    "status": "occupied" if is_occupied else "available"
                })

        return jsonify(filtered_spots), 200


    def search_users(self, query, page, per_page):
        if not query:
            return jsonify({"msg": "Query is required"}), 400

        users_query = User.query.filter(
            or_(
                func.lower(User.username).like(f"%{query.lower()}%"),
                func.lower(User.email).like(f"%{query.lower()}%")
            )
        ).order_by(User.username.asc())

        paginated = users_query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            "results": [
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_admin": user.is_admin
                } for user in paginated.items
            ],
            "total": paginated.total,
            "page": paginated.page,
            "pages": paginated.pages
        }), 200
