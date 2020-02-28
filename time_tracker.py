import argparse
import datetime
import csv

# TODO: Add validation - break or start time cannot be greater than end_day time
# TODO: Add validation - there cannot be more than one start day or end day date
# TODO: filter out calculation by day

EVENTS = ['start_day', 'start_break', 'end_break', 'end_day', 'calculate']
START_DAY = []
START_BREAK = []
END_BREAK = []
END_DAY = []
FOR_DATE = 'today'

def calculate_working_hours():
    read_file_and_store_data()
    seconds_worked_in_day = calculate_day_duration()
    seconds_break_in_a_day = calculate_break_duration()

    total_working_seconds = seconds_worked_in_day - seconds_break_in_a_day
    total_working_mins = total_working_seconds/60
    total_working_hours = total_working_mins/60
    print("%.2f" % total_working_hours)


def calculate_day_duration():
    if END_DAY == []:
        return (END_BREAK[len(END_BREAK) - 1] - START_DAY[0]).total_seconds()
    else:
        return (END_DAY[0] - START_DAY[0]).total_seconds()


def calculate_break_duration():
    seconds_break_in_a_day = 0
    for start, stop in zip(START_BREAK, END_BREAK):
        seconds_break_in_a_day += (stop - start).total_seconds()
    return seconds_break_in_a_day

def record_event(event_name):
    if event_name == 'calculate':
        calculate_working_hours()
    else:
        event_time = datetime.datetime.now()
        write_to_file([event_name, event_time])

def write_to_file(data):
    with open('time_tracker.csv', 'ab',) as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(data)

def read_file_and_store_data():
    if FOR_DATE == 'today':
        for_date = datetime.datetime.now()
    else:
        for_date = datetime.datetime.strptime(FOR_DATE, '%d-%m-%Y')

    with open('time_tracker.csv', 'r',) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            event_name = row[0]
            event_datetime = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f')
            if event_datetime.date() == for_date.date():
                if event_name == 'start_day':
                    START_DAY.append(event_datetime)
                if event_name == 'start_break':
                    START_BREAK.append(event_datetime)
                if event_name == 'end_break':
                    END_BREAK.append(event_datetime)
                if event_name == 'end_day':
                    END_DAY.append(event_datetime)



parser = argparse.ArgumentParser()
parser.add_argument('-e', '--event', help="can be start_day, start_break, end_break, end_day")
parser.add_argument('-d', '--date', help="date in the format dd-mm-yyyy", default="today")

args = parser.parse_args()
if args.date:
    FOR_DATE = args.date
if args.event in EVENTS:
    record_event(args.event)
else:
    print("Invalid event")

