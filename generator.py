import pydbgen
from pydbgen import pydbgen
import random
import datetime
from datetime import date

def random_date(start, end):
    return start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

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
    print(random.randint(0,9))
    # randomize prices
    for i in range(len(prices)):
        prices[i] += prices[i] * random.choice([0,5,10,15,20,25])/100
        prices_courses[i] += prices_courses[i] * random.choice([0, 5, 10, 15, 20, 25]) / 100
    # dates of courses
    year = input("Enter starting year: ")
    month = input("Month: ")
    day = input("Day: ")

    start = datetime.datetime(int(year),int(month),int(day))
    course_frequency = input("How many times a year courses take place? :")
    current = datetime.datetime.today()
    delay = datetime.timedelta(days=(365/int(course_frequency)))
    courses = []
    iter = 0
    while(1):
        if((start + (iter+1)*delay) > current):
            courses.append(random_date(start + (iter*delay), current))
            break;
        courses.append(random_date(start + (iter*delay), start + (iter+1)*delay))
        iter += 1
    print(courses)

    # end dates of courses
    # specify length of every course and randomize a little (+/- 1-4 days)?

    print(prices)

