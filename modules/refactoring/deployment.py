# standard
import time, tracemalloc, asyncio, threading, os
from tqdm import tqdm
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# external
from prettytable import PrettyTable as pt
import matplotlib.pyplot as plt
import seaborn as sns

# internal
from utils import get_chunks

def running_records(func: callable, inputs: list) -> dict:

    tracemalloc.start()

    start_time_total = time.perf_counter()
    start_time_cpu = time.process_time()

    tracemalloc.clear_traces()

    _ = func(inputs)

    end_time_total = time.perf_counter()
    end_time_cpu = time.process_time()

    _, mem_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "tamaño_de_la_muestra": f'{len(inputs):,}',
        "tiempo_total_seg": round(end_time_total - start_time_total, 4),
        "tiempo_cpu_seg": end_time_cpu - start_time_cpu,
        "pico_memoria_mb": round(mem_peak / 1024 / 1024, 4),
    }

def get_results(
        parent_func, child_func, inputs, top_factor: int = 5,
        start: int = 1, step: int = 1
    ) -> dict[str, int | float]:
    return {
        f"Multiplier {mult}": parent_func(
            lambda x: child_func(x), inputs * mult
        ) for mult in tqdm(range(start, top_factor + 1, step))
    }

def create_table(
        data: dict[str, int | float], title: str = 'Metrics',
        columns: list[str] = None, has_custom_columns: bool = False
    ) -> pt:

    def create_columns(data: dict) -> list:
        return [list(data.keys())[0].split(" ")[0]] + \
            list(data[list(data.keys())[0]].keys())

    if has_custom_columns: cols = columns
    else: cols = create_columns(data)

    table = pt()
    table.title = title
    table.field_names = cols
    for k, v in data.items():
        table.add_rows([[k.split(" ")[1]] + list(v.values())])
    return table

def get_generic_output(results):

    def merge_pair(func):
        def wrapper(results, combined):
            for res in results:
                for key, val in res.items():
                    func(key, val, combined)
            return combined
        return wrapper

    @merge_pair
    def merge_single(key, val, combined):
        match val:
            case Counter():
                combined[key].update(val)
            case list():
                combined[key].update(dict(val))
            case _:
                if not isinstance(combined[key], list):
                    combined[key] = []
                combined[key].extend(val)

    return dict(merge_single(results, defaultdict(Counter)))

class PipelineExecutor:

    def __init__(self, worker, combine_fn):
        self.worker = worker
        self.combine_fn = combine_fn

    def _execute_template(self, executor_class, text, desc, **executor_kwargs):

        chunks = list(get_chunks(text))
        with executor_class(**executor_kwargs) as executor:
            partial_results = list(
                tqdm(executor.map(self.worker, chunks), total=len(chunks), desc=desc)
            )
        return self.combine_fn(partial_results)

    def multiprocessing(self, text: str) -> dict:
        return self._execute_template(
            ProcessPoolExecutor, text, "Multiprocessing", max_workers=os.cpu_count()
        )

    def threading(self, text: str, num_threads: int = 10) -> dict:
        return self._execute_template(
            ThreadPoolExecutor, text, "Threading", max_workers=num_threads
        )

    async def _async_main(self, text: str):

        chunks = list(get_chunks(text))
        tasks = [self._async_wrapper(f) for f in chunks]
        partial_results = await asyncio.gather(*tasks)
        return self.combine_fn(partial_results)

    async def _async_wrapper(self, fragmento: str):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self.worker, fragmento)

    def asynchronic(self, text: str) -> dict:
        resultado = {}
        def run_in_thread():
            nonlocal resultado
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                resultado = loop.run_until_complete(self._async_main(text))
            finally:
                loop.close()

        thread = threading.Thread(target=run_in_thread)
        thread.start()
        thread.join()
        return resultado

def plot_data_wrapper(func):
    def wrapper(results):
        processed = get_data_to_plot(results)
        return func(processed)
    return wrapper

def get_data_to_plot(results_list):
    all_rows = []
    for strategy_name, result_dict in results_list:
        for key, values in result_dict.items():
            multiplier_num = int(key.split(" ")[1])
            row = {"Strategy": strategy_name, "Multiplier": multiplier_num}
            for k, v in values.items():
                if isinstance(v, str) and v.replace(",", "").isdigit():
                    values[k] = int(v.replace(",", ""))
            row.update(values)
            all_rows.append(row)
    return all_rows

@plot_data_wrapper
def plot_comparative_series(rows):

    def get_dict_of_columns(rows):
        return {k: [row[k] for row in rows] for k in rows[0].keys()}

    def format_axis(ax, config):
        ax.set_title(config["title"], fontsize=18, weight="bold")
        ax.set_ylabel(config["ylabel"], fontsize=12)
        if "xlabel" in config and config["xlabel"]:
            ax.set_xlabel(config["xlabel"], fontsize=12)
        ax.legend(title="Strategy", fontsize=10, title_fontsize=11)
        ax.tick_params(axis="x", rotation=45)

    configs = [
        {
            "y": "tiempo_total_seg",
            "title": "Execution Time Comparison (Mean and Variability)",
            "ylabel": "Total Execution Time (seconds)",
            "xlabel": "Sample Multiplier",
        },
        {
            "y": "pico_memoria_mb",
            "title": "Memory Peak Usage (Mean and Variability)",
            "ylabel": "Peak Memory Used (MB)",
            "xlabel": "Sample Multiplier",
        }
    ]

    lineplot_kwargs = {
        "data": get_dict_of_columns(rows),
        "x": "Multiplier",
        "hue": "Strategy",
        "style": "Strategy",
        "markers": True,
        "dashes": False,
        "linewidth": 2.5,
        "markersize": 8
    }

    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(2, 1, figsize=(10, 10))
    for cfg, ax in zip(configs, axes):
        cfg["ax"] = ax

    for cfg in configs:
        sns.lineplot(y=cfg["y"], ax=cfg["ax"], **lineplot_kwargs)
        format_axis(cfg["ax"], cfg)

    plt.tight_layout()
    plt.show()

class Deployment:

    def __init__(self, input_data, worker: callable, combine_fn: callable):
        self.input_data = input_data
        self.executor = PipelineExecutor(worker, combine_fn)
        self.config = {
            'parent_func': running_records, 'inputs': self.input_data,
            'start': 1, 'top_factor': 30, 'step': 3
        }

    def run(self) -> dict:

        runs = {
            'Secuential': self.executor.worker,
            'Threading': self.executor.threading,
            'Asyncio': self.executor.asynchronic,
            'Multiprocessing': self.executor.multiprocessing
        }

        self.results = [
            (k, get_results(child_func=v, **self.config))
            for k, v in runs.items()
        ]

        plot_comparative_series(self.results)
        return self.results