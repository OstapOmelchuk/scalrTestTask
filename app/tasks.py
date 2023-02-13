import flask


from . import database


# blueprint = flask.Blueprint("tasks", __name__)
#
#
# @blueprint.route('/tasks', methods=['GET'])
# def get_tasks():
#     print(flask.request)
#     """List all tasks.py."""
#     tasks = database.Task.select()
#     return flask.jsonify({
#         "data": [task.to_response(flask.request.base_url) for task in tasks]
#     })
#
#
# @blueprint.route('/tasks', methods=['POST'])
# def create_task():
#     """Create the new docker task"""
#     if "data" not in flask.request.json:
#         return flask.jsonify({"error": "data is required"}), 400
#
#     if "attributes" not in flask.request.json["data"]:
#         return flask.jsonify({"error": "data.attributes is required"}), 400
#
#     if "title" not in flask.request.json["data"]["attributes"]:
#         return flask.jsonify({"error": "data.attributes.title is required"}), 400
#
#     task = database.Task.create(
#         title=flask.request.json["data"]["attributes"]["title"],
#         command=flask.request.json["data"]["attributes"]["command"],
#         image=flask.request.json["data"]["attributes"]["image"],
#         description=flask.request.json["data"]["attributes"]["description"],
#     )
#
#     return flask.jsonify({"data": task.to_response(flask.request.base_url)}), 201
#
