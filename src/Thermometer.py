# _*_ coding: UTF-8 _*_
#!/usr/bin/env python3
#############################################################################
# Filename    : Thermometer.py
# Description : DIY Thermometer
# Author      : www.freenove.com
# modification: 2019/03/09
########################################################################
from twython import Twython
import RPi.GPIO as GPIO
from time import sleep, strftime
import math
from ADCDevice import *

adc = ADCDevice()  # Define an ADCDevice class object
log = open('temperatures.csv', 'a')


def setup():
    global adc
    if (adc.detectI2C(0x48)):  # Detect the pcf8591.
        adc = PCF8591()
    elif (adc.detectI2C(0x4b)):  # Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
              "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
              "Program Exit. \n")
        exit(-1)


def send_tweet(tempC, datetime):
    from auth import (
        API_key,
        API_secret_key,
        access_token,
        access_token_secret
    )
    tempF = tempC * (9.0 / 5.0) + 32.0
    date, time = datetime.split(" ")
    hour, minute, second = time.split(":")
    hour = int(hour)
    minute = int(minute)
    message = "Live from Raul's backyard:\n"
    if 0 <= hour < 12:
        meridiem = "am"
    else:
        meridiem = "pm"
    if 5 <= hour < 10:
        emote = " ⛅ "
    elif 10 <= hour < 18:
        emote = " 🌤️ "
    else:
        emote = " 🌙 "
    if hour != 12:
        hour = hour % 12
    message += "%02d:%02d%s%s %.2f F" % (hour, minute, meridiem, emote, tempF)

    # Twython
    twitter = Twython(API_key, API_secret_key, access_token, access_token_secret)
    twitter.update_status(status=message.decode('utf-8'))
    print("Tweeted: %s" % message)


def loop():
    i = 48
    try:
        while True:
            value = adc.analogRead(0)  # read ADC value A0 pin
            voltage = value / 255.0 * 3.3  # calculate voltage
            Rt = 10 * voltage / (3.3 - voltage)  # calculate resistance value of thermistor
            tempK = 1 / (1 / (273.15 + 25) + math.log(Rt / 10) / 3950.0)  # calculate temperature (Kelvin)
            tempC = tempK - 273.15  # calculate temperature (Celsius)
            datetime = strftime("%Y-%m-%d %H:%M:%S")

            # Write to file
            log.write("{0}, {1}, {2}, {3}\n".format(datetime, str(tempC), str(voltage), str(value)))

            # Print to terminal
            print("{0}, {1}".format(datetime, str(tempC)))
            print('ADC Value: %d, Voltage: %.2f\n' % (value, voltage))

            # Use counter to determine 48 * (30 minutes) = 1440 minutes == 24 hours
            # Send tweet every 2 hours
            if i % 4 == 0:
                try:
                    send_tweet(tempC, datetime)
                except:
                    print("Could not send Tweet.")
                i = 48

            sleep(1800)
            i -= 1
    except:
        log.close()


def destroy():
    log.close()
    adc.close()
    GPIO.cleanup()


if __name__ == '__main__':  # Program entrance
    print('Program is starting ... ')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
