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

# Don't bother with regex-ing the telnet output from the Extron
# because the first string ends in a date and doesn't give a prompt.
# Unhelpful! Todo: Find a better 'until' string.
print tn.read_until("ThisWillNeverOccur", 1);

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
    print tn.read_until("Pwr3", 1); # Pwr3 is "powering up"
else:
    # Simulate pressing the "Display Off" button
    # and wait for the response
    tn.write('X2*44#\r\n')
    print tn.read_until("SwCmd*X1", 1);

    # Tell projector to turn off, wait for response.
    tn.write('0P\r\n')
    print tn.read_until("Pwr2", 1); # Pwr2 is "powering down"


tn.close()
