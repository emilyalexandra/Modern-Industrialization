from glob import glob
from collections import defaultdict
from pathlib import Path

import os
import json

path = "src/main/resources/data/modern_industrialization/recipes/"
path_output = "src/main/resources/data/modern_industrialization/recipes/generated/assembler/"

Path(path_output).mkdir(parents=True, exist_ok=True)

file_list = Path(path).rglob('*.json')
for f in file_list:
    file_name = os.path.basename(f)

    if file_name[-10:] == '_asbl.json':
        print(f)

        with open(f, "r") as file:
            json_file = json.load(file)
            json_output = {}
            json_output["type"] = "modern_industrialization:assembler"
            json_output["eu"] = 8
            json_output["duration"] = 200

            item_inputs_dict = defaultdict(lambda: 0)
            item_inputs = []

            for s in json_file["pattern"]:
                for c in s:
                    if c != " ":
                        key = json_file["key"][c]["item"]
                        item_inputs_dict[key] = item_inputs_dict[key] + 1

            for i, c in item_inputs_dict.items():
                item_inputs.append({"item": i, "amount": c})

            json_output["item_inputs"] = item_inputs
            item_ouput = json_file["result"]["item"]
            item_ouput_count = json_file["result"][
                "count"] if "count" in json_file["result"] else 1

            json_output["item_outputs"] = [
                {"item": item_ouput, "amount": item_ouput_count}]

            with open(path_output + item_ouput.split(':')[-1] + ".json", "w") as file_output:
                json.dump(json_output, file_output, indent=4)