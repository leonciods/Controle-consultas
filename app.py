import os
from flask import Flask
from flask_cors import CORS
from controllers.consulta_controller import consulta_controller
from controllers.receita_controller import receita_controller


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(consulta_controller)
    app.register_blueprint(receita_controller)
    return app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app = create_app()
    app.run(host='0.0.0.0', port=port, debug=True)
