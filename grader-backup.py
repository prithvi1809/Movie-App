import json
import os
from zipfile import ZipFile
import numpy as np
from tqdm import tqdm

import logging
logging.basicConfig(filename='grader.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

# frequency.json

"""solution_path = "frequency.json"

with open(solution_path, "r") as f:
    solution_freq = json.load(f)

frequency_path = "frequency-test.json"
with open(frequency_path, "r") as f:
    frequency = json.load(f)


cntr = 0
for category in solution_freq.keys():

    top_k_true = solution_freq[category]
    top_k = frequency[category]

    top_k_sort = {k: v for k, v in sorted(top_k.items(), key=lambda item: item[1], reverse=True)}"""

def load_file(file, fpath):
    if file.endswith(".json"):

        with open(fpath, 'r') as f:
            output = json.load(f)

    else:

        output = np.loadtxt(fpath, delimiter=',')

    return output

def verify_matrix(candidate, solution, precision=4):

    return (np.round(candidate, precision) == np.round(solution, precision)).all()

def verify_dict(candidate, solution):

    candidate = {k.lower(): v for k, v in candidate.items()}

    is_equal = True

    for category in solution.keys():
        top_k_true = solution[category.lower()]
        top_k = candidate[category.lower()]

        top_k_sort = np.array(list({k: v for k, v in sorted(top_k.items(), key=lambda item: item[1], reverse=True)}.keys()))
        top__k_true_sort = np.array(list({k: v for k, v in sorted(top_k_true.items(), key=lambda item: item[1], reverse=True)}.keys()))


        if not (top_k_sort == top__k_true_sort).all():
            is_equal = False
            break





    return is_equal



def main():

    solution_dict = {
        "frequency": "./solution/frequency.json",
        "matrix": "./solution/matrix-log-nat.txt",
        "scores": "./solution/scores.json"
    }

    output_dict = {}

    submission_dir = "./submissions"
    submissions = os.listdir(submission_dir)
    raw_dir = os.path.join(submission_dir, "raw")

    # open zip files
    for sub in tqdm(submissions):
        if sub.endswith(".zip"):
            name = sub.split(".")[0]
            with ZipFile(os.path.join(submission_dir, sub), 'r') as zip:

                zip.extractall(path=os.path.join(raw_dir, name))

            result = []

            output_dict[name] = {}

            for file_folder in os.listdir(os.path.join(raw_dir, name)):
                if file_folder.startswith("__"):
                    continue
                if os.path.isdir(os.path.join(raw_dir, name, file_folder)):
                    for file in os.listdir(os.path.join(raw_dir, name, file_folder)):
                        if os.path.isdir(os.path.join(raw_dir, name, file_folder, file)):
                            continue
                        if file.lower() not in ["frequency.json", "matrix.txt", "scores.json"]:
                            continue

                        try:

                            sub_type = file.split(".")[0]

                            fpath = f"{raw_dir}/{name}/{file_folder}/{file}"

                            candidate = load_file(file, fpath)

                            solution_path = solution_dict[sub_type]

                            solution = load_file(solution_path, os.path.join(solution_path))


                            if sub_type == "matrix":
                                is_correct = verify_matrix(candidate, solution)
                                result.append(is_correct)
                            elif sub_type in ["frequency", "scores"]:
                                is_correct = verify_dict(candidate, solution)
                                result.append(is_correct)



                        except Exception as err:
                            is_correct = False
                            result.append(is_correct)
                            logging.warning(f"{name}-{err}")

                        output_dict[name][file.split(".")[0]] = str(is_correct)

            if len(result) == 0:
                output_dict[name]["total_score"] = "null"
            else:
                output_dict[name]["total_score"] = .5 + np.mean(result)*.5

    with open("./solution/grades.json", "w") as f:

        json.dump(output_dict, f)




    #with open("./solution/grades.txt", "w") as f:

    #    for name, val in output_dict.items():

    #        f.write(f"{name}: {val}\n")





if __name__ == "__main__":
    main()