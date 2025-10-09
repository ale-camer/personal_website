# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
from functools import wraps

# --- Third-party ---
from flask import request, render_template

# --- Project ---
from .validations import validate_stream_size, FileTooBigError

# =============================================================================
# DECORATORS
# =============================================================================
def validate_file_size(
        template_on_error: str, file_key: str = 'file', max_size_mb: float = 20
    ):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            uploaded_file = request.files.get(file_key)
            try:
                validate_stream_size(uploaded_file, max_size_mb=max_size_mb)
                # uploaded_file.seek(0)
                print("The file size is OK")
                return f(uploaded_file=uploaded_file, *args, **kwargs)
            except FileTooBigError as e:
                print("Error:", e)
                return render_template(template_on_error, error=str(e))
        return wrapper
    return decorator