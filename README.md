# dig_command
custom-made dig command based on Python that allows you to get A and NS types of DNS name servers of the input domain.

READ ME
“mydig.py” is implemented as a “dig”-like tool. Once you run the
program, it lets the user enter a domain as an input, and it
resolves the domain name to ip addresses. This is done by
contacting the given 25 root servers. I have created a function
called myDNSresolver, which requests and receives queries with
the input domain and one of the root servers’ IP address. The
external library used in this method is dnspython - specifically
dns.name and dns.query. I have also imported sys, time, and
datetime to write other details such as query time and date time
onto the output text file.

HOW TO USE
Once you run the program on either terminal or the IDE you are
using, it will print a line saying “Enter a domain: “. You can
then enter any domain you want and if the user domain input is
valid, it will write onto mydig_output.txt the resolved results
of the method. This program requires installation of dnspython
and might require usage of VPN if you are using Stonybrook
University’s server.
