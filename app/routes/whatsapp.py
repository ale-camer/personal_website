# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---

# --- Third-party ---
from flask import Blueprint, request, redirect, current_app

# --- Project ---
import modules.whatsapp as wp
from modules.common.decorators import validate_file_size

# =============================================================================
# CONFIGURATION
# =============================================================================
bp = Blueprint('whatsapp', __name__)
whatsapp_service = wp.ChatSession()

# =============================================================================
# ROUTES
# =============================================================================
@bp.route('/whatsapp_dashboard', methods=['POST'])
@validate_file_size(template_on_error='whatsapp.html')
def whatsapp_dashboard(uploaded_file):
    
    data = whatsapp_service.parse_chat(
        uploaded_file,
        request.form.get('selected_language')
    )
    
    issuers = sorted(list(set(d[2] for d in data.parsed_data)))
    dash_app = current_app.dash_app
    dash_app.layout = wp.layout(issuers)
    
    return redirect('/dashboard/')