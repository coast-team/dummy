from flask import Flask, jsonify
from flask_api import status

app = Flask(__name__)

DEFAULT_PORT = 5000


def entryPoint(controller):

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
        return jsonify(controller.stopWritingMuteCollaborator()),
        status.HTTP_200_OK

    @app.route('/stop-reading/mute/collaborator', methods=['PUT'])
    def stopReadingMuteCollaborator():
        return jsonify(controller.stopReadingMuteCollaborator()),
        status.HTTP_200_OK

    @app.route('/retrieve/mute/collaborator/records', methods=['GET'])
    def retrieveMuteCollabRecords():
        return jsonify(controller.retrieveMuteCollabRecords()),
        status.HTTP_200_OK

    config = controller.getConfig()

    if not config or 'port' not in config:
        config['port'] = DEFAULT_PORT

    app.run(port=config['port'], host='0.0.0.0')
