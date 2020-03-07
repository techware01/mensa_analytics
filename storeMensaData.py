# -*- coding: utf-8 -*-
import requests
from datetime import date, datetime, timedelta
import csv

API_URL = 'https://openmensa.org/api/v2'


def getRequestUrl(canteen_id, day):
    day_string = day.strftime('%Y-%m-%d')
    return "{}/canteens/{}/days/{}/meals".format(API_URL, canteen_id, day_string)


def getType(notes):
    print(notes)
    if('vegan' in notes):
        return 2
    if('vegetarisch' in notes):
        return 1
    return 0


def getPrice(price):
    if(price == None):
        return None
    return str(price).replace(".", ",")

def isInterestingMeal(meal):
    for category in ['Angebot des Tages', 'Abendangebot']:
        if category == meal['category']:
            return False
    if "Sushi in verschiedenen Sorten" in meal['name']:
        return False
    return True


if __name__ == "__main__":
    sdate = date(2020, 1, 1)   # start date
    edate = date(2020, 3, 6)   # end date

    delta = edate - sdate       # as timedelta

    results = []
    with open('alteMensa.csv', 'wt') as f:
        csv_writer = csv.writer(f, delimiter=';', dialect='excel')
        # write head
        csv_writer.writerow(['date', 'weekday', 'category',
                             'name', 'employees', 'students', 'type'])  # write header

        for i in range(delta.days + 1):
            day = sdate + timedelta(days=i)
            url = getRequestUrl(79, day)
            print(url)
            resp = requests.get(url)
            meals = resp.json()
            if meals != []:
                for meal in meals:
                    if (isInterestingMeal(meal)):
                        employees_price = getPrice(meal['prices']['employees'])
                        stundents_price = getPrice(meal['prices']['students'])
                        row = [day.strftime('%Y-%m-%d'), day.strftime('%a'), meal['category'], meal['name'],
                            employees_price, stundents_price, getType(meal['notes'])]
                        csv_writer.writerow(row)