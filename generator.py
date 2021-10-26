import pydbgen
from pydbgen import pydbgen
import random
import datetime
from datetime import date
from faker import Faker
from pandas import Series

def random_date(start, end):
    return start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

class Worker:
    def __init__(self, name="", surname="", login=0):
        self.name = name
        self.surname = surname
        self.login = login

if __name__ == '__main__':
    myDB = pydbgen.pydb()
    services = ["Manicure", "Pedicure", "Body Waxing", "Face Waxing", "Event Makeup", "Wedding Specials",
                "Massage", "Eyebrow Shaping", "Eyelash Extension", "Milk Peel", "Derma Roller", "Freckle Bleaching",
                "Acne Treatments", "Moisturizing Facials", "Hair Conditioning", "Haircut"]
    prices = [15, 35, 40, 15, 80, 300,
              100, 6, 140, 20, 25, 750,
              55, 35, 30, 25]
    prices_courses = [300, 400, 80, 100, 700, 1200,
                      600, 50, 350, 50, 50, 1000,
                      350, 175, 300, 450]
    course_lengths = [2, 2, 1, 1, 5, 7,
                      4, 1, 3, 1, 1, 3,
                      3, 1, 2, 4]
    # randomize prices
    for i in range(len(prices)):
        prices[i] += prices[i] * random.choice([0,5,10,15,20,25])/100
        prices_courses[i] += prices_courses[i] * random.choice([0, 5, 10, 15, 20, 25]) / 100
    # dates of courses
    workers_num = input("Enter number of workers: ")
    workers = [Worker() for i in range(int(workers_num))]
    temp_workers = myDB.gen_data_series(num=int(workers_num), data_type='name')
    for i in range(int(workers_num)):
        workers[i].name = temp_workers.at[i].split(" ")[0]
        workers[i].surname = temp_workers.at[i].split(" ")[1]


    print(temp_workers.at[0].split(" ")[0])
    year = input("Enter starting year: ")
    month = input("Month: ")
    day = input("Day: ")

    start = datetime.datetime(int(year),int(month),int(day))
    course_frequency = input("How many times a year courses take place?: ")
    current = datetime.datetime.today()
    delay = datetime.timedelta(days=(365/int(course_frequency)))
    courses_startdates = []
    courses = []
    iter = 0
    while(1):
        if((start + (iter+1)*delay) > current):
            courses_startdates.append(random_date(start + (iter*delay), current))
            courses.append(random.randint(0, len(course_lengths) - 1))
            break;
        courses_startdates.append(random_date(start + (iter*delay), start + (iter+1)*delay))
        courses.append(random.randint(0, len(course_lengths)-1))
        iter += 1
    courses_names = []
    courses_prices = []
    for i in range(len(courses)):
        courses_names.append(services[courses[i]])
        courses_prices.append(prices_courses[courses[i]])
    print(courses_names)
    print(courses_startdates)

    # end dates of courses
    # specify length of every course and randomize a little (+/- 1-4 days)?
    courses_enddates = []
    iter = 0
    for course_date in courses_startdates:
        delay = datetime.timedelta(days=(course_lengths[courses[iter]] + random.randint(0, 4)))
        courses_enddates.append(course_date + delay)
        iter += 1
    print(courses_enddates)
    print(courses_prices)

