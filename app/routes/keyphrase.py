# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---

# --- Third-party ---
from flask import Blueprint, request, render_template, jsonify, make_response

# --- Project ---
from modules.common.decorators import validate_file_size
from modules.common.utils import FileExporter, write_json
from modules.keyphrase import pipeline, read_kp_results
from config import KEYPHRASE_INPUT_PATH

# =============================================================================
# CONFIGURATION
# =============================================================================
bp = Blueprint('keyphrase', __name__)
progress = {"value": 0}

# =============================================================================
# ROUTES
# =============================================================================
@bp.route('/extract_keyphrases', methods=['GET', 'POST'])
@validate_file_size(template_on_error='keyphrase.html')
def extract_keyphrases(uploaded_file):
    
    try:
        results = pipeline(
            raw_text=uploaded_file.read().decode('utf-8'),
            progress=progress,
            top_k=int(request.form.get('num_rows', 1)),
            max_n=int(request.form.get('num_tables', 1))
        )
        summary = {
            label: [{"Keywords": d[0], "# Appearances": d[1]} for d in data]
            for label, data in results.items()
        }
        write_json(summary, KEYPHRASE_INPUT_PATH)
        return render_template('keyphrase.html', results=results)
    except Exception as e:
        return render_template('keyphrase.html', execution_exception=str(e))

@bp.route('/progress')
def get_progress():
    return jsonify(progress)

@bp.route('/download_keyphrases', methods=['GET'])
def download_keyphrases():
    print("AAAAAAAAAAAAAAAAAAAA")
    results_data = read_kp_results(KEYPHRASE_INPUT_PATH)
    exporter = FileExporter(results_data, cols=["Keywords", "# Appearances"])

    file_format = request.args.get('format', 'txt')
    match file_format:
        case 'txt': output_content = exporter.to_txt_string()
        case 'md': output_content = exporter.to_md_string()
        case 'pdf': output_content = exporter.to_pdf_bytes()

    type_str = f"application/{file_format}" if file_format == 'pdf' else f"text/{file_format}"
    disp_str = f'attachment; filename={f"keyphrase_results.{file_format}"}'
    response = make_response(output_content)
    response.headers['Content-Type'] = type_str
    response.headers['Content-Disposition'] = disp_str
    return response