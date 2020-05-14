from flask import render_template, Blueprint
from app_config import action_cam_snap,action_cam_stream

index_bp = Blueprint("index", __name__)


@index_bp.route('/', methods=['GET'])
def home():
    return render_template("index.html")


@index_bp.route('/snapshot', methods=['GET'])
def snapshot():
    return render_template("snapshot.html",webcam_snapshot_url=action_cam_snap)


@index_bp.route('/stream', methods=['GET'])
def stream():
    return render_template("stream.html", webcam_stream_url=action_cam_stream)
