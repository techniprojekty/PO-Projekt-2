from flask import jsonify, request, abort


def register_routes(app, service):
    @app.route("/users", methods=["GET"])
    def list_users():
        return jsonify(service.list_users()), 200

    @app.route("/users/<int:user_id>", methods=["GET"])
    def get_user(user_id):
        user = service.get_user(user_id)
        if user is None:
            abort(404)
        return jsonify(user), 200

    @app.route("/users", methods=["POST"])
    def create_user():
        if not request.is_json:
            abort(400)
        data = request.get_json()
        try:
            user = service.create_user(data)
            return jsonify(user), 201
        except ValueError as e:
            abort(400, description=str(e))

    @app.route("/users/<int:user_id>", methods=["PATCH"])
    def update_user(user_id):
        if not request.is_json:
            abort(400)
        data = request.get_json()
        try:
            updated = service.update_user(user_id, data)
            if updated is None:
                abort(404)
            return jsonify(updated), 200
        except ValueError as e:
            abort(400, description=str(e))

    @app.route("/users/<int:user_id>", methods=["DELETE"])
    def delete_user(user_id):
        deleted = service.delete_user(user_id)
        if not deleted:
            abort(404)
        return "", 204
