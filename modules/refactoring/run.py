from keyphrase_pipeline import input_params, pipeline
import validations as val
from utils import get_input, FileExporter

val.validate_file_size(input_params["filename"])
input_file = get_input(**input_params)
results = pipeline(input_file)

exporter = FileExporter(results, ["N Gram", "Count"], "keyphrases")
exporter.export_txt()
exporter.export_md()
exporter.export_pdf()
