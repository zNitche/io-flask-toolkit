from flask import Blueprint, Response


core_blueprint = Blueprint("core", __name__, template_folder="templates",
                 static_folder="static", url_prefix="/")


@core_blueprint.route("", methods=["GEt"])
def root():
    return Response(status=200)
