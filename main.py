import subprocess
import re
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import calendar

path = "/Users/dario/Desktop/logs/"


def count_total_requests(logs):
    extracted_GET_logs = re.findall(r'\d{2}/[A-Za-z]{3}/\d{4}:0?\d{2}:0?\d{2}:0?\d{2} \+0000] "GET', logs)
    return extracted_GET_logs.__len__()


# given the date in string format ("dd/mm/aaaa") returns name day in string format
def data_string_get_day(data_string):
    mese_to_numero = {calendar.month_abbr[i].lower(): i for i in range(1, 13)}
    giorno, mese_str, anno = data_string.split('/')
    mese = mese_to_numero[mese_str.lower()]
    anno = int(anno)

    # Crea un oggetto datetime
    data = datetime(anno, mese, int(giorno))

    # Ottieni il nome del giorno della settimana
    giorno_settimana = calendar.day_name[data.weekday()]
    return giorno_settimana


def month_to_int(month):
    if month == "Jan":
        return 0
    if month == "Feb":
        return 1
    if month == "Mar":
        return 2
    if month == "Apr":
        return 3
    if month == "May":
        return 4
    if month == "Jun":
        return 5
    if month == "Jul":
        return 6
    if month == "Aug":
        return 7
    if month == "Sep":
        return 8
    if month == "Oct":
        return 9
    if month == "Nov":
        return 10
    if month == "Dec":
        return 11


def day_to_int(day):
    if day == "Monday":
        return 0
    elif day == "Tuesday":
        return 1
    elif day == "Wednesday":
        return 2
    elif day == "Thursday":
        return 3
    elif day == "Friday":
        return 4
    elif day == "Saturday":
        return 5
    elif day == "Sunday":
        return 6


# returns a list with 24 elements, each element contains the count of GET requests in the hour defined of index
def extract_hours_count_requests(get_requests):
    extracted_hours = re.findall(r':0?\d{2}:0?\d{2}:0?\d{2}', get_requests)
    hours_count = []
    for hour in range(24):
        time = str(hour).zfill(2)
        times_counter = re.findall(r'\b' + time + r':0?\d{2}:0?\d{2}\b', extracted_hours.__str__())
        result_count = times_counter.__len__()
        hours_count.append(result_count)
    return hours_count


# returns a list of 7 elements, each element contains the request count for the day identified by the array index
def extract_days_count_requests(get_requests):
    data_string = re.findall(r'(\d{2}/[a-zA-Z]{3}/\d{4})', get_requests)
    count_req_day = np.zeros(7)
    for data in data_string:
        day = data_string_get_day(data)
        count_req_day[day_to_int(day)] += 1
    return count_req_day


# returns a list of 12 elements, each element contains the request count of the month identified by the array index
def extract_months_count_requests(get_requests):
    data_string = re.findall(r'(\d{2}/[a-zA-Z]{3}/\d{4})', get_requests)
    count_req_day = np.zeros(12)
    for data in data_string:
        day, month, year = data.split('/')
        count_req_day[month_to_int(month)] += 1
    return count_req_day


def plot(count_hours, count_days, count_months):
    hours = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
             '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
             '20', '21', '22', '23']

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    plt.figure(figsize=(10, 6))
    plt.plot(hours, count_hours)
    plt.xlabel('hours')
    plt.ylabel('count hours requests')
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.figure(figsize=(10, 6))
    plt.plot(days, count_days)
    plt.xlabel('days')
    plt.ylabel('count days requests')
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.figure(figsize=(10, 6))
    plt.plot(months, count_months)
    plt.xlabel('months')
    plt.ylabel('count months requests')
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()


def normalize(count_hours, count_days, count_months):
    sum_count_hours = np.sum(count_hours)
    sum_count_days = np.sum(count_days)
    sum_count_months = np.sum(count_months)
    hours_normalized = count_hours / sum_count_hours
    days_normalized = count_days / sum_count_days
    months_normalized = count_months / sum_count_months

    return hours_normalized, days_normalized, months_normalized


def sum_of_all_requests(count_hours, count_days, count_months):
    sum_h = np.sum(count_hours)
    sum_d = np.sum(count_days)
    sum_m = np.sum(count_months)
    return sum_h + sum_d + sum_m


def calculate_probabilities(hour, day, month, count_hours, count_days, count_months, count_moths_no_norm):
    return count_hours[hour] * count_days[day] * count_months[month] * np.sum(count_moths_no_norm)


def main():
    file_logs = subprocess.check_output(["ls", path])
    file_list_decode = file_logs.decode("utf-8").strip().split('\n')

    count_hours_requests = np.zeros(24)
    count_days_requests = np.zeros(7)
    count_months_requests = np.zeros(12)

    for file in file_list_decode:
        if 'access' in file:
            path_var = path + file
            print("PATH : " + path_var)

            with open(path_var, "r") as file_var:
                var_log = file_var.read()
                file_var.close()

            extracted_GET_logs = re.findall(r'\d{2}/[A-Za-z]{3}/\d{4}:0?\d{2}:0?\d{2}:0?\d{2} \+0000] "GET', var_log)

            days_count_requests_var = extract_days_count_requests(extracted_GET_logs.__str__())

            for i in range(days_count_requests_var.__len__()):
                count_days_requests[i] += days_count_requests_var[i]

            months_count_requests_var = extract_months_count_requests(extracted_GET_logs.__str__())

            for i in range(months_count_requests_var.__len__()):
                count_months_requests[i] += months_count_requests_var[i]

            hours_count_requests_var = extract_hours_count_requests(extracted_GET_logs.__str__())

            for i in range(24):
                count_hours_requests[i] += hours_count_requests_var[i]

    print("\n")
    print(count_hours_requests)
    print("\n")
    print(count_days_requests)
    print("\n")
    print(count_months_requests)
    print("\n")

    plot(count_hours_requests, count_days_requests, count_months_requests)
    hours_normalized, days_normalized, months_normalize = normalize(count_hours_requests, count_days_requests,
                                                                    count_months_requests)
    plot(hours_normalized, days_normalized, months_normalize)

    print("------- NORMALIZED ---------")
    print("\n")
    print(hours_normalized)
    print("\n")
    print(days_normalized)
    print("\n")
    print(months_normalize)

    # ore 10:00
    # 5/Set
    prob = calculate_probabilities(10, 5, 8, hours_normalized, days_normalized, months_normalize, count_months_requests)
    print("\n")
    print(prob)


main()
