# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---

# --- Third-party ---
from flask import Blueprint, render_template

# --- Project ---
from modules.common.utils import job_duration

# =============================================================================
# CONFIGURATION
# =============================================================================
bp = Blueprint('static_pages', __name__)

# =============================================================================
# ROUTES
# =============================================================================
@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/linear_algebra')
def linear_algebra():
    return render_template('intro_to_linear_algebra_for_data_science.html')

@bp.route('/vector_norms')
def vector_norms():
    return render_template('vector_norms_applications_in_data_science.html')

@bp.route('/algorithmic_trading')
def algorithmic_trading():
    return render_template('stock_algorithmic_trading_strategy_backtesting.html')

@bp.route('/ds_trends')
def ds_trends():
    return render_template('trends_in_data_science_labour_market.html')

@bp.route('/arg_macro')
def arg_macro():
    return render_template('macro_n_employment_english.html')

@bp.route('/mi_cv')
def mi_cv():
    return render_template('mi_cv.html', delta_time_string=job_duration())

@bp.route('/keyphrase_extraction')
def keyphrase_extraction():
    return render_template('keyphrase.html')

@bp.route('/seasonality_prediction')
def seasonality_prediction():
    return render_template('seasonality.html')

@bp.route('/world_bank')
def world_bank():
    from config import INDICATORS
    return render_template('world_bank.html', indicators=INDICATORS)

@bp.route('/whatsapp')
def whatsapp():
    return render_template('whatsapp.html')