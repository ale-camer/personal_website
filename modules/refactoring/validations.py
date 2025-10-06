import os

class TooManySheetsError(Exception):
    pass

def validate_number_of_sheets(data):
    number_of_sheets = len(data)
    if number_of_sheets > 1:
        raise TooManySheetsError(
            f"The file should only have one sheet. The file has {number_of_sheets} sheets"
        )
    else:
        print("The number of sheets is OK")


class TooManyColumnsError(Exception):
    pass

def validate_number_of_columns(data):
    sheet_names = list(data.keys())
    number_of_columns = len(data[sheet_names[0]])
    if number_of_columns > 1:
        raise TooManyColumnsError(
            f"The sheet '{sheet_names[0]}' has too many columns. It has {number_of_columns} columns"
        )
    else:
        print("The number of columns is OK")

class NonNumericValueError(Exception):
    pass

def validate_data_type(data):
    if not all([s.isnumeric() for s in data]):
        raise NonNumericValueError("Not all values are numeric")
    else:
        print("The data type of the values is OK")

class FileTooBig(Exception):
    pass

def validate_file_size(filename: str, max_size_mb: float = 10):
    file_size_mb = os.path.getsize(filename) / (1024 * 1024)
    if file_size_mb > max_size_mb:
        raise FileTooBig(f"The file can't be bigger than {max_size_mb} MB")
    else:
        print("File size is OK")
