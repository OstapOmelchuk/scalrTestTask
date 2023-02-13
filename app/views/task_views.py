from flask import Blueprint, request, make_response
from flask.views import MethodView
from ..database import Task
import os

mod = Blueprint('task', __name__)


class TaskView(MethodView):
    def get(self, **kwargs):
        tasks = Task.select()

        if kwargs.get("id"):
            task = TaskView.getTaskIfExist(kwargs.get("id"))

            if not task:
                return make_response({"error": "The task with the specified ID does not exist"}, 400)
            tasks = [task]

        """List all tasks.py."""
        return make_response({
            "data": [task.to_response(request.base_url) for task in tasks]
        }, 200)

    def post(self):
        """Create the new docker task"""
        if "data" not in request.json:
            return make_response({"error": "data is required"}, 400)

        if "attributes" not in request.json["data"]:
            return make_response({"error": "data.attributes is required"}, 400)

        if "title" not in request.json["data"]["attributes"]:
            return make_response({"error": "data.attributes.title is required"}, 400)

        task = Task.create(
            title=request.json["data"]["attributes"]["title"],
            command=request.json["data"]["attributes"]["command"],
            image=request.json["data"]["attributes"]["image"],
            description=request.json["data"]["attributes"]["description"],
        )
        runTask(task.id)
        return make_response({"data": task.to_response(request.base_url)}, 201)

    def delete(self, **kwargs):
        task = TaskView.getTaskIfExist(kwargs.get("id"))
        if not task:
            return make_response({"error": "The task with the specified ID does not exist"}, 400)

        print(task.status)
        if task.status in ["finished", "failed"]:
            task.delete_instance()
            return make_response({"success": "task is deleted"}, 204)
        else:
            return make_response({"task can not be deleted while it is running or pending"}, 400)

    def patch(self, **kwargs):
        task = TaskView.getTaskIfExist(kwargs.get("id"))
        if not task:
            return make_response({"error": "The task with the specified ID does not exist"}, 400)

        data_to_update = request.json
        if not data_to_update:
            return make_response({"error": "no data to update"}, 400)

        title, command, description = data_to_update["title"], data_to_update["command"], data_to_update["description"]

        if isinstance(title, str):
            task.title = title
        if isinstance(command, str):
            task.command = command
        if isinstance(description, str):
            task.description = description

        try:
            task.save()
            return make_response({"data": Task.get(id=kwargs.get("id")).to_response(request.base_url)}, 200)
        except Exception as ex:
            print(ex, data_to_update)
            return make_response("An error occurred during updating. Check if the entered data is correct:"
                                 " (title: <str>, command: <str>, description: <str>)", 400)

    @classmethod
    def getTaskIfExist(task_id):
        try:
            task = Task.get(id=task_id)
            return task
        except Exception as e:
            return False


def runTask(task_id):
    os.mkdir("../../dockerDir")
    pass


class TaskLogView(MethodView):
    def get(self, **kwargs):
        if kwargs.get("id"):
            task = TaskView.getTaskIfExist(kwargs.get("id"))

            if not task:
                return make_response({"error": "The task with the specified ID does not exist"}, 400)

            response = make_response("LOG", 200)
            response.mimetype = "text/plain"
            return response

        return make_response({"Enter the ID of a task"}, 400)


task_view = TaskView.as_view('task')
mod.add_url_rule('/', view_func=task_view, methods=['GET', 'POST'])
mod.add_url_rule('/<id>', view_func=task_view, methods=['GET', 'DELETE', 'PATCH'])

task_log_view = TaskLogView.as_view('tasklog')
mod.add_url_rule('/<id>/logs', view_func=task_log_view, methods=['GET'])
