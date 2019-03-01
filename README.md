Acurite + Weewx-SDR + SmartHUB (optional) + Acurite Access (optional)
---

So, Acurite went for a money grab and decided to kill all SmartHUB devices on
Feb 28, 2019. Users who want to continue to send data to MyAcurite must upgrade
to the Acurite Access to continue to do so. You also will be unable to manage
your SmartHUB devices (i.e. add/remove sensors, replace failed sensors, etc)
after Feb 28, 2019. So what do you do?  

My solution was to get a discounted Access and keep it in the box until right
before the dropdead date. I also purchased an [SDR
Receiver](https://www.amazon.com/gp/product/B009U7WZCA) to plug into my old
Raspberry PI B+. The Software Defined Radio device, combined with some [linux
drivers](https://github.com/matthewwall/weewx-sdr) and
[Weewx](https://github.com/weewx/weewx), essentially allows you to sniff the
Acurite sensors as they transmit their info over the air - you don't even need an Access
device or SmartHUB to receive this data. I'll get into why I kept them below,
but both SmartHUB and Acurite access are optional if you're done giving Acurite
your money. 

Options for installation
---
1. Buy a [SDR Receiver](https://www.amazon.com/gp/product/B009U7WZCA)
and connect it to a Linux box or Raspberry Pi. Weewx can upload your data to
Wunderground, CWOP, PWSweather, Open Weathermap, Weather Bug, etc. Your cost is
SDR dongle ($20) + Rpi ($30-50).  
'Pros': Cheapest solution without buying more Acurite hardware
'Cons': No MyAcurite app access, no pressure data (pressure data comes from
Access or SmartHUB, not the outdoor sensors).
2. If you want MyAcurite, you need an Acurite Access. You can still use items
in #1 if you want local data and uploads to other providers; you can still use
MyAcurite (through Acurite Access) to upload to Wunderground.  You still won't
have pressure data for your local data unless you go to option 3.
'Pros': You can use the MyAcurite app to get your weather data and to send to
Wunderground.
'Cons': You don't get local sensor data unless you also do items in #1. Even
if you get local sensor data, you won't get pressure information unless you go
to option #3.
3. If you want local data including pressure and ability to send data to providers other than
Wunderground (i.e. Weewx), you'll need to have an old SmartHUB device that is
still linked to some sensor and the items in #1. If you have an old SmartHUB device that just
became recently unsupported, this is where many of you will be at. 
'Pros': All original sensor data will exist locally. You can also send data to
other providers.
'Cons': MyAcurite won't work unless you also have an Acurite Access. Other con
is that you'll have to run your old SmartHUB just to get pressure data off the
local sensor, so you could be running two hubs (SmartHUB and Acurite access)
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
$ sudo apt-get install weewx git cmake libusb-1.0-0-dev<
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
$ cd ~
$ sudo rtl_433 -G
$ wget -O weewx-sdr.zip https://github.com/matthewwall/weewx-sdr/archive/master.zip
$ sudo wee_extension --install weewx-sdr.zip
$ sudo wee_config --reconfigure --driver=user.sdr --no-prompt
# Run sdr.py to determine how to map your sensors. 
$ cd /usr/share/weewx
$ sudo PYTHONPATH=. python user/sdr.py --cmd="rtl_433 -M utc -F json -G"
</pre>
3. This command should output data that will allow you to map your sensor(s) to Weewx. It should look similar to this, but for more info, check [Weewx-sdr instructions](https://github.com/matthewwall/weewx-sdr). This will go in /etc/weewx/weewx.conf.
<pre>
# collect data from Acurite 5n1 sensor 0BFA and t/h sensor 24A4
[SDR]
    driver = user.sdr
    [[sensor_map]]
        windDir = wind_dir.0BFA.Acurite5n1Packet
        windSpeed = wind_speed.0BFA.Acurite5n1Packet
        outTemp = temperature.0BFA.Acurite5n1Packet
        outHumidity = humidity.0BFA.Acurite5n1Packet
        rain_total = rain_total.0BFA.Acurite5n1Packet
        inTemp = temperature.24A4.AcuriteTowerPacket
        inHumidity = humidity.24A4.AcuriteTowerPacket
</pre>
4. Hopefully you're getting sensor data now, go to http://your.ip.address/weewx
and verify that you are getting data from your sensors and check
/var/log/syslog if you're not. You won't get pressure data, so here's where
your SmartHUB comes in.
5. Configure your Rpi to be an [ethernet bridge](https://willhaley.com/blog/raspberry-pi-wifi-ethernet-bridge/). Again,
you need to be using Wifi to connect to your lan so you can use ethernet to
connect to your SmartHUB. The linked instructions worked perfect for my Pi 1
B+, and should work for newer devices. Don't connect your SmartHUB yet. 
6. Add an entry to /etc/hosts on your device, it should look similar to below,
but with the ip address (wireless lan IP) of your Pi - use ifconfig -a command
to get this if you're not sure:
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
Contents are based on [weewx-interceptor](https://github.com/matthewwall/weewx-interceptor) package
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
9. Create a /etc/apache2/conf-enabled/acurite.conf
<pre>
ScriptAlias /weatherstation/updateweatherstation /usr/lib/cgi-bin/myacurite
&lt;Directory "/usr/lib/cgi-bin"&gt;
    Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
    Order allow,deny
    Allow from all
Require all granted
&lt;/Directory&gt;
</pre>
10. Restart apache <pre> $ sudo /etc/init.d/apache2 restart</pre>
11. Copy pond.py (from this repo) to /usr/share/weewx/user and enable in /etc/weewx/weewx.conf
(this is based on [this](https://github.com/weewx/weewx/wiki/add-sensor)). 
<pre>
[Engine]
    [[Services]]
        data_services = user.pond.PondService
</pre>
12. Restart Weewx
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
doesn't really matter since the only data coming out of SmartHub that you care
about is the pressure that's coming from the hub itself. You're getting the
rest of the data via SDR).

What did I just do?
---
You now have a setup that:
1) Transmits data to Wunderground via Acurite Access and MyAcurite app works.
2) You have local weather data via WeeWx and pressure information (via your old SmartHUB). 
3) If you replace any of your gear, you simply link to Acurite Access, go
through the sdr script above and re-map the new sensor ID's.  
4) WeeWX can also submit to Wunderground and others and is much more flexible
than just sending data to MyAcurite. I'd also suggest you check out [this
skin](https://github.com/poblabs/weewx-belchertown).

Bugs/Contact Info
-----------------
Bug me on Twitter at [@brianwilson](http://twitter.com/brianwilson) or email me [here](http://cronological.com/comment.php?ref=bubba).
