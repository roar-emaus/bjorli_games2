import csv
from pathlib import Path
from datetime import datetime


def write_csv(data_dict, folder_path):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'scores_{timestamp}.csv'
    file_path = Path("data/")/folder_path / filename

    # Create the folder if it doesn't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)

    headers = ['Deltager'] + list(data_dict[list(data_dict.keys())[0]].keys())

    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(headers)

        for Deltager, scores in data_dict.items():
            row = [Deltager] + list(scores.values())
            csv_writer.writerow(row)


def read_csv(folder_path):
    folder = Path("data/")/folder_path

    def file_timestamp(file):
        return datetime.strptime(file.stem[7:], '%Y%m%d_%H%M%S')

    try:
        latest_file = max(folder.glob('scores_*.csv'), key=file_timestamp)
    except ValueError:
        print("No matching files found.")
        return None

    with open(latest_file, 'r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        data = [row for row in csv_reader]

    return data


def get_games():
    data_path = Path("data")
    folders = [f.name for f in data_path.iterdir() if f.is_dir()]
    return folders


def check_lock(folder_path):
    path = Path(f"data/{folder_path}/.lock")
    return path.exists()



if __name__ == "__main__":
    # Example usage
    data = {
        'Alice': {'game1': 10, 'game2': 20, 'game3': 30},
        'Bob': {'game1': 15, 'game2': 25, 'game3': 35},
        'Eve': {'game1': 20, 'game2': 30, 'game3': 40},
    }
    folder = 'example'

    write_csv(data, folder)
    latest_data = read_csv(folder)
    print(latest_data)
