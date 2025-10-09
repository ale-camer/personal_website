from flask import Flask
import modules.common.utils as ut
from modules.whatsapp import init_dash, ChatSession
from config import WEEK_DAYS, MONTHS

def create_app():
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    
    # IMPORTANTE: Las sesiones requieren una clave secreta.
    # Cámbiala por una cadena de caracteres aleatoria y segura.
    app.config['SECRET_KEY'] = 'a-very-secret-and-random-string-should-go-here'

    with app.app_context():
        app.before_request(ut.load_language_texts)
        app.context_processor(ut.inject_texts_and_languages)

        from .routes import static_pages, keyphrase, seasonality, world_bank, whatsapp

        app.register_blueprint(static_pages.bp)
        app.register_blueprint(keyphrase.bp)
        app.register_blueprint(seasonality.bp)
        app.register_blueprint(world_bank.bp)
        app.register_blueprint(whatsapp.bp)
        
        app.dash_app = init_dash(app, whatsapp.whatsapp_service, WEEK_DAYS, MONTHS)
        
    return app