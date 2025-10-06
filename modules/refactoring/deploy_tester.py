from deployment import Deployment
import keyphrase_pipeline as params

def get_input(func, *args, **kwargs):
    return func(*args, **kwargs)

def main():
    input_data = get_input(**params.input_params)
    params.deploy_params["input_data"] = input_data
    return Deployment(**params.deploy_params).run()

if __name__ == "__main__":
    for _ in range(3):
        results = main()