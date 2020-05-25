# Working with the OpenMensa Api
This page is ment to describe all specific parts of the [OpenMensaApi](https://doc.openmensa.org/api/v2/) needed for getting information about meals in the STUWE canteens in Dresden.

## General information
OpenMensa is a projekt ment to store all neccessary information about as many cateens as possible to provide easy and central access to these information for menu apps and interested people. Every one can use it and get data from their database via the OpenMensa api. Also it's possible to write your own parser that adds new meals for missing canteens. For example by crawling the data from the canteens website.

## How to get data from the api
Everthing works via GET requests. That means simply open an URL which holds all your search parameters. 
E.g. https://openmensa.org/api/v2/canteens will give you all cateens in the OpenMensa database.
An api request has two parts the _Base URL_ which is the same for all requests: https://openmensa.org/api/v2/
and the parameters that specify your search. For example /canteens. It's also possible to go a step further and add more restrictions to the search. Like ```/canteens/1``` will only show you information about the canteen with ID 1.

### Call the Api
- Open Firefox and just paste the request URL you built their. This is nice to get an overview and check if the URL works as Firefox is presenting the answer in a nicly styled form.
- To get the information with python use python the libary ```requests```.
Doing a request with this is as easy as follows:
```python
    import request
    resp = requests.get(url)
    meals = resp.json()
```
Url is a variable that holds the full URL as described above. Meals holds a python array with with the response where you can get the information from after the request.


## Canteen IDs
Every canteen in the OpenMensa Database has it's own unique ID to get information about this particular canteen like meals, opening hours, etc.

| canteen name     | ID |
|------------------|----|
| Zeltschlösschen  | 78 |
| Alte Mensa       | 79 | 
| Siedepunkt       | 82 |
| UBoot - BioMensa | 88 |

### How did I get this IDs?
1. Get coords of a central canteen
AlteMensa: 51.0269492, 13.7264910
2. Use the Api to get all canteens in a radius arround this point. 
    ```
    https://openmensa.org/api/v2/canteens?near[lat]=51.0269492&near[lng]=13.7264910&near[dist]=5
    ```
    This link gets all canteens in a radius of **5 km** arround the location of the _Alte Mensa_.

3. Take a look at the resulting json array with all canteens found in this area. As you can see the Alte Mensa has the id _79_.
    ```
    {"id":79,"name":"Dresden, Alte Mensa","city":"Dresden","address":"Mommsenstr. 13, 01069 Dresden, Deutschland","coordinates":[51.0269420344792,13.7264835834503]}
    ```

## Request the menu for a specific mensa for a single day

Blueprint for the request URL:
```
https://openmensa.org/api/v2/canteens/:id/days/:time_period/meals
```

```:id``` => specific canteen ID from above

```:time_period``` => date in the format ```yyyy-mm-dd```

Example request for all meals in the alte Mensa at 21.01.2020:

```
https://openmensa.org/api/v2/canteens/79/days/2020-01-21/meals
```

To get all meals for a time period you have to request every single day. The python program does this with a for loop over all days.

```python
year = 2020
sdate = date(year, 1, 1)   # start date
edate = date(year, 12, 31)   # end date

delta = edate - sdate # get time period

for i in range(delta.days + 1):
    day = sdate + timedelta(days=i)
    meals = getMealsFromApi(canteen[0], day)
```



# OpenMensa Api vs. Stuwe api
Next to the official OpenMensa api the Stuwe offers it's own api. This [Stuwe api](https://www.studentenwerk-dresden.de/mensen/speiseplan-api.html) follows the structure of the official Api but only holds the data for Stuwe canteens.
Also their are some differences:

## Different IDs for canteens
### OpenMensa Api

| canteen name     | ID |
|------------------|----|
| Zeltschlösschen  | 78 |
| Alte Mensa       | 79 | 
| Siedepunkt       | 82 |
| UBoot - BioMensa | 88 |

### Stuwe Api

| canteen name     | ID |
|------------------|----|
| Zeltschlösschen  | 35 |
| Alte Mensa       | 4  | 
| Siedepunkt       | 9  |
| UBoot - BioMensa | 29 |

Get all IDs: 
```https://api.studentenwerk-dresden.de/openmensa/v2/canteens```

## Behaviour with sold out meals
### OpenMensa Api
For meals that were sold out the prices are removed.

### Stuwe Api
For meals that were sold out the prices the whole meals get removed entirely.

## Promitted Meal data
The data is the same, but the Stuwe Api in addition offers images for some meals.


