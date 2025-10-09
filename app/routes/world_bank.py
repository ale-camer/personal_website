# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import os

# --- Third-party ---
from flask import Blueprint, request, jsonify, url_for

# --- Project ---
import modules.world_bank as wb
import modules.common.utils as ut
from config import WORLD_BANK_DIR, INDICATOR_NAMES, GEO_DATA_PATH

# =============================================================================
# CONFIGURATION
# =============================================================================
bp = Blueprint('world_bank', __name__)

# =============================================================================
# HELPERS
# =============================================================================
def get_params():
    return (
        request.args.get('indicator') or request.form.get('indicator') or None,
        request.args.get('type') or request.form.get('type') or None,
        request.args.get('option') or request.form.get('option') or None
    )

def get_downloaded_data(indicator):
    return ut.read_json(os.path.join(WORLD_BANK_DIR, f'{indicator}.json'))

def get_filtered_data(data, _type, option):
    return wb.filter_data(data, _type, option)

# =============================================================================
# ROUTES
# =============================================================================
@bp.route('/download_data')
def download_data():
    indicator = get_params()[0]
    data = wb.download_data(indicator)
    ut.write_json(data, os.path.join(WORLD_BANK_DIR, f'{indicator}.json'))
    return jsonify({'message': 'Data saved successfully'})

@bp.route('/show_options')
def show_options():
    indicator, _type, _ = get_params()
    data = get_downloaded_data(indicator)
    options = wb.get_options(data, _type)
    return jsonify(options)

@bp.route('/show_data')
def show_data():
    indicator, _type, option = get_params()
    data = get_downloaded_data(indicator)
    filtered_data = get_filtered_data(data, _type, option)
    return jsonify(filtered_data)

@bp.route('/plot_graph', methods=['POST'])
def plot_graph():
    indicator, _type, option = get_params()
    data = get_downloaded_data(indicator)
    filtered_data = get_filtered_data(data, _type, option)

    title = f'{INDICATOR_NAMES.get(indicator)} - {option}'
    relative_path = wb.plot(filtered_data, _type, GEO_DATA_PATH, title=title)
    plot_url = url_for('static', filename=f'world_bank/{relative_path}')
    return jsonify(
        {'message': 'Interactive graph generated.', 'plot_url': plot_url}
    )