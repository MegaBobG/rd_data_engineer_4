from ht_template.job1.dal import local_disk, sales_api
import os
import asyncio
import json
import pandas as pd

dag_path = os.getcwd()


# def save_sales_to_local_disk(date: str, raw_dir: str) -> None:
#     # 1. get data from the API
#     # 2. save data to disk
#     print("\tI'm in get_sales(...) function!")
#     json_content = asyncio.run(sales_api.get_sales(date=date))
#     file_name = f"sales_{date}.json"
#     local_disk.save_to_disk(json_content, raw_dir, file_name)
#
#     # Convert json_content to DataFrame if it's a list
#     # if isinstance(json_content, list):
#     #     json_content = pd.DataFrame(json_content)
#
#     # Save DataFrame to CSV
#     # json_content.to_csv(f"{dag_path}/processed_data/{file_name}", index=False)
#
#     pass


def save_sales_to_local_disk(date: str, file_path: str) -> None:
    # 1. Получить данные из API
    json_content = asyncio.run(sales_api.get_sales(date=date))

    # 2. Сохранить данные в файл JSON
    with open(file_path, "w") as file:
        json.dump(json_content, file)