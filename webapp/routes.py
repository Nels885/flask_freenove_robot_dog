import subprocess
from datetime import datetime

from flask import render_template, jsonify, Blueprint, request, flash, Response
from constance import config, redis_get, redis_mset

main_bp = Blueprint("main", __name__)


@main_bp.route('/now/ajax/', methods=['GET'])
def now_ajax():
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return jsonify(**locals())


@main_bp.route('/')
def index():
    redis_mset(prog_status="Libre")
    card_title = "Home"
    return render_template('index.html', **locals())


@main_bp.route('/status/')
def status():
    card_title = "Operating state"
    return render_template('status.html', **locals())


@main_bp.route('/system/')
def system():
    card_title = "System"
    user = subprocess.check_output(['whoami']).decode("utf-8")
    return render_template('system.html', **locals())


@main_bp.route('/status/ajax/', methods=['GET'])
def status_ajax():
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    status = redis_get("prog_status", default="Hors ligne")
    return jsonify({'now': now, 'status': status})


@main_bp.route('/stop/')
def stop():
    context = {'status': 'busy', 'html': '<h4 class="text-center">Stop du Raspberry Pi en cours ...</h4>'}
    if redis_get("prog_status") in ["Libre", "Hors ligne"]:
        subprocess.Popen(["sudo", "shutdown", "-h", "now"])
        context['status'] = 'stop'
    else:
        context['html'] = '<h4 class="text-center">Arrêt impossible, Raspberry Pi occupé</h4>'
    return jsonify(context)


@main_bp.route('/restart/')
def restart():
    context = {'status': 'busy', 'html': '<h4 class="text-center">Restart du Raspberry Pi en cours ...</h4>'}
    if redis_get("prog_status") in ["Libre", "Hors ligne"]:
        subprocess.Popen(["sudo", "reboot"])
        context['status'] = 'reboot'
    else:
        context['html'] = '<h4 class="text-center">Restart impossible, Raspberry Pi occupé</h4>'
    return jsonify(context)


@main_bp.route('/conf/ajax/reset/', methods=["POST"])
def ajax_value_reset():
    data = request.get_json()
    key = data.get('key', "")
    print(key)
    value = config.get_default(key)
    return jsonify({'val': value})


@main_bp.route("/conf/all/", methods=["GET", "POST"])
def all():
    card_title = "Global config"
    redis_mset(prog_status="Config")
    obj = config.get_fields('GLOBAL')
    if request.method == "POST":
        print(request.form.to_dict())
        for key, value in request.form.to_dict().items():
            config.set(key, value)
        obj = config.get_fields('GLOBAL')
        flash(f"Saved {card_title} Successfully!")
    return render_template('settings.html', **locals())


@main_bp.route("/conf/network/", methods=["GET", "POST"])
def network():
    card_title = "Network config"
    redis_mset(prog_status="Config")
    obj = config.get_fields('NETWORK')
    if request.method == "POST":
        print(request.form.to_dict())
        for key, value in request.form.to_dict().items():
            config.set(key, value)
        obj = config.get_fields('NETWORK')
        flash(f"Saved {card_title} Successfully!")
    return render_template('settings.html', **locals())


@main_bp.route('/stream/')
def stream():
    card_title = "Stream"
    return render_template('stream.html', **locals())


def gen(camera):
    # get camera frame
    while True:
        # frame = camera.get_recognize_text()
        frame = camera.get_frame()
        if frame:
            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@main_bp.route('/video_feed')
def video_feed():
    from raspack.camera import pi_camera
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# Take a photo when pressing camera button
@main_bp.route('/picture')
def take_picture():
    from raspack.camera import pi_camera
    pi_camera.take_picture()
    return "None"
