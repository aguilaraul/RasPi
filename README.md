# RasPi
**Introduction**

​	Working with the Raspberry Pi 3 Model B, the Freenove Ultimate Starter Kit for Raspberry Pi, and Python, I was able to build an apparatus that reads the temperature from my backyard every thirty minutes, records it into a comma-separated value sheet, and sends a tweet with the current time and temperature at desired time intervals. Afterwards, using the data that was logged, I was able to plot a line graph displaying the daily average temperature, as well as calculate the power output.

​	Following Freenove's Project 11.1 Thermometer tutorial, I used their hardware schematic to wire the circuitry onto the breadboard provided and connected to the 40 pin GPIO built into the Raspberry Pi. The thermistor is able to react to the changes in temperature by changing its electrical resistance. Using Ohm’s Law with the measured resistance, the current temperature is able to be calculated. Every thirty minutes the date and time, the temperature, voltage, and ADC value were recorded into a CSV file that was then parsed to draw a line graph displaying the daily average temperatures. Along with that, a Tweet would be transmitted announcing the current time and temperature.

​	Originally I wanted to make a remote controlled car. There is a tutorial on raspberrypi.org to build a line-following buggy, unfortunately, I did not possess any of the necessary parts, like the chassis, sensors, motors, etc., to make it happen. And once I got the thermometer working, I wanted to wire the LCD screen to present the time and temperature, however, I could not get the software to recognize the ADC value for both the thermistor and the liquid crystal display.

​	Sending a status update to Twitter was confronted with some issues that I was fortunately able to solve. One issue was using emojis on the Raspberry Pi OS. Raspbian can only handle ASCII characters, so Unicode, the code point utilized by emojis, wasn't able to be encoded. But Python can handle Unicode, so it was a matter of encoding the Python file in 'utf-8' then decoding the text before sending it to Twitter.

![img](https://lh5.googleusercontent.com/HgwRxUHVayMFCbqx3k8JWHcbk-7_lTWagbeF9qHO8ckcSbIIt7IwiSDUM0gqfkkUxir0kv_IKiIXt8LabO7ypapSmzWH4Qv_TJalrAm8y3Ki9ZfN8zivaJ5C5U5I4Ty3xNOsuQXU)



**Hardware**

​	The Raspberry Pi 3 Model B is a single-board computer embedded with a Broadcom BCM2837 system-on-a-chip running a quad core 1.2GHz 64bit ARM Cortex-A53 CPU, a Broadcom VideoCore IV GPU, 1GB of LPDDR2 RAM at a frequency of 900MHz, Ethernet and 2.4GHz wireless network connectivity, Bluetooth 4.1, and a 40 pin extended GPIO. The Raspberry Pi also allows you to connect peripherals for input and output, such as an HDMI out display, audio, mouse and keyboard, a CSI camera port for connecting a Raspberry Pi camera, and a DSI display port for connecting a Raspberry Pi touchscreen display. Most importantly, the Raspberry Pi does not include embedded storage, so a MicroSD port is also attached to the board. I loaded the latest version of Raspberry Pi OS (32 bit), as of December 2, 2020; onto a MicroSD card, and, after the initial boot up, have chosen to interact with the Raspberry Pi through a remote desktop viewer called VNC Viewer.

​	This build uses the Raspberry Pi in combination with several pieces from the Freenove Ultimate Starter Kit for Raspberry Pi including: a GPIO extension board and ribbon cable, a breadboard, male-to-male jumper wires, 10k ohm resistors, a PCF8591 ADC module, and a PTC thermistor. The schematic for connecting the circuitry is provided by Freenove in their tutorial.

![img](https://lh4.googleusercontent.com/6Nk3aVV293FpRIyoETg9VtwKjEmWpncM1KlOczoCRYn2jLx0ohps3VmawRx2pvHVbzocflhQb9CDgMhDmhpFHj51a0A1zVekEaX-W10BwmettYNDym2X0pMcz_frAIvKNQCcETPJ)



​	The power consumption of the project was low compared to the Raspberry Pi 3 Model B’s specified typical bare board active current consumption of 400mA. Since the thermistor’s resistance has a positive correlation with the temperature, the resistance increases as the temperature rises. We can use the PCF8591 ADC module to calculate the current passing through it and, using Ohm's Law, calculate the voltage and the power output. The lowest power consumption computed was running at 494mA occurring at 25.5℃. The highest power consumption read at 713mA at 5.8℃. The software was simple too, with the most labor intensive tasks being operating a file, such as opening and writing to it, and sending a message to Twitter. The program is designed to take a reading, log it, and ‘sleep’ for thirty minutes before doing so again, and to use wireless connectivity to send a tweet once per day. Using Python’s time library, the sleep method suspends the execution of the calling thread which puts less stress on the board’s processor. One way to physically reduce power consumption would be to turn off both Bluetooth and WiFi. The software could make less frequent calls to print and write messages that would reduce the amount of processes handled by the CPU thus keeping its power consumption low.

**Software**

​	The Raspberry Pi is running the latest version, as of December 2, 2020, of Raspberry Pi OS (32-bit). I opted to connect to the Pi through a remote desktop viewer, VNC Viewer, that is recommended by Raspberry Pi Foundation, to operate and run the program necessary to collect data.

​	The programming language I used in the build of this project is Python. While formulating the algorithm for what I wanted my project to do, I decided to choose Python for its simplicity and ease of use, especially utilizing the imported libraries to accomplish the tasks of contacting Twitter’s API and painting an immaculate graph. The program running on the Raspberry Pi to read and calculate the temperature is taken from Freenove’s Project 11.1 Thermometer tutorial. However, I modified it to log the information into a CSV file, and send a Tweet with the current temperature at desired time intervals using mathematics and the Twython library. Twython is imported as a wrapper for the Twitter API that makes it simpler to operate. After instantiating the object with my developer keys, I was able to interact with Twitter through a single command after constructing the custom message to send.

​	I wrote two subsequent programs myself. The first program is to parse the data from the file, calculate the daily average temperatures, and graph them using the Matplotlib library. Matplotlib is designed to create static, animated, and interactive visualizations in Python. After parsing the date and calculating the daily temperatures, I was able to feed them into Matplotlib that in return plots and paints a windowed visualization of the data.

​	The second program finds and displays when the lowest power consumption and when the highest power consumption is detected in the data. Because the thermistor determines the electrical resistance, the power consumption also corresponds to the hottest and coldest temperatures captured.

​	Moving forward I would want to treat this device like a real weather station. The Word Meteorological Organization, a specialized agency of the United Nations, states that a generally accepted rule of thumb is to sample at least once during the time constant of the sensor. Figuring out the response time of the thermistor would mean calculating its response to a step change of temperature. I think the additional mathematics and data processing would be worthwhile.

Sources:

Raspberry Pi 3 Model B Specifications

* https://www.raspberrypi.org/products/raspberry-pi-3-model-b/
* https://www.raspberrypi.org/documentation/hardware/raspberrypi/power/README.md
* https://magpi.raspberrypi.org/articles/raspberry-pi-3-specs-benchmarks
* https://www.cnx-software.com/2016/03/01/raspberry-pi-3-odroid-c2-and-pine-a64-development-boards-comparison/

Freenove Ultimate Starter Kit for Raspberry Pi

* https://github.com/Freenove/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi

VNC Viewer

* https://www.realvnc.com/en/connect/download/viewer/

PCF8591 Datasheet

* https://www.nxp.com/docs/en/data-sheet/PCF8591.pdf

Python time.sleep documentation

* https://docs.python.org/3/library/time.html#time.sleep

Twython

* https://twython.readthedocs.io/en/latest/

Matplotlib

* https://matplotlib.org/

Decoding Emojis (Error With Unicode)

* https://www.raspberrypi.org/forums/viewtopic.php?t=56353

Measurements at Automatic Weather Stations

* https://library.wmo.int/doc_num.php?explnum_id=3179