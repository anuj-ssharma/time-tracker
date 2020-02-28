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

def calculate_working_hours():
    read_file()
    seconds_worked_in_day = (END_DAY[0] - START_DAY[0]).total_seconds()
    seconds_break_in_a_day = calculate_break_duration()
    total_working_seconds = seconds_worked_in_day - seconds_break_in_a_day

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

def read_file():
    with open('time_tracker.csv', 'r',) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            event_name = row[0]
            event_datetime = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f')
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

args = parser.parse_args()
if args.event in EVENTS:
    record_event(args.event)
else:
    print("Invalid event")

