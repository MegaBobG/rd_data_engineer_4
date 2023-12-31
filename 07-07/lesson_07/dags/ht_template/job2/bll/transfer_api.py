import os
from ht_template.job2.dal.local_disk import read_data, load_data
from pathlib import Path

dag_path = os.getcwd()

def transfer_from_raw_to_stg(raw_dir: str, stg_dir: str) -> None:
    data_list = read_data(raw_dir)
    load_data(stg_dir, data_list)
