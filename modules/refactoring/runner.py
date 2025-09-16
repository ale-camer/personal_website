# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 23:18:21 2025

@author: ale_c
"""

from keyphrase import PipelineExecutor, get_ngrams_output, read_txt, keyphrase_pipeline

if __name__ == "__main__":
    executor = PipelineExecutor(worker=keyphrase_pipeline, combine_fn=get_ngrams_output)
    text = read_txt("whatsapp_chat.txt")

    res_mp = executor.multiprocessing(text)
    res_th = executor.threading(text)
    res_async = executor.asynchronic(text)

    print(res_mp)
