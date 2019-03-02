Acurite + Weewx-SDR + SmartHUB (optional) + Acurite Access (optional)
---

In early 2018 Acurite (Chaney Instruments) made a [decision to
discontinue](https://www.acurite.com/blog/extending-end-of-service-and-support-for-acurite-smarthub.html)
support of their SmartHUB device in August 2018, meaning they would cripple the
device and turn off their cloud endpoint so it would would not longer be able to send
data to their MyAcurite cloud. This announcment went off like a lead balloon
and they backpedaled and extended support until Feb. 28, 2019 and gave people a
discount for their Acurite Access (a device which didn't provide as frequent updates as
SmartHUB AND it didn't support as many sensors - basically a downgrade for
many). Users who wanted to continue to send data to MyAcurite were required to upgrade
to the Acurite Access to continue to do so. Now that that date is passed,
and you'll (likely?) be unable to manage your sensors connected to your
SmartHUB in the future, what should you do? Well don't give Chaney any more money...

My solution was to get a discounted Access and keep it in the box until right
before the dropdead date, but a better option would be to spend $20 on a [USB
SDR Receiver](https://www.amazon.com/gp/product/B009U7WZCA) and $50 on a
[Raspberry
Pi](https://www.amazon.com/CanaKit-Raspberry-Power-Supply-Listed/dp/B07BC6WH7V/ref=sr_1_4?keywords=canakit&qid=1551490187&s=gateway&sr=8-4)
and **own your weather data** - keep it local and in your control. 

I already had a Rpi 1 B+ and a WiFi dongle - this
will work fine as well. The Software Defined Radio device, combined with some [linux
drivers](https://github.com/matthewwall/weewx-sdr) and
[Weewx](https://github.com/weewx/weewx), essentially allows you to sniff the
Acurite sensor data as they transmit their info over the air - this means you don't
need to give Acurite any more money for their Access device. As an added
benefit, if you still have
your SmartHUB, you can still use it (if still linked to a sensor), to get
pressure data from (since this doesn't come from their sensors). The SmartHUB
and Acurite Access are optional in these instructions, but since I had both and
wanted the MyAcurite app to work, this covers having both the SmartHUB and
Access.

Options for Installation
---
1. Buy a [SDR Receiver](https://www.amazon.com/gp/product/B009U7WZCA)
and connect it to a Linux box or Raspberry Pi. Weewx can upload your data to
Wunderground, CWOP, PWSweather, Open Weathermap, Weather Bug, etc. Your cost is
SDR dongle ($20) + Rpi ($30-50). <br>
**Pros**: Cheapest solution without buying more Acurite hardware. You can send
to other weather providers supported by Weewx.<br>
**Cons**: No MyAcurite app access, no pressure data (pressure data comes from
Access or SmartHUB, not the outdoor sensors).
2. If you want MyAcurite, you need an Acurite Access. You can still use items
in #1 if you want local data and uploads to other providers; you can still use
MyAcurite (through Acurite Access) to upload to Wunderground.  You still won't
have pressure data for your **local** weewx data unless you go to option 3.<br>
**Pros**: You can use the MyAcurite app to get your weather data and to send to
Wunderground.<br>
**Cons**: You don't get local sensor data unless you also do items in #1. Even
if you get local sensor data, you won't get pressure information unless you go
to option #3.
3. If you want **local** data including pressure and ability to send data to providers other than
Wunderground (i.e. Weewx), you'll need to have an old SmartHUB device that is
still linked to some sensor and the items in #1. If you have an old SmartHUB device that just
became recently unsupported, this is where many of you will be at.<br>
**Pros**: All original sensor data will exist locally (sensor data + local
pressure data from SmartHUB). You can also send data to other providers via
Weewx.<br>
**Cons**: MyAcurite won't work unless you also have an Acurite Access. Other con
is that you'll have to run your old SmartHUB just to get pressure data, so you could be running two hubs (SmartHUB and Acurite access)
simultaneously which seems wasteful. 

Installation
---
1. Install
[Rasbian](https://medium.com/@danidudas/install-raspbian-jessie-lite-and-setup-wi-fi-without-access-to-command-line-or-using-the-network-97f065af722e)
on your Pi device and make sure you are using Wifi for LAN. Your Pi will
serve 2 purposes - run Weewx and act as place for your SmartHUB to submit it's
pressure data to (your Pi will answer for hubapi.myacurite.com). 
2. Install Weewx, SDR tools, [Weewx-SDR](https://github.com/matthewwall/weewx-sdr),
connect up your SDR device and make sure you see your sensors show up. 
<pre>
$ sudo apt-get install weewx git cmake libusb-1.0-0-dev
$ mkdir git
$ cd git
$ git clone git://github.com/merbanan/rtl_433
$ git clone git://git.osmocom.org/rtl-sdr.git
$ cd rtl-sdr
$ mkdir build
$ cd build
$ cmake ../ -DINSTALL_UDEV_RULES=ON -DDETACH_KERNEL_DRIVER=ON
$ make
$ sudo make install
$ sudo ldconfig
$ cd ..
$ cd ..
$ cd rtl_433
$ mkdir build
$ cd build
$ cmake ../
$ make
$ sudo make install
</pre>
Now do a test.
<pre>
$ sudo rtl_433 -G
rtl_433 version 18.12-102-g44a5c13 branch master at 201902161227 inputs file rtl_tcp RTL-SDR
Trying conf file at "rtl_433.conf"...
Trying conf file at "/root/.config/rtl_433/rtl_433.conf"...
Trying conf file at "/usr/local/etc/rtl_433/rtl_433.conf"...
Trying conf file at "/etc/rtl_433/rtl_433.conf"...
Registered 114 out of 120 device decoding protocols [ 1-4 6-8 10-17 19-26 29-64 67-120 ]
Found Rafael Micro R820T tuner
Exact sample rate is: 250000.000414 Hz
[R82XX] PLL not locked!
Sample rate set to 250000 S/s.
Tuner gain set to Auto.
Tuned to 433.920MHz.
Allocating 15 zero-copy buffers
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
time      : 2019-03-01 20:56:17
model     : Acurite 5n1 sensor                     sensor_id : 2986          channel   : A             sequence_num: 0           battery   : LOW           message_type: 56          wind_speed: 0.0 kph       temperature: 42.1 F       humidity  : 99
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
time      : 2019-03-01 20:56:17
model     : Acurite 5n1 sensor                     sensor_id : 2986          channel   : A             sequence_num: 1           battery   : LOW           message_type: 56          wind_speed: 0.0 kph       temperature: 42.1 F       humidity  : 99
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
time      : 2019-03-01 20:56:17
model     : Acurite 5n1 sensor                     sensor_id : 2986          channel   : A             sequence_num: 2           battery   : LOW           message_type: 56          wind_speed: 0.0 kph       temperature: 42.1 F       humidity  : 99
</pre>
Now you're in business. Now get the Weewx-SDR driver.
<pre>
$ wget -O weewx-sdr.zip https://github.com/matthewwall/weewx-sdr/archive/master.zip
$ sudo wee_extension --install weewx-sdr.zip
$ sudo wee_config --reconfigure --driver=user.sdr --no-prompt
# Run sdr.py to determine how to map your sensors. 
$ cd /usr/share/weewx
$ sudo PYTHONPATH=. python user/sdr.py --cmd="rtl_433 -M utc -F json -G"
out: ['{"time" : "2019-03-02 01:58:25", "model" : "Acurite 5n1 sensor", "sensor_id" : 2986, "channel" : "A", "sequence_num" : 0, "battery" : "LOW", "message_type" : 49, "wind_speed_kph" : 0.000, "wind_dir_deg" : 270.000, "rain_inch" : 87.580}\n', '{"time" : "2019-03-02 01:58:25", "model" : "Acurite 5n1 sensor", "sensor_id" : 2986, "channel" : "A", "sequence_num" : 1, "battery" : "LOW", "message_type" : 49, "wind_speed_kph" : 0.000, "wind_dir_deg" : 270.000, "rain_inch" : 87.580}\n', '{"time" : "2019-03-02 01:58:25", "model" : "Acurite 5n1 sensor", "sensor_id" : 2986, "channel" : "A", "sequence_num" : 2, "battery" : "LOW", "message_type" : 49, "wind_speed_kph" : 0.000, "wind_dir_deg" : 270.000, "rain_inch" : 87.580}\n']
parsed: {'channel.0BAA.Acurite5n1Packet': u'A', 'rain_total.0BAA.Acurite5n1Packet': 87.58, 'wind_dir.0BAA.Acurite5n1Packet': 270.0, 'dateTime': 1551491905, 'battery.0BAA.Acurite5n1Packet': 1, 'wind_speed.0BAA.Acurite5n1Packet': 0.0, 'usUnits': 1, 'status.0BAA.Acurite5n1Packet': None}
parsed: {'channel.0BAA.Acurite5n1Packet': u'A', 'rain_total.0BAA.Acurite5n1Packet': 87.58, 'wind_dir.0BAA.Acurite5n1Packet': 270.0, 'dateTime': 1551491905, 'battery.0BAA.Acurite5n1Packet': 1, 'wind_speed.0BAA.Acurite5n1Packet': 0.0, 'usUnits': 1, 'status.0BAA.Acurite5n1Packet': None}
parsed: {'channel.0BAA.Acurite5n1Packet': u'A', 'rain_total.0BAA.Acurite5n1Packet': 87.58, 'wind_dir.0BAA.Acurite5n1Packet': 270.0, 'dateTime': 1551491905, 'battery.0BAA.Acurite5n1Packet': 1, 'wind_speed.0BAA.Acurite5n1Packet': 0.0, 'usUnits': 1, 'status.0BAA.Acurite5n1Packet': None}
</pre>
3. If you see above, the output allows you to map your sensor(s) to Weewx. It
should look similar to this, but for more info, check [Weewx-sdr
instructions](https://github.com/matthewwall/weewx-sdr). This will go in
/etc/weewx/weewx.conf. If you have more sensors, you can use extraTemp1,
extraTemp2 and extraTemp3 as sensor names to map addіtional data to. 
<pre>
# collect data from Acurite 5n1 sensor 0BAA and t/h sensor 24A4
[SDR]
    driver = user.sdr
    [[sensor_map]]
        windDir = wind_dir.0BAA.Acurite5n1Packet
        windSpeed = wind_speed.0BAA.Acurite5n1Packet
        outTemp = temperature.0BAA.Acurite5n1Packet
        outHumidity = humidity.0BAA.Acurite5n1Packet
        rain_total = rain_total.0BAA.Acurite5n1Packet
        inTemp = temperature.24A4.AcuriteTowerPacket
        inHumidity = humidity.24A4.AcuriteTowerPacket
</pre>
Restart Weewx
<pre>
sudo /etc/init.d/weewx stop
sudo /etc/init.d/weewx start
</pre>
4. Hopefully you're getting sensor data now, go to http://your.ip.address/weewx
and verify that you are getting data from your sensors and check
/var/log/syslog if you're not. You won't get pressure data, so here's where
your SmartHUB comes in. **If you don't have a SmartHUB, you're done. If you
want to send your Weewx data to other providers, check the config file in
/etc/weewx/weewx.conf**.
5. If you have a SmartHUB that is configured with at least one sensor, then
keep going. Configure your Rpi to be an [ethernet bridge](https://willhaley.com/blog/raspberry-pi-wifi-ethernet-bridge/). Again,
you need to be using Wifi to connect to your lan so you can use ethernet to
connect to your SmartHUB. The linked instructions worked perfect for my Pi 1
B+, and should work for newer devices. Don't connect your SmartHUB yet. 
6. Add an entry to /etc/hosts on your device, it should look similar to below,
but with the ip address (wireless lan IP) of your Pi, same one from step #4.
<pre>
192.168.XX.XX  hubapi.myacurite.com
</pre>
7. Install apache2 and enable cgi support (this assumes that this host only
exists on your LAN and not exposed to the Internet. You're about to enable
access to a webserver on your LAN).
<pre>
$ sudo apt-get install apache2 
$ sudo sudo a2enmod cgi
</pre>
8. Create a file and store it in /usr/lib/cgi-bin/myacurite, make it executable
and create a directory and file to store pressure data.
<pre>
$ sudo vi /usr/lib/cgi-bin/myacurite
</pre>
Contents are based on
[weewx-interceptor](https://github.com/matthewwall/weewx-interceptor) package;
Thanks Matthew for Weewx and this. This is not meant to be secure - if you have
a hostile LAN, then you should adjust your access list in step 9.
<pre>
#!/bin/sh
echo "Content-type: text/html"
echo
echo '{ "success": 1, "checkversion": "224" }'
DATA=$QUERY_STRING
echo "$DATA" | awk -F'baromin=' '{print $2}' | awk -F '&' '{print $1}' > /var/lib/bridge-data/pressure
</pre>
Then change permissions and create the file to collect the data
<pre>
$ sudo chmod 755 /usr/lib/cgi-bin/myacurite
$ sudo mkdir /var/lib/bridge-data
$ sudo touch /var/lib/bridge-data/pressure
$ sudo chown -R www-data:www-data  /var/lib/bridge-data/
</pre>
9. Create a /etc/apache2/conf-enabled/acurite.conf. Change the Allow IP
address/network to be whatever you configured for your DHCP range for your
bridged network in step 5. The Access list is in case you do expose this server
to the Internet, or reverse proxy connections to your internal Weewx
server/Rpi.
<pre>
ScriptAlias /weatherstation/updateweatherstation /usr/lib/cgi-bin/myacurite
&lt;Directory "/usr/lib/cgi-bin"&gt;
    AllowOverride all
    Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
    Order deny,allow
    Deny from all
    Allow from 192.168.6.0/255.255.255.0 ::1/128
    Allow from 127.0.0.1
&lt;/Directory&gt;
</pre>
10. Restart apache 
<pre> 
$ sudo /etc/init.d/apache2 restart
</pre>
11. Copy pond.py (from this repo) to /usr/share/weewx/user and enable in /etc/weewx/weewx.conf
(this is based on [this](https://github.com/weewx/weewx/wiki/add-sensor)). 
<pre>
[Engine]
    [[Services]]
        data_services = user.pond.PondService
</pre>
12. Restart Weewx; check /var/log/syslog for errors.  If you see rtl_433
errors, you may need to make sure your antenna is plugged in. You can only run
1 instance of rtl_433; so if weewx is running, you can't debug using the
commands in step 2, so stop weewx first.  
<pre>
sudo /etc/init.d/weewx stop
sudo /etc/init.d/weewx start
</pre>
13. Connect your SmartHUB to your Rpi via ethernet, it should start sending
data to your Rpi and writing that pressure data to:
/var/lib/bridge-data/pressure. It should not be attempting to send data to
hubapi.myacurite.com (which is now dead anyway).
14. Now you can go to MyAcurite, plug in and register your Acurite Access if
you haven't, and migrate your sensors over to your Access. Never connect your
SmartHUB to the internet as you may lose it's existing configuration (which
doesn't really matter since the only data coming out of SmartHUB that you care
about is the pressure that's coming from the hub itself. You're getting the
rest of the data via SDR). You can go into MyAcurite and remove your old
SmartHUB device as it won't be getting any data anyway.

What did I just do?
---
You now have a setup that:
1) Have a setup that receives signals from Acurite sensors and feeds them into Weewx. 
2) You have local weather data via WeeWx and pressure information (optionally if you have an old SmartHUB). 
3) If you replace any of your sensors, go through the sdr script in step #2 and re-map the new sensor ID's.  
4) WeeWX can also submit to [Wunderground](http://www.weewx.com/docs/usersguide.htm#Wunderground) and others and is much more flexible than just sending data to MyAcurite. I'd also suggest you check out [this
skin](https://github.com/poblabs/weewx-belchertown).
5) If you have an Acurite Access, the MyAcurite app will work, and can
optionally submit data to Wunderground (which may be more reliable than Weewx.
YMMV. 

Bugs/Contact Info
-----------------
Bug me on Twitter at [@brianwilson](http://twitter.com/brianwilson) or email me [here](http://cronological.com/comment.php?ref=bubba).
