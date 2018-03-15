from flask import Flask, jsonify
from flask_api import status

app = Flask(__name__)

DEFAULT_PORT = 5000


def entryPoint(controller):

    @app.route('/get/status', methods=['GET'])
    def getStatus():
        return jsonify(controller.getStatus()), status.HTTP_200_OK

    @app.route('/get/<collaborator_type>/collaborator/status', methods=['GET'])
    def getCollaboratorStatus(collaborator_type):
        pass

    @app.route('/create/<collaborator_type>/collaborator', methods=['POST'])
    def createCollaborator(collaborator_type):
        return jsonify(controller.createCollaborator(collaborator_type)),
        status.HTTP_200_OK

    @app.route('/start/<collaborator_type>/collaborator', methods=['PUT'])
    def startCollaborator(collaborator_type):
        return jsonify(controller.startCollaborator(collaborator_type)),
        status.HTTP_200_OK

    @app.route('/stop-writing/<collaborator_type>/collaborator',
               methods=['PUT'])
    def stopWritingCollaborator(collaborator_type):
        return jsonify(controller.stopWritingCollaborator(collaborator_type)),
        status.HTTP_200_OK

    @app.route('/stop-reading/<collaborator_type>/collaborator',
               methods=['PUT'])
    def stopReadingMuteCollaborator(collaborator_type):
        return jsonify(controller.stopReadingCollaborator(collaborator_type)),
        status.HTTP_200_OK

    @app.route('/retrieve/<collaborator_type>/collaborator/records',
               methods=['GET'])
    def retrieveMuteCollabRecords(collaborator_type):
        return jsonify(controller.retrieveCollabRecords(collaborator_type)),
        status.HTTP_200_OK

    config = controller.getConfig()

    if not config or 'port' not in config:
        config['port'] = DEFAULT_PORT

    app.run(port=config['port'], host='0.0.0.0')
