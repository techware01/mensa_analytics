import requests
from datetime import date, datetime, timedelta
import csv

API_URL = 'https://openmensa.org/api/v2'


def getRequestUrl(canteen_id, day):
    day_string = day.strftime('%Y-%m-%d')
    return "{}/canteens/{}/days/{}/meals".format(API_URL, canteen_id, day_string)


def checkNicePrice(prices):
    students_price = prices['students']
    employees = prices['employees']
    if (employees == None):
        raise ValueError("Employees price is not specified")

    nice_price = round(employees - 0.45 * employees, 2)
    if (students_price == nice_price):
        return True
    return False


def getType(notes):
    if('vegan' in notes):
        return 2
    if('vegetarisch' in notes):
        return 1
    return 0


def isInterestingMeal(meal):
    if meal['category'] == 'Angebote' or meal['category'] == 'Abendangebot':
        if not 'Sushi in verschiedenen Sorten' in meal['name']:
            if not 'Pizza' in meal['name']:
                return True
    return False


def countForCurrentDay(meals):
    counter = {"lunch": [0, 0, 0, 0], "dinner": [0, 0, 0, 0]}
    for meal in meals:
        if isInterestingMeal(meal):
            type_id = getType(meal['notes'])
            if meal['category'] == 'Angebote':
                time = "lunch"
            else:
                time = "dinner"

            # count if it's meat, vegetarian or vegan for the right daytime
            counter[time][type_id] += 1
            try:
                is_nice_price = checkNicePrice(meal['prices'])
                if is_nice_price:
                    counter[time][3] = type_id + 1
                else:
                    print("no nice price")
            except ValueError as e:
                print("No specified price :(")
    return counter

sdate = date(2019, 6, 1)   # start date
edate = date(2020, 3, 6)   # end date

delta = edate - sdate       # as timedelta

results = []
for i in range(delta.days + 1):
    day = sdate + timedelta(days=i) 
    url = getRequestUrl(79, day)
    print(url)
    resp = requests.get(url)
    meals = resp.json()
    dayly_stats = [day.strftime('%Y-%m-%d'), day.strftime('%a'), countForCurrentDay(meals)]
    results.append(dayly_stats)
print(results)



header = ['date', 'weekday', 'meat', 'veg', 'vegan', 'nice', 'meat', 'veg', 'vegan', 'nice']

with open('customers.csv', 'wt') as f:
    csv_writer = csv.writer(f, dialect='excel')

    csv_writer.writerow(header) # write header

    for result in results:
        row = [result[0], result[1]]
        for key in ["lunch", "dinner"]:
            for i in range(4):
                row.append(result[2][key][i])
        csv_writer.writerow(row)