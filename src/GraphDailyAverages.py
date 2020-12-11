#
# GraphDailyAverages.py
# Author    Raul Aguilar
# Date      December 8, 2020
#
# Parses data from temperature.csv to calculate and plot a line graph
# of daily average temperatures
#
# Algorithm:
# 1. While the file is open
# 2. Read the first line in the file to initialize default value of the
# current day and time
# 3. For each line in the file, first split the data into tokens using
# a comma delimiter. Parse the first token into the date and time and
# parse the second token into the temperature.
# 4. If the date is equal to the current day, then add the temperature
# to the day's total and increment the count by one
# 5. If the date is not equal to the current day, then calculate the
# daily temperature average, append the current day to x[] and
# append the daily average to y[]. Print out the information to console.
# Then reset the current day to the new date, the count to one, and the
# day's total temperature to the new date's temperature.
# 6. At the end of file, repeat step 5
# 7. Using matplotlib, plot a line graph of the daily average
# temperatures
#

import matplotlib.pyplot as plt

if __name__ == '__main__':
    x = []
    y = []
    day_total = 0.0
    count     = 0

    with open('temperatures.csv', 'r') as file:
        tokens = file.readline().split(", ")
        current_day, current_time = tokens[0].split(" ")
        for line in file:
            tokens = line.split(", ")
            date, time = tokens[0].split(" ")
            temp       = float(tokens[1])
            if date == current_day:
                day_total += temp
                count     += 1
            else:
                daily_average = day_total/count
                x.append(current_day)
                y.append(daily_average)
                print("{0}: avg temp - {1}".format(current_day, daily_average))
                current_day = date
                count       = 1
                day_total   = temp

            # print(current_day)
            # print(day_total)
            # print(count)
        daily_average = day_total/count
        x.append(current_day)
        y.append(daily_average)
        print("{0}: avg temp - {1}".format(current_day, daily_average))

    # Plot graph
    plt.plot(x, y)

    plt.xlabel("Date")
    plt.ylabel("Temperature (C)")
    plt.title("Daily Average Temperature")

    plt.show()