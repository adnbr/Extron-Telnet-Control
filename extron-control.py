import sys
import telnetlib
import time
import getopt

if len(sys.argv) < 3:
    print "extron-control.py <ipaddress> on|off\n\n"
    print "eg. extron-control.py xx.xx.xx.xx on"
    quit()

HOST = sys.argv[1]
tn = telnetlib.Telnet(HOST)

# Look for the name "Extron Electronics" and the timestamp at the
# end of the welcome message. TODO: Concat regex into one string.
#
# Example message:
# (c) Copyright 2006, Extron Electronics, MLC 226 IP, V1.05, 60-600-00
# Wed, 09 Mar 2016 12:43:34
tn.expect([r"(Extron).*?(Electronics)(?:)"]);
tn.expect([r"((?:(?:[0-1][0-9])|(?:[2][0-3])|(?:[0-9])):(?:[0-5][0-9])(?::[0-5][0-9])?)"]);
print "\nConnected to Extron control at " + HOST

if sys.argv[2] == "on":
    # Simulate pressing the "Display On" button
    # and wait for the response
    tn.write('X1*44#\r\n')
    print tn.read_until("SwCmd*00z1", 1);

    # Because the Display On button doesn't always
    # turn on the display when emulated (depends on
    # programming) actually power on the display now
    # and wait for the display powering on status.
    tn.write('1P\r\n')
    tn.read_until("Pwr3", 1); # Pwr3 is "powering up"
    print "Status Pwr3. Powering on."
else:
    # Simulate pressing the "Display Off" button
    # and wait for the response
    tn.write('X2*44#\r\n')
    print tn.read_until("SwCmd*X1", 1);

    # Tell projector to turn off, wait for response.
    tn.write('0P\r\n')
    tn.read_until("Pwr2", 1); # Pwr2 is "powering down"
    print ("Status Pwr2. Powering off.")


tn.close()
