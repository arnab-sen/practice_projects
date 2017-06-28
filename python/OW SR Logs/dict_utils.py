"""
Useful tools to use with dictionaries
"""
import random

### Main Functions ###

def dict_to_string(d):
    """ A neater alternative for converting a dict to a string:
    While str(dict) creates "{key_1:value_1, ..., key_n:value_n}",
    dict_to_string(dict) creates:
    "{
      key_1 : value_1,
      ...,
      key_n : value_n
    }"
    """
    
    dict_string = "{"
    for key in d:
        dict_string += '\n\t"' + str(key) + '" : ' + str(d[key]) + ","
    dict_string = dict_string[:-1] # remove the final comma
    dict_string += "\n}"
    
    return dict_string

def sort_by_date(keys):
    """Sorts date/day/month keys and returns a list
    of the keys in ascending order by converting the
    dates into a list of integer tuples and using list.sort()

    This assumes that the dates provided are valid
    """
    # Order assumed to be "DAY DATE MONTH"
    sorted_keys = []
    months = ["January", "February", "March", "April",
              "May", "June", "July", "August",
              "September", "October", "November", "December"]
    days = ["Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"]
    sorted_keys = date_to_tuples(keys, months, days)
    sorted_dates = tuples_to_dates(sorted_keys, months, days)

    return sorted_dates

### ---------------- ###
### Helper Functions ###

def date_to_tuples(dates, months, days):
    """Converts a list of dates (form "DAY DATE MONTH") into
    a list of tuples, and sorts it, e.g.:
    "Monday 10 December" -> (12, 10, 1)
    """
    sorted_list = []
    
    for entry in dates:
        split = entry.split()
        month = split[2]
        month = months.index(month) + 1
        date = int(split[1])
        day = split[0]
        day = days.index(day) + 1
        sorted_list.append((month, date, day))
        
    sorted_list.sort()

    return sorted_list

def tuples_to_dates(tuple_list, months, days):
    """Converts a list of 3-element tuples into a list
    of dates (form "DAY DATE MONTH"), e.g.:
    (12, 10, 1) -> "Monday 10 December"
    """
    dates = []

    for entry in tuple_list:
        day = days[entry[2] - 1]
        date = entry[1]
        month = months[entry[0] - 1]
        string_date = day + " " + str(date) + " " + month
        dates.append(string_date)

    return dates
    

def get_days_per_month(year = 2017):
    """Returns a dict of key : val = month_n : days in month_n
    """
    days_per_month = {
                        "January" : 31,
                        "February" : 28,
                        "March" : 31,
                        "April" : 30,
                        "May": 31,
                        "June" : 30,
                        "July" : 31,
                        "August" : 31,
                        "September" : 30,
                        "October" : 31,
                        "November" : 30,
                        "December" : 31
                        }

    days_per_month["February"] = 29 if year % 4 == 0 else 28

    return days_per_month

def generate_test_data(num_dates = 1):
    """Returns a list of random dates in the form "DAY DATE MONTH" 
    """
    test_data = []
    days = ["Monday", "Wednesday", "Thursday", "Friday",
            "Saturday", "Sunday"]
    dates = list(range(1, 32))
    days_per_month = get_days_per_month(year = YEAR)
    months = list(days_per_month.keys())    

    for i in range(num_dates):
        rand_day = days[random.randrange(len(days))]
        rand_month = months[random.randrange(len(months))]
        max_days = days_per_month[rand_month]
        rand_date = str(random.randrange(1, max_days))

        test_data.append(rand_day + " " + rand_date + " " + rand_month)

    return test_data

def main():
    pass

def test_main():
    global YEAR
    YEAR = 2017

    test_dates = generate_test_data(num_dates = 5)
    print(test_dates)
    sorted_dates = sort_by_date(test_dates)
    print(sorted_dates)
                  

if __name__ == "__main__":
    test_main()
else:
    main()
