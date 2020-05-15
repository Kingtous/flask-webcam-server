from flask import render_template, Blueprint
from app_config import action_cam_snap, action_cam_stream, auth

index_bp = Blueprint("index", __name__)


@index_bp.route('/', methods=['GET'])
@auth.login_required
def home():
    return render_template("index.html")


@index_bp.route('/snapshot', methods=['GET'])
@auth.login_required
def snapshot():
    return render_template("snapshot.html", webcam_snapshot_url=action_cam_snap)


@index_bp.route('/stream', methods=['GET'])
@auth.login_required
def stream():
    return render_template("stream.html", webcam_stream_url=action_cam_stream)
