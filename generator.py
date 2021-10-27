import pydbgen
from pydbgen import pydbgen
import random
import datetime
from datetime import date
from faker import Faker
from pandas import Series
import pandas


def random_date(start, end):
    return start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )


def generate_salons(myDB):
    salon_num = input("Enter number of salons:")
    salondf = myDB.gen_dataframe(salon_num, fields=['zipcode', 'street_address', 'city'])
    salondf.to_csv('salons.csv', index=True, index_label='id')
    return salondf


def generate_devices(start, end, myDB, salonsdf):
    A, B, C, D, E, F, G = [], [], [], [], [], [], []
    devices_num = input("Enter number of devices:")
    salons_num = len(salonsdf.index)
    dev_stat = ["Running", "Broken", "Running", "Running", "Running"]
    for i in range(int(devices_num)):
        A.append(random.randint(0, salons_num))
        B.append(dev_stat[random.randint(0, len(dev_stat) - 1)])
        C.append(random_date(end, end + (datetime.timedelta(days=(366)))))
        D.append(random_date(end, end))
        E.append(round(random.uniform(500, 10000), 2))

    df = pandas.DataFrame({
        'fk_salon': A,
        'state': B,
        'service_date': C,
        'purchase_date': D,
        'price': E
    })
    df.to_csv('devices.csv', index=True, index_label='id')
    return df


class Worker:
    def __init__(self, name="", surname="", login=0, fk_salon=0):
        self.name = name
        self.surname = surname
        self.login = login
        self.fk_salon = fk_salon


class Client:
    def __init__(self, name="", phone=0, email=""):
        self.name = name
        self.phone = phone
        self.email = email


if __name__ == '__main__':
    myDB = pydbgen.pydb()
    year = input("Enter starting year: ")
    month = input("Month: ")
    day = input("Day: ")
    start = datetime.datetime(int(year), int(month), int(day))
    current = datetime.datetime.today()
    salonsdf = generate_salons(myDB)
    devicesdf = generate_devices(start, current, myDB, salonsdf)

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
        prices[i] += prices[i] * random.choice([0, 5, 10, 15, 20, 25]) / 100
        prices_courses[i] += prices_courses[i] * random.choice([0, 5, 10, 15, 20, 25]) / 100
    # dates of courses
    workers_num = input("Enter number of workers: ")
    workers = [Worker() for i in range(int(workers_num))]
    temp_workers = myDB.gen_data_series(num=int(workers_num), data_type='name')
    A, B, C, D = [], [], [], []
    for i in range(int(workers_num)):
        workers[i].name = temp_workers.at[i].split(" ")[0]
        A.append(temp_workers.at[i].split(" ")[0])
        workers[i].surname = temp_workers.at[i].split(" ")[1]
        B.append(temp_workers.at[i].split(" ")[1])
        workers[i].login = 1000 + i
        C.append(1000 + i)
        workers[i].fk_salon = random.randint(0, len(salonsdf.index) - 1)
        D.append(workers[i].fk_salon)

    workersdf = pandas.DataFrame({
        'name': A,
        'surname': B,
        'login': C,
        'fk_salon': D
    })
    workersdf.to_csv('workers.csv', index=False)

    course_frequency = input("How many times a year courses take place?: ")
    delay = datetime.timedelta(days=(365 / int(course_frequency)))
    courses_startdates = []
    courses = []
    iter = 0
    while (1):
        if ((start + (iter + 1) * delay) > current):
            courses_startdates.append(random_date(start + (iter * delay), current))
            courses.append(random.randint(0, len(course_lengths) - 1))
            break
        courses_startdates.append(random_date(start + (iter * delay), start + (iter + 1) * delay))
        courses.append(random.randint(0, len(course_lengths) - 1))
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

    courses_attendants = int(input("How many workers attend the courses?: "))

    workers_on_courses = []
    for i in range(len(courses)):
        workers_on_courses.append([])
        temp_workers = random.sample(range(0, courses_attendants), random.randint(1, courses_attendants))
        for work in temp_workers:
            workers_on_courses[i].append(work)

    # create lists to connect (sketchy)
    A, B, C, D, E, F, G = [], [], [], [], [], [], []
    for i in range(len(courses_names)):
        for j in range(len(workers_on_courses[i])):
            A.append(courses_names[i])
            B.append(courses_startdates[i])
            C.append(courses_enddates[i])
            D.append(courses_prices[i])
            E.append(workers[workers_on_courses[i][j]].login)
            F.append(workers[workers_on_courses[i][j]].name)
            G.append(workers[workers_on_courses[i][j]].surname)

    df = pandas.DataFrame({
        'course': A,
        'begin_date': B,
        'completion_date': C,
        'price': D,
        'login': E,
        'name': F,
        "surname": G
    })
    df.to_csv('courses.csv', index=False)

    # create client
    clients_num = input("Enter number of clients: ")
    clients = [Client() for i in range(int(clients_num))]
    clients_df = myDB.gen_dataframe(
        clients_num, fields=['name', 'phone', 'email'], real_email=True
    )
    temp = clients_df.name.str.split()
    for i in range(len(temp)):
        temp[i] = temp[i][0]
    clients_df.name = temp
    clients_df.columns = ['name', 'phone_number', 'email']
    clients_df.to_csv('clients.csv', index=False)

    # create service
    services_df = pandas.DataFrame({
        'id': range(len(services)),
        'name': services,
        'price': prices
    })
    services_df.to_csv('service.csv', index=False)

    # wizyta i wykonanie

    # appointment
    appointments_num = input("Enter number of appointments: ")

    # execution
    execution_services = []
    execution_appointments = []
    execution_workers = []
    execution_devices = []
    execution_done = []
    execution_rating = []
    execution_price = []
    for i in range(int(appointments_num)):
        temp_service_id = random.randint(0, len(services_df.index) - 1)
        execution_services.append(temp_service_id)
        execution_workers.append(workers[random.randint(0, int(workers_num) - 1)].login)
        execution_devices.append(random.randint(0, len(devicesdf.index) - 1))
        execution_appointments.append(random.randint(0, int(appointments_num) - 1))
        execution_done.append(1)
        execution_rating.append(random.randint(1, 10))
        execution_price.append(services_df.price[temp_service_id] * random.choice([1, 1, 1, 1, 1, 1, 1, 0.9, 0.8]))

    execution_df = pandas.DataFrame({
        'fk_service': execution_services,
        'fk_worker': execution_workers,
        'fk_devices': execution_devices,
        'fk_appointments': execution_appointments,
        'is_done': execution_done,
        'rating': execution_rating,
        "price": execution_price
    })
    execution_df.to_csv('executions.csv', index=False)

    # appointment continuation
    timespan = current - start
    delay = datetime.timedelta(days=(timespan.days / int(course_frequency)))
    appointments_dates = []
    appointments_salons = []
    appointments_clients = []
    appointments_prices = []
    appointments_ratings = []
    ids = []
    for i in range(int(appointments_num)):
        list_of_executions = [j for j, x in enumerate(execution_appointments) if x == i]
        if (len(list_of_executions) != 0):
            temp_worker_login = execution_workers[list_of_executions[0]]
            iter = 0
            found = False
            for work in workers:
                if work.login == temp_worker_login:
                    found = True
                    break
                iter += 1
            if(found):
                appointments_salons.append(workers[iter].fk_salon)
            else:
                print("yyy")
            # generate date
            appointments_dates.append(random_date(start + (i * delay), start + (i + 1) * delay))
            # get salon's ID from executions - devices.salon
            # appointments_salons.append(random.randint(0, len(salonsdf.index) - 1))
            appointments_clients.append(clients_df.phone_number[random.randint(0, int(clients_num) - 1)])
            #print(execution_df.query("fk_appointment == " + str(i))['fk_worker'].sum())
            #temp_worker_login = execution_workers[execution_appointments.index(i)]
            price = 0
            rating = 0
            for exe in list_of_executions:
                price += execution_price[exe]
                rating += execution_rating[exe]
            rating = round(rating / len(list_of_executions), 2)
            appointments_ratings.append(rating)
            appointments_prices.append(round(price, 2))

    appointments_df = pandas.DataFrame({
        'id': range(len(appointments_dates)),
        'date': appointments_dates,
        'fk_salon': appointments_salons,
        'fk_client': appointments_clients,
        'price': appointments_prices,
        'rating': appointments_ratings,
    })
    appointments_df.to_csv('appointments.csv', index=False)
