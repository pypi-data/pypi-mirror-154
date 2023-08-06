from datetime import datetime
import argparse
import os.path
from operator import itemgetter

FORMAT_DATE = "%Y-%m-%d_%I:%M:%S.%f"

START_LOG = "start.log"
END_LOG = "end.log"
ABBR_TXT = "abbreviations.txt"


def get_files_paths(dir_path):
    path_files = [START_LOG, END_LOG, ABBR_TXT]
    files_path = ()
    for i in path_files:
        full_path = os.path.join(dir_path, i)
        if not os.path.exists(full_path):
            print(f'File {i} not found.')
            exit()

        files_path += (full_path,)

    return files_path


def open_log_file(path_to_file):
    with open(path_to_file, "r") as report:
        data = report.readlines()
        racer_report = {}
        for i in data:
            i = i.strip()
            racer = i[:3]
            racer_report[racer] = datetime.strptime(i[3:], FORMAT_DATE)
        return racer_report


def open_abbr_file(path_to_file):
    with open(path_to_file, "r") as abbreviations:
        data_abbr = abbreviations.readlines()
        abbr_dict = {}

        for i in data_abbr:
            abbr, name, team = i.strip().split("_")
            abbr_dict[abbr] = (name, team)
        return abbr_dict


def get_time_delta(data_start: dict, data_end: dict):
    result = dict()
    for key, start_time in data_start.items():
        end_time = data_end.get(key)
        result[key] = end_time - start_time if end_time and end_time > start_time else None

    return result


def build_report(start_file, end_file, abbreviations_file, desc: bool = False, driver: str = None):
    racer_start_report = open_log_file(start_file)
    racer_end_report = open_log_file(end_file)
    abbr_dict = open_abbr_file(abbreviations_file)
    time_delta = get_time_delta(racer_start_report, racer_end_report)
    results = [(name, team, time_delta.get(abbr)) for abbr, (name, team) in abbr_dict.items()]
    errors = [i for i in results if i[2] is None]
    correct = [i for i in results if i[2] is not None]
    correct.sort(key=itemgetter(2), reverse=desc)
    results = correct + errors
    if driver:
        results = list(filter(lambda x: x[0] == driver, results))
    return results


def print_report(report):
    for index, (name, team, timedelta) in enumerate(report, 1):
        time = str(timedelta)[:-3] if timedelta else 'Invalid data'
        print(f'{index}. {name:20}|{team:30}|{time}')
        if index == 15:
            print('-' * 80)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--files_dir", help="folder_path", nargs="?")
    parser.add_argument("--driver", help="Enter driver's name")
    parser.add_argument("--desc", help="optional")
    args = parser.parse_args()
    if args.files_dir:
        file_start, file_end, abbr = get_files_paths(args.files_dir)
    else:
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(root_dir, 'data')
        file_start, file_end, abbr = get_files_paths(data_dir)
    print_report(build_report(file_start, file_end, abbr, driver=args.driver, desc=bool(args.desc)))


if __name__ == '__main__':
    main()

