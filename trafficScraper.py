import requests
from datetime import datetime

# Python script that tracks traffic in some of New York's most busy places such as the George Washington bridge.
# It uses data.cityofnewyork.us API to get the needed JSON data it then sorts it by the location that the user wants.
# It will also tell you an estimated bounded and unbounded toll price based on the traffic it's seeing.

counter = 0
car_num  = 0

#import all of the times of day
timeFile = open('times.txt', 'r')
time = timeFile.readlines()
times_list = []
times_list.extend(time)
#strip the end line off of each line
t= map(lambda s: s.strip(), times_list)

#import the total amount of cars per hour
totalFile = open('totals.txt', 'r')
total = totalFile.readlines()
total_list = []
total_list.extend(total)
#strip the end line off of each line
t = map(lambda s: s.strip(), total_list)


#take out the \n of all list components
for r in range(len(times_list)):
    total_list[r] =total_list[r].strip('\n')

for t in range(len(times_list)):
    times_list[t] =times_list[t].strip('\n')


#check weather it is AM or PM
for k in range(len(total_list)):
    hour = int(datetime.now().hour)
    morning_or_afternoon = 'am'
    if hour >= 0 and hour < 12:
        morning_or_afternoon = 'am'
    else:
        morning_or_afternoon = 'pm'

#convert the current hour to string
hour = str(datetime.now().hour)
#concatinate AM or PM to hour
new_Time= hour + morning_or_afternoon

#match the current time with the time on the list
for i in range(len(times_list)):
    if times_list[i] == new_Time:
        car_num = total_list[i]


#grab the json data
hour = int(datetime.now().hour)
url = "https://data.cityofnewyork.us/resource/i4gi-tjb9.json"
info = requests.get(url)

#append all speed values to a list if its in the GW bridge
speed_list = []
for i in range(0,1000):
    owner = info.json()[i]['owner']
    if owner == 'PA-GWBridge':
        car_speed = float(info.json()[i]['speed'])
        speed_list.append(car_speed)


#find thes average speed of all cars
sum = sum(speed_list)
#med_speed is the average car speed
med_speed = sum/len(speed_list)



def car_num_max(car_num):
    #place a limit on the number of cars (to put a cap on the price)
    if car_num >= 10000:
        car_num = 10000
    else:
        car_num = car_num
    return car_num

def car_speed_max(car_speed):
    #put a limit to car speed
    if car_speed >= 50:
        car_speed = 50
    elif car_speed <= 10:
        car_speed = 10
    else:
        car_speed = car_speed
    return car_speed

def price_bounds(price):
    #put bounds on the price
    if price >= 15:
        price = 15
    elif price <= 5:
        price = 5
    else:
        price = price
    return price


car_num = int(car_num)
#create a new price for each car with and without bounds
for speeds in range(len(speed_list)):
    price = ((car_num_max(car_num)) - (200 * ((car_speed_max(speed_list[speeds])) - med_speed))) / 400
    car_num_max(car_num)
    car_speed_max(speed_list[speeds])
    price_bounds(price)
    print("-------------------------------------------------------------")
    #To get the rest of the cars for the hour you need to pay
    print("the current cars speed is: %r" % speed_list[speeds])
    print("The toll price (with bounds) is: $", price_bounds(price))
    print("The toll price (without price bounds) is: $", price)


print("The total number of cars in the last hour is %r" % car_num)
print("The average speed is for all the cars in this hour: %r" % med_speed)


#create a loop--> all possibilities, car speed, traffic number