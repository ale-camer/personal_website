from functools import wraps
from flask import request, render_template
from .validations import validate_stream_size, FileTooBigError

def validate_file_size(template_on_error: str, file_key: str = 'file', max_size_mb: float = 10):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            uploaded_file = request.files.get(file_key)
            try:
                validate_stream_size(uploaded_file, max_size_mb=max_size_mb)
                return f(uploaded_file=uploaded_file, *args, **kwargs)
            except FileTooBigError as e:
                return render_template(template_on_error, error=str(e))
        return wrapper
    return decorator