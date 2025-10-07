from deployment import Deployment
import world_bank_pipeline as params
from utils import get_input

def main():
    params.tester_params["input_data"] = get_input(**params.input_params)
    return Deployment(**params.tester_params).run()

if __name__ == "__main__":
    for _ in range(3):
        results = main()