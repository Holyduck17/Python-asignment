import os
from datetime import datetime

river_stations = {
    'Sungai Klang KL': {'state': 'Selangor', 'wqi': 68.3, 'status': ''},
    'Sungai Muar': {'state': 'Johor', 'wqi': 54.1, 'status': ''},
    'Sungai Kedah': {'state': 'Kedah', 'wqi': 82.5, 'status': ''},
    'Sungai Singapore': {'state': 'Singapore', 'wqi': 45.0, 'status': ''}
}

reading_log = []


def classify_water_quality(wqi):
    if wqi > 92.7:
        return "Class I", "Clean"
    elif wqi > 76.5:
        return "Class II", "Slightly Polluted"
    elif wqi > 51.9:
        return "Class III", "Moderately Polluted"
    elif wqi > 31.0:
        return "Class IV", "Polluted"
    else:
        return "Class V", "Heavily Polluted"


def update_status():
    for data in river_stations.values():
        _, status = classify_water_quality(data['wqi'])
        data['status'] = status


def display_river_information():
    print("\nRiver Information:")
    print(f"{'Station':30} {'State':15} {'WQI':>6} {'Status':20}")
    print("-" * 75)
    for station, data in river_stations.items():
        print(f"{station:30} {data['state']:15} {data['wqi']:6.1f} {data['status']:20}")


def classify_all_stations():
    update_status()
    display_river_information()


def add_update_station():
    name = input("Enter station name: ").strip()
    state = input("Enter state: ").strip()
    wqi_input = input("Enter WQI: ").strip()

    if not name or not state:
        print("Error: Station name and state cannot be empty.")
        return

    try:
        wqi = float(wqi_input)
    except ValueError:
        print("Error: WQI value must be a numeric value.")
        return

    if wqi < 0 or wqi > 100:
        print("Error: WQI value must be between 0 and 100.")
        return

    if name in river_stations:
        river_stations[name]['state'] = state
        river_stations[name]['wqi'] = wqi
        print(f"Station {name} updated with new WQI: {wqi}.")
    else:
        river_stations[name] = {'state': state, 'wqi': wqi, 'status': ''}
        print(f"New station {name} added.")

    update_status()


def log_monitoring_reading():
    name = input("Enter station name: ").strip()
    if name not in river_stations:
        print(f"Error: Station {name} not found.")
        return

    wqi_input = input("Enter WQI reading: ").strip()
    try:
        wqi = float(wqi_input)
    except ValueError:
        print("Error: WQI value must be numeric.")
        return

    if wqi < 0 or wqi > 100:
        print("Error: WQI value must be between 0 and 100.")
        return

    river_stations[name]['wqi'] = wqi
    update_status()
    timestamp = datetime.now()
    reading_log.append((timestamp, name, wqi))
    print(f"Reading logged for {name} at {timestamp.strftime('%Y-%m-%d %H:%M:%S')}.")

    polluted_stations = [
        (station, data) for station, data in river_stations.items() if data['wqi'] < 51.9
    ]

    if polluted_stations:
        for station, data in polluted_stations:
            print(f"[!] ALERT: {station} in {data['state']} is {data['status']} (WQI: {data['wqi']}).")
    else:
        print("All monitored rivers are within acceptable quality levels.")

    if not reading_log:
        print("No readings have been logged yet.")
    else:
        print("\nMonitoring Log:")
        for entry in reading_log:
            print(f"{entry[0].strftime('%Y-%m-%d %H:%M:%S')} - {entry[1]}: WQI {entry[2]}")


def display_menu():
    print("\n======= Main Menu =======")
    print("1. Classify All Stations")
    print("2. Add / Update Station")
    print("3. Log Monitoring Reading")
    print("4. Trend Analysis")
    print("5. Export / Load Data")
    print("0. Exit")
    print("=========================\n")


class RiverStation:
    def __init__(self, name, state, wqi):
        self.name = name
        self.state = state
        self.wqi = wqi

    def get_classification(self):
        return classify_water_quality(self.wqi)[0]

    def summary(self):
        return f"{self.name} | {self.state} | WQI: {self.wqi} | {self.get_classification()}"


def analyze_trends():
    print("\n--- RiverStation Summaries ---")
    station_objects = []
    for index, (name, data) in enumerate(river_stations.items()):
        if index >= 2:
            break
        station_objects.append(RiverStation(name, data['state'], data['wqi']))

    if station_objects:
        for station in station_objects:
            print(station.summary())
    else:
        print("No river stations available for summary.")

    print("\n--- Average WQI by State ---")
    state_wqis = {}
    for data in river_stations.values():
        state_wqis.setdefault(data['state'], []).append(data['wqi'])

    sorted_states = sorted(
        ((state, sum(wqis) / len(wqis)) for state, wqis in state_wqis.items()),
        key=lambda item: item[1],
        reverse=True,
    )

    for state, avg_wqi in sorted_states:
        print(f"{state}: {avg_wqi:.1f}")

    print("\n--- Trend Identification ---")
    station_readings = {}
    for _, name, wqi in reading_log:
        station_readings.setdefault(name, []).append(wqi)

    valid_trends = {name: values for name, values in station_readings.items() if len(values) >= 2}
    if not valid_trends:
        print("Insufficient data for trend analysis. Please log more readings.")
    else:
        improvements = {name: max(values) - min(values) for name, values in valid_trends.items()}
        print(f"Greatest improvement/variation: {max(improvements, key=improvements.get)}")
        print(f"Least improvement/greatest decline: {min(improvements, key=improvements.get)}")

    print("\n--- Class Distribution ---")
    class_counts = {"Class I": 0, "Class II": 0, "Class III": 0, "Class IV": 0, "Class V": 0}
    for data in river_stations.values():
        class_label = classify_water_quality(data['wqi'])[0]
        class_counts[class_label] += 1

    for cls, count in class_counts.items():
        print(f"{cls}: {count} station(s)")


def export_report(filename="river_report.txt"):
    try:
        with open(filename, "w", encoding="utf-8") as report_file:
            report_file.write("River Monitoring Report\n")
            report_file.write(f"Generated on: {datetime.now():%Y-%m-%d %H:%M:%S}\n\n")
            report_file.write("Station Information:\n")
            for station, data in river_stations.items():
                report_file.write(
                    f"{station}, {data['state']}, {data['wqi']}, {data['status']}\n"
                )
            report_file.write("\nMonitoring Log:\n")
            for entry in reading_log:
                report_file.write(
                    f"{entry[0].strftime('%Y-%m-%d %H:%M:%S')}, {entry[1]}, {entry[2]}\n"
                )
        print(f"Report exported successfully to '{filename}'.")
    except PermissionError:
        print(f"Error: Permission denied when writing '{filename}'.")


def save_station_data(filename="river_stations.txt"):
    try:
        with open(filename, "w", encoding="utf-8") as data_file:
            for station, data in river_stations.items():
                data_file.write(f"{station}, {data['state']}, {data['wqi']}, {data['status']}\n")
        print(f"Station data saved successfully to '{filename}'.")
    except PermissionError:
        print(f"Error: Permission denied when writing '{filename}'.")


def load_station_data(filename="river_stations.txt"):
    try:
        with open(filename, "r", encoding="utf-8") as data_file:
            loaded_stations = {}
            for line_number, line in enumerate(data_file, start=1):
                if not line.strip():
                    continue
                parts = [field.strip() for field in line.split(",")]
                if len(parts) != 4:
                    raise ValueError(
                        f"Invalid format on line {line_number}: expected 4 values."
                    )
                station_name, state, wqi_text, status = parts
                try:
                    wqi = float(wqi_text)
                except ValueError:
                    raise ValueError(
                        f"Invalid WQI value on line {line_number}: {wqi_text}"
                    )
                loaded_stations[station_name] = {
                    'state': state,
                    'wqi': wqi,
                    'status': status,
                }
        river_stations.clear()
        river_stations.update(loaded_stations)
        update_status()
        print(f"Station data loaded successfully from '{filename}'.")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except PermissionError:
        print(f"Error: Permission denied when accessing '{filename}'.")
    except ValueError as error:
        print(f"Error: {error}")


def export_menu():
    while True:
        print("\n--- Export / Load Data ---")
        print("1. Export Report")
        print("2. Save station data to file")
        print("3. Load station data from file")
        print("0. Back to main menu")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            export_report()
        elif choice == '2':
            save_station_data()
        elif choice == '3':
            filename = input("Enter filename to load (default river_stations.txt): ").strip() or "river_stations.txt"
            load_station_data(filename)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    update_status()
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            classify_all_stations()
        elif choice == '2':
            add_update_station()
        elif choice == '3':
            log_monitoring_reading()
        elif choice == '4':
            analyze_trends()
        elif choice == '5':
            export_menu()
        elif choice == '0':
            print("Exiting the River Quality Monitoring System.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()