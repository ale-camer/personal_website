from flask import Flask
from modules.common.utils import load_language_texts, inject_texts_and_languages
from modules.whatsapp import init_dash, ChatSession
from config import WEEK_DAYS, MONTHS

def create_app():
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    app.config['SECRET_KEY'] = 'a-very-secret-and-random-string-should-go-here'

    with app.app_context():
        app.before_request(load_language_texts)
        app.context_processor(inject_texts_and_languages)

        from .routes import static_pages, keyphrase, seasonality, world_bank, whatsapp

        app.register_blueprint(static_pages.bp)
        app.register_blueprint(keyphrase.bp)
        app.register_blueprint(seasonality.bp)
        app.register_blueprint(world_bank.bp)
        app.register_blueprint(whatsapp.bp)
        
        app.dash_app = init_dash(app, whatsapp.whatsapp_service, WEEK_DAYS, MONTHS)
        
    return app