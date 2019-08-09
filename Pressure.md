Raspberry Pi Pressure Sensor to Weewx
---

1. You need a [$10 on a pressure sensor](https://www.amazon.com/gp/product/B01LETIESU)
2. Female/Female [dupont
cables](https://www.amazon.com/Yohii-EL-CP-004-Multicolored-Dupont-Breadboard/dp/B07F378FCJ)
- I had these lying around.
3. [3d case for your sensori](https://www.thingiverse.com/thing:3799556) (optional)

Installation
---
1. Connect the sensor device to your Pi![]()
2. [Enable I2C on your
Pi](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c).
Verify connectivity with the sesnor. You should see 76.
<pre>
 i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- 76 --
</pre>
3. Install the python modules:
<pre>
$ sudo apt-get update
$ sudo apt-get install build-essential python-pip python-dev python-smbus git
$ cd ~pi
$ git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
$ cd Adafruit_Python_GPIO
$ sudo python setup.py install
$ cd ..
$ git clone https://github.com/bdwilson/Adafruit_Python_BME280
$ cd Adafruit_Python_BME280
</pre>
4. Verify connectivity to your device again to make sure we can read data:
<pre>
$ python ./Adafruit_BME280_Example.py
Temp      = 31.769 deg C
Pressure  = 1004.16 hPa
Humidity  = 30.67 %
</pre>
5. Install Weewx user program (note: I found this program on one of the weewx forums; I modified it to fit my needs)
<pre>
$ cd /usr/share/weewx/user
$ sudo curl -s FIX -o bme280.py
</pre>
6. Edit Weewx config. Under ''[[Services]]'' section, add this:
<pre>
[Engine]
    [[Services]]
        data_services = user.bme280.bme
</pre>
Also add a section for your BME device above the ''[Engine]'' section. In the
example below, I'm mapping the BME pressure to the ''pressure' device. I'm not
mapping the temperature from the BME device to anything in Weewx. You'll also
need to determine your sea level denominator which is based on # of meters
above sea level. This adjusts the pressure output from the BME to the pressure
at your altitude∵ In my example, I'm 78.9432 meters above sea level:
(1-(6.87535 x (10^-6)) x 78.9432)^5.2561 = 0.99715048109
The other thing to consider is your location where your Adafruit BME280 modules
are installed.
<pre>
[BME280]
    col_pres = pressure
    col_temp = ''
    #sl_denominator = 0.98445116524
    sl_denominator = 0.99715048109  # https://www.raspberrypi.org/forums/viewtopic.php?t=154262
    BME280_lib_location = '/home/pi/Adafruit_Python_BME280'
</pre>
7. Restart Weewx
<pre>
sudo /etc/init.d/weewx stop
sudo /etc/init.d/weewx start
</pre>
8. Check /var/log/syslog for any errors. If you own an Acurite SmartHUB throw it away. 

Bugs/Contact Info
-----------------
Bug me on Twitter at [@brianwilson](http://twitter.com/brianwilson) or email me [here](http://cronological.com/comment.php?ref=bubba).
