import dns.query
import dns.name
import sys
from datetime import datetime
import time

rootServers = ["198.41.0.4", "199.9.14.201", "192.33.4.12", "199.7.91.13", "192.203.230.10", "192.5.5.241",
               "192.112.36.4", "198.97.190.53", "192.36.148.17", "192.58.128.30", "193.0.14.129", "199.7.83.42",
               "202.12.27.33"]  # array of root servers

inputDomain = str(input("Enter a domain: "))  # once the program runs inputDomain will take the user input as the domain


def myDNSresolver(domain, ServerIP):
    queryRequest = dns.message.make_query(domain, "A")
    # use make_query function to make query for A times with the input domain
    responseQuery = dns.query.udp(queryRequest, ServerIP, timeout=3)
    # get response with the query I got from above, set timeout as 10 seconds
    while len(responseQuery.answer) == 0:  # check if any answer is found, continue until answer is found
        if len(responseQuery.additional) != 0:  # check if there are an additional
            for k in range(len(responseQuery.additional)):
                if responseQuery.additional[k].rdtype == 1:  # check if A type
                    responseQuery = dns.query.udp(queryRequest,
                                                  str(responseQuery.additional[k]).split()[4], timeout=3)
                    # get response with the next server IP
                    break
        elif len(responseQuery.authority) != 0:  # check if there is an authority
            for k in range(len(responseQuery.authority)):
                if responseQuery.authority[k].rdtype == 2:  # check if NS type
                    newServerIP = myDNSresolver(str(responseQuery.authority[k]).split()[4][:-1], ServerIP)
                    # get a new server ip with the domain
                    return myDNSresolver(domain, str(newServerIP).split()[4])
                    # return recursive call with new domain
    if responseQuery.answer[0].rdtype == 5:  # check if CNAME type
        return myDNSresolver(str(responseQuery.answer[0]).split()[4], ServerIP)
        # if CNAME type, then just return recursive call with new domain in the responseQuery
    else:
        return responseQuery.answer[0]  # return the answer.


file = open("mydig_output.txt", "w")  # open mydig_out.txt as write mode.
file.write(";; QUESTION SECTION:\n")  # write question section
requested = dns.message.make_query(inputDomain, "A")
file.write(str(requested.question[0]) + "\n\n")  # write domain and its type in the question section
file.write(";; ANSWER SECTION:\n") # write answer section

startTime = time.time() # measure start time
for i in range(len(rootServers)):
    try:
        server = rootServers[i]
        output = myDNSresolver(inputDomain, rootServers[i])
        break
    except Exception as e:  # if error occured, move to next
        if i == len(rootServers) - 1:  # If I cannot find at all from given root server
            file.write("Please check your domain. There seems to be a problem with your input domain")
            file.close()
            sys.exit()
        else:
            continue

file.write(str(inputDomain) + ".\t" + str(output).split(' ', 1)[1] + "\n")
endTime = time.time()
file.write("\n;; Query time: " + str(int((endTime - startTime) * 1000)) + " ms \n")  # write query time
file.write(";; SERVER: " + server + "\n")  # write server
file.write(";; WHEN: " + datetime.now().strftime('%A')[:3] + datetime.now().strftime(
    ' %B %d %H:%M:%S %Y\n'))  # write date and time
print("Successfully created txt file. ")
file.close()  # file close

sys.exit()
