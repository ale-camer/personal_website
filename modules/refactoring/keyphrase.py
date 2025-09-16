r"""
results = Ngrams(data).run()

whatsapp_pattern = r'(\d{1,2}/\d{1,2}/\d{4}, \d{2}:\d{2} .*?)(?=\d{1,2}/\d{1,2}/\d{4}, \d{2}:\d{2}|$)'
whatsapp_chunk = re.findall(whatsapp_pattern, clean_chunk)
print(whatsapp_chunk)
"""

"""
tareas:

    1. agregar plots
    2. separar logica
    3. armar politica
"""
#%%

import re, string, itertools, time, tracemalloc
from tqdm import tqdm
from unidecode import unidecode
from collections import deque, Counter, defaultdict

from prettytable import PrettyTable as pt

def read_txt(filename, encoding: str = "utf-8") -> str:
    with open(filename, encoding=encoding) as f:
        return f.read()

def get_chunks(iterable: iter, size: int = 100_000, start: int = 0) -> iter:
    if not hasattr(iterable, "__iter__") or not hasattr(iterable, "__len__"):
        raise TypeError("The 'iterable' input must be an iterable with length like a list or string")
    if len(iterable) == 0:
        raise ValueError("The 'iterable' input must have a length greater than zero")
    if not isinstance(size, int) or size <= 0:
        raise ValueError("The 'size' input must be a positive integer")

    for i in range(start, len(iterable), size):
        yield iterable[i : i + size]

class TextCleaner:

    _PUNCTUATION_PATTERN = f"[{re.escape(string.punctuation)}]"
    _NUMBERS_PATTERN = r"\d+"

    def __init__(self, text: str, stopwords: set[str] = None):
        self.text = text
        self.stopwords = stopwords if stopwords is not None else set()

    def get_stopwords():
        pass

    def clean(
        self,
        has_stream: bool = True,
        to_lowercase: bool = True,
        remove_accents: bool = True,
        remove_punctuation: bool = False,
        remove_numbers: bool = False,
        filter_stopwords: bool = True,
        min_token_length: int = 3
    ) -> list[str]:

        text = self.text
        if to_lowercase: text = text.lower()
        if remove_accents: text = unidecode(text)
        if remove_punctuation: text = re.sub(self._PUNCTUATION_PATTERN, ' ', text)
        if remove_numbers: text = re.sub(self._NUMBERS_PATTERN, ' ', text)

        if has_stream:
            yield from (
                token for token in text.split()
                if len(token) > min_token_length
                and not (filter_stopwords and token in self.stopwords)
            )
        else:
            return [
                token for token in text.split()
                if len(token) > min_token_length
                and not (filter_stopwords and token in self.stopwords)
            ]

def get_top_ngrams(
        tokens_iterator: list[str],
        has_stream: bool = True,
        top_k: int = 3,
        max_n: int = 3
    ) -> dict:

    def ngram_generator(tokens):
        for token in tokens:
            window.append(token)
            if len(window) == n:
                yield tuple(window)

    if has_stream:
        results = {}
        for n in range(1, max_n + 1):
            window = deque(maxlen=n)
            current_tokens_iterator, tokens_iterator = itertools.tee(tokens_iterator)
            ngram_counts = Counter(ngram_generator(current_tokens_iterator))
            results[f"N-Gram Value: {n}"] = ngram_counts.most_common(top_k)

        return results

    else:
        return {
            f"N-Gram Value: {n}": Counter(
                tuple(tokens_iterator[i:i+n])
                for i in range(len(tokens_iterator)-n+1)
            ).most_common(top_k)
            for n in range(1, max_n + 1)
        }

def running_records(func: callable, inputs: list) -> dict:

    tracemalloc.start() # inicio de seguimiento de memoria

    start_time_total = time.perf_counter() # Mide tiempo real
    start_time_cpu = time.process_time()   # Mide tiempo de CPU

    tracemalloc.clear_traces() # limpiar memoria

    _ = func(inputs) # ejecutando funcion

    end_time_total = time.perf_counter() # Registrar tiempos de finalización
    end_time_cpu = time.process_time()

    _, mem_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop() # Detener el seguimiento

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

# data = read_txt("whatsapp_chat.txt")
# inputs = {
#     'parent_func':running_records,
#     'child_func':lambda x: get_top_ngrams(TextCleaner(x).clean()),
#     'inputs':data,
#     'top_factor':10
# }
# print(create_table(*(get_results(**inputs), '')))

#%%

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import asyncio, threading as th, os

def keyphrase_pipeline(data: str) -> dict:
    cleaned_data = TextCleaner(data).clean()
    return get_top_ngrams(cleaned_data)

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

def get_ngrams_output(results, top_k=3):
    return {
        key: counter.most_common(top_k)
        for key, counter in get_generic_output(results).items()
    }

class PipelineExecutor:
    def __init__(self, worker, combine_fn, fragment_size=100_000):
        self.worker = worker
        self.combine_fn = combine_fn
        self.fragment_size = fragment_size

    def _execute_template(self, executor_class, text, desc, **executor_kwargs):

        fragmentos = list(get_chunks(text, size=self.fragment_size))
        with executor_class(**executor_kwargs) as executor:
            partial_results = list(
                tqdm(executor.map(self.worker, fragmentos), total=len(fragmentos), desc=desc)
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

        fragmentos = list(get_chunks(text, size=self.fragment_size))
        tasks = [self._async_wrapper(f) for f in fragmentos]
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

        thread = th.Thread(target=run_in_thread)
        thread.start()
        thread.join()
        return resultado

def main():

    data = read_txt("whatsapp_chat.txt")

    config = {
        'parent_func': running_records,
        'inputs': data,
        'start': 1,
        'top_factor': 10,
        'step': 5
    }

    executor = PipelineExecutor(
        worker=keyphrase_pipeline,
        combine_fn=get_ngrams_output
    )

    runs = {
        'Secuential': keyphrase_pipeline,
        'Threading': executor.threading,
        'Asyncio': executor.asynchronic,
        'Multiprocessing': executor.multiprocessing
    }

    return [(k, get_results(child_func=v, **config)) for k, v in runs.items()]

if __name__ == '__main__':
    results = main()

#%%

r"""
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # (Asegúrate de tener aquí la función 'preparar_dataframe' de la respuesta anterior)
# def preparar_dataframe(lista_de_resultados: list[tuple[str, dict]]) -> pd.DataFrame:
#     all_rows = []
#     for nombre_estrategia, dict_resultados in lista_de_resultados:
#         for key, values in dict_resultados.items():
#             multiplier_num = int(key.split(" ")[1])
#             row = {'Estrategia': nombre_estrategia, 'Multiplier': multiplier_num}
#             row.update(values)
#             all_rows.append(row)
#     df = pd.DataFrame(all_rows)
#     if 'tamaño_de_la_muestra' in df.columns:
#         df['tamaño_de_la_muestra'] = df['tamaño_de_la_muestra'].str.replace(',', '').astype(int)
#     return df

# def graficar_series_comparativas(df: pd.DataFrame):

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 14), sharex=True)
    sns.set_theme(style="whitegrid")

    # --- Gráfico 1: Tiempo de Ejecución Total ---
    sns.lineplot(
        data=df,
        x="Multiplier",
        y="tiempo_total_seg",
        hue="Estrategia",
        style="Estrategia",
        markers=True,
        dashes=False,
        linewidth=2.5,
        markersize=8,
        ax=ax1
    )
    ax1.set_title('Comparativa de Tiempo de Ejecución (Media y Variabilidad)', fontsize=18, weight='bold')
    ax1.set_ylabel('Tiempo Total de Ejecución (segundos)', fontsize=12)
    ax1.legend(title='Estrategia')

    # --- Gráfico 2: Pico de Memoria ---
    sns.lineplot(
        data=df,
        x="Multiplier",
        y="pico_memoria_mb",
        hue="Estrategia",
        style="Estrategia",
        markers=True,
        dashes=False,
        linewidth=2.5,
        markersize=8,
        ax=ax2
    )
    ax2.set_title('Comparativa de Uso de Memoria (Media y Variabilidad)', fontsize=18, weight='bold')
    ax2.set_xlabel('Multiplicador de Muestra (Tamaño)', fontsize=12)
    ax2.set_ylabel('Pico de Memoria Utilizada (MB)', fontsize=12)
    ax2.legend(title='Estrategia')

    plt.xticks(df['Multiplier'].unique())
    plt.tight_layout()
    plt.show()

# if __name__ == '__main__':

#     NUM_EJECUCIONES = 5
#     top_factor = 15
#     data = read_txt("whatsapp_chat.txt")
#     todos_los_resultados = []

#     for i in range(NUM_EJECUCIONES):
#         print(f"\n{'='*20} INICIANDO EJECUCIÓN {i+1}/{NUM_EJECUCIONES} {'='*20}\n")

#         # --- Recolección de datos (sin cambios) ---
#         print(f"--- [Run {i+1}] MIDIENDO SECUENCIAL ORIGINAL ---")
#         inputs_original = {'parent_func': running_records, 'child_func': lambda x: get_top_ngrams(TextCleaner(x).clean()), 'inputs': data, 'top_factor': top_factor}
#         todos_los_resultados.append(('Secuencial', get_results(**inputs_original)))

#         print(f"\n--- [Run {i+1}] MIDIENDO MULTIPROCESSING ---")
#         inputs_multiprocessing = {'parent_func': running_records, 'child_func': ejecucion_con_multiprocessing, 'inputs': data, 'top_factor': top_factor}
#         todos_los_resultados.append(('Multiprocessing', get_results(**inputs_multiprocessing)))

#         print(f"\n--- [Run {i+1}] MIDIENDO THREADING ---")
#         inputs_threading = {'parent_func': running_records, 'child_func': ejecucion_con_threading, 'inputs': data, 'top_factor': top_factor}
#         todos_los_resultados.append(('Threading', get_results(**inputs_threading)))

#         print(f"\n--- [Run {i+1}] MIDIENDO ASYNCIO ---")
#         inputs_asyncio = {'parent_func': running_records, 'child_func': ejecucion_con_asyncio, 'inputs': data, 'top_factor': top_factor}
#         todos_los_resultados.append(('Asyncio', get_results(**inputs_asyncio)))

#         # --- VISUALIZACIÓN INTERMEDIA (AHORA ES LÓGICA Y CONSISTENTE) ---
#         print(f"\n{'*'*15} VISUALIZACIÓN DESPUÉS DE LA EJECUCIÓN {i+1} {'*'*15}\n")

#         # 1. Prepara el DataFrame una sola vez con los datos acumulados
#         df_resultados_parciales = preparar_dataframe(todos_los_resultados)

#         # 2. Pasa el MISMO DataFrame a TODAS las funciones de graficado
#         print(f"--- [Run {i+1}] Generando Gráfico de Series Comparativas ---")
#         graficar_series_comparativas(df_resultados_parciales)

#         print(f"\n--- [Run {i+1}] Generando Dashboard Comparativo ---")
#         # graficar_dashboard_comparativo(df_resultados_parciales) # <-- AHORA USA LOS PARCIALES

#     # --- ANÁLISIS FINAL ---
#     print(f"\n{'='*20} ANÁLISIS FINAL DE LAS {NUM_EJECUCIONES} EJECUCIONES {'='*20}\n")
#     df_resultados_finales = preparar_dataframe(todos_los_resultados)

#     print("\n--- Generando Gráfico de Distribución de Frecuencias Final (Boxplot) ---")
#     graficar_distribuciones(df_resultados_finales)

"""
