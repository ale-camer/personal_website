# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import os

# --- Third-party ---

# --- Project ---

# =============================================================================
# CUSTOM EXCEPTIONS
# =============================================================================
class TooManySheetsError(Exception):
    pass

class TooManyColumnsError(Exception):
    pass

class NonNumericValueError(Exception):
    pass

class FileTooBigError(Exception):
    pass

class WhatsappFileError(Exception):
    pass     

class FileTooLargeError(Exception):
    pass

# =============================================================================
# VALIDATIONS
# =============================================================================
def validate_number_of_sheets(data):
    number_of_sheets = len(data)
    if number_of_sheets > 1:
        raise TooManySheetsError(
            (
                f"The file should only have one sheet.",
                " The file has {number_of_sheets} sheets"
            )
        )
    else:
        print("The number of sheets is OK")

def validate_number_of_columns(data):
    sheet_names = list(data.keys())
    number_of_columns = len(data[sheet_names[0]])
    if number_of_columns > 1:
        raise TooManyColumnsError(
            (
                f"The sheet '{sheet_names[0]}' has too many columns. ",
                "It has {number_of_columns} columns"
            )
        )
    else:
        print("The number of columns is OK")

def validate_data_type(data):
    if not all([s.isnumeric() for s in data]):
        raise NonNumericValueError("Not all values are numeric")
    else:
        print("The data type of the values is OK")

def validate_stream_size(stream, max_size_mb: float = 10) -> None:
    original_position = stream.tell()    
    try:
        stream.seek(0, os.SEEK_END)
        file_size_bytes = stream.tell()
    finally:
        stream.seek(original_position, os.SEEK_SET)

    file_size_mb = file_size_bytes / (1024 * 1024)
    if file_size_mb > max_size_mb:
        raise FileTooBigError(
            f"The file is too big ({file_size_mb:.2f} MB). "
            f"Max allowed is {max_size_mb} MB."
        )