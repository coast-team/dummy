from flask import Flask, jsonify
from flask_api import status
from collaborator.controller import Controller
import netifaces as ni

app = Flask(__name__)

DEFAULT_PORT = 5000


def entryPoint(path_to_config):

    @app.route('/get/status', methods=['GET'])
    def getStatus():
        return jsonify(controller.getStatus()), status.HTTP_200_OK

    @app.route('/get/mute/collaborator/status', methods=['GET'])
    def getMuteCollaboratorStatus():
        pass

    @app.route('/create/mute/collaborator', methods=['POST'])
    def createMuteCollaborator():
        return jsonify(controller.createMuteCollaborator()), status.HTTP_200_OK

    @app.route('/start/mute/collaborator', methods=['PUT'])
    def startMuteCollaborator():
        return jsonify(controller.startMuteCollaborator()), status.HTTP_200_OK

    @app.route('/stop-writing/mute/collaborator', methods=['PUT'])
    def stopWritingMuteCollaborator():
        return jsonify(controller.stopWritingMuteCollaborator())

    @app.route('/stop-reading/mute/collaborator', methods=['PUT'])
    def stopReadingMuteCollaborator():
        return jsonify(controller.stopReadingMuteCollaborator())

    @app.route('/retrieve/mute/collaborator/records', methods=['GET'])
    def retrieveMuteCollabRecords():
        return jsonify({'status': 'Not yet implemented'})

    controller = Controller(path_to_config)
    config = controller.getConfig()

    if not config or 'port' not in config:
        config['port'] = DEFAULT_PORT

    if 'address' not in config:
        # Get the right interface
        gws = ni.gateways()
        interface = gws['default'][2][1]

        ni.ifaddresses(interface)
        ip_addr = ni.ifaddresses(interface)[2][0]['addr']
        config['address'] = ip_addr

    app.run(port=config['port'], host=config['address'])
