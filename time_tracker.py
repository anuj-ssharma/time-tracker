import argparse
import datetime
import csv

EVENTS = ['start_day', 'start_break', 'end_break', 'end_day']


def calculate_working_hours():
    pass

def calculate_break_duration():
    pass

def record_event(event_name):
    event_time = datetime.datetime.now()
    write_to_file([event_name, event_time])

def write_to_file(data):
    with open('time_tracker.csv', 'ab',) as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(data)


parser = argparse.ArgumentParser()
parser.add_argument('-e', '--event', help="can be start_day, start_break, end_break, end_day")
args = parser.parse_args()
if args.event in EVENTS:
    record_event(args.event)
else:
    print("Invalid event")

