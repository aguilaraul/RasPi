#
# FindPowerConsumption.py
# Author    Raul Aguilar
# Date      December 7, 2020
#
# Program to read temperature.csv and display the datetime with the
# lowest power consumption and the datetime with the highest power
# consumption
#
# Algorithm:
# 1. With the file open
# 2. Read the first line from the file to set default values for the
# datetime and the ADC value
# 3. For every line in the file, parse the datetime and ADC value from
# the data
# 4. If the parsed ADC value is higher than the one stored, then set
# the new highest ADC value along with the datetime that it occurred.
# 5. If the parsed ADC value is lower than the one stored, then set the
# new lowest ADC value alond with the datetime that it occurred.
# 6. After the file has been processed, calculate the power consumption
# using the ADC values stored and Ohm's Law
# 7. Display results
#

import math

def calculate_power_consumption(adc):
    resistance = 3.3                # ohms
    current = adc / 255.0           # 8-bit ADC
    voltage = current * resistance  # Volts
    power   = voltage * current     # Watts
    mA      = (power / voltage) * 1000
    Rt      = 10 * voltage / (resistance - voltage)
    tempK   = 1/(1/(273.15 + 25) + math.log(Rt/10)/3950.0)
    tempC   = tempK - 273.15
    tempF   = (tempC * (9/5)) + 32

    print("Temperature: %.2f C"%(tempC))
    print("Temperature: %.2f F"%(tempF))
    print("Voltage (V): %.2f"%(voltage))
    print("  Power (W): %.2f"%(power))
    print(" Power (mA): %.2f"%(mA))

if __name__ == '__main__':
    with open('temperatures.csv', 'r') as file:
        tokens = file.readline().split(", ")
        datetime = tokens[0]
        ADCValue = float(tokens[3])
        lowestADC          = ADCValue
        highestADC         = ADCValue
        lowestADC_daytime  = datetime
        highestADC_daytime = datetime
        
        for line in file:
            tokens = line.split(", ")
            datetime   = tokens[0]
            ADCValue   = float(tokens[3])
            
            if ADCValue > highestADC:
                highestADC         = ADCValue
                highestADC_daytime = datetime
            if ADCValue < lowestADC:
                lowestADC         = ADCValue
                lowestADC_daytime = datetime


    print("Lowest Power Consumption:")
    print(lowestADC_daytime)
    calculate_power_consumption(lowestADC)
    print("\nHighest Power Consumption:")
    print(highestADC_daytime)
    calculate_power_consumption(highestADC)
    input('\nhit Return to exit')
