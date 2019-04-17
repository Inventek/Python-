#-------------------------------------------------------------------------------
# Name:        TCP/UDP Client Demo
# Purpose:     To illistrait how to use the TCP/UDP cLient IWIN AT commands to
#              tramsit and receive data.
#
# Author:      sep
#
# Created:     27/05/2014
# Copyright:   (c) Inventek Systems, LLC. 2014
#
# Name:        INVENTEK WIRELESS INTEROPERABILITY NETWORK (IWIN), AT Command Software
# Purpose:     To provide Inventek customers Python scripts illustrating how to
#              use the IWIN AT Command Software.
#
#------------------------------------------------------------------------------
#LICENSE:
#   THE IWIN PROGRAM IS FREE SOFTWARE FOR INVENTEK CUSTOMERS ONLY.
#   INVENTEK SYSTEMS RETAINS ALL OWNERSHIP AND INTELLECTUAL PROPERTY RIGHTS
#   IN THE IWIN CODE ACCOMPANYING THIS MESSAGE AND IN ALL DERIVATIVES HERETO.
#   USER MAY USE THE IWIN CODE, AND ANY DERIVATIVES CREATED BY ANY PERSON OR
#   ENTITY BY OR ON USER?S BEHALF, EXCLUSIVELY WITH INVENTEK'S PROPRIETARY
#   PRODUCTS.
#
#   USER AGREES THAT USER IS SOLELY RESPONSIBLE FOR TESTING THE CODE AND
#   DETERMINING IT?S SUITABILITY.  INVENTEK HAS NO OBLIGATION TO MODIFY, TEST,
#   CERTIFY, OR SUPPORT THE CODE.
#
#   USER ACCEPTANCE AND/OR USE OF THE IWIN CODE CONSTITUTES AGREEMENT TO THE
#   TERMS AND CONDITIONS OF THIS NOTICE. IWIN CAN BE REDISTRIBUTED AND/OR
#   MODIFIED BY INVENTEK CUSTOMERS ONLY AND UNDER THE TERMS OF THE GNU GENERAL
#   PUBLIC LICENSE AS PUBLISHED BY THE FREE SOFTWARE FOUNDATION, EITHER VERSION
#   3 OF THE LICENSE, OR (AT USER?S OPTION) ANY LATER VERSION.
#
#   THIS PROGRAM IS DISTRIBUTED IN THE HOPE THAT IT WILL BE USEFUL, BUT WITHOUT
#   ANY WARRANTY; WITHOUT EVEN THE IMPLIED WARRANTY OF MERCHANTABILITY OR FITNESS
#   FOR A PARTICULAR PURPOSE.  REFERENCE THE GNU GENERAL PUBLIC LICENSE FOR MORE
#   DETAILS.
#
#   CODE ACCOMPANYING THIS MESSAGE IS SUPPLIED BY INVENTEK "AS IS".  NO WARRANTIES,
#   WHETHER EXPRESSED, IMPLIED OR STATUTORY, INCLUDING, BUT NOT LIMITED TO,
#   IMPLIED WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY AND FITNESS FOR A
#   PARTICULAR PURPOSE APPLY TO THIS CODE, IT?S INTERACTION WITH INVENTEK 'S
#   PRODUCTS, COMBINATION WITH ANY OTHER PRODUCTS, OR USE IN ANY APPLICATION.
#
#   USER ACKNOWLEDGES AND AGREES THAT, IN NO EVENT, SHALL INVENTEK BE LIABLE,
#   WHETHER IN CONTRACT, WARRANTY, TORT (INCLUDING NEGLIGENCE OR BREACH OF
#   STATUTORY DUTY), STRICT LIABILITY, INDEMNITY, CONTRIBUTION, OR OTHERWISE,
#   FOR ANY INDIRECT, SPECIAL, PUNITIVE, EXEMPLARY, INCIDENTAL OR CONSEQUENTIAL
#   LOSS, DAMAGE, FOR COST OR EXPENSE OF ANY KIND WHATSOEVER RELATED TO THE CODE,
#   HOWSOEVER CAUSED, EVEN IF INVENTEK HAS BEEN ADVISED OF THE POSSIBILITY OR THE
#   DAMAGES ARE FORESEEABLE.  TO THE FULLEST EXTENT ALLOWABLE BY LAW, INVENTEK 'S
#   TOTAL LIABILITY ON ALL CLAIMS IN ANY WAY RELATED TO THIS CODE, SHALL NOT
#   EXCEED THE PRICE PAID DIRECTLY TO INVENTEK SPECIFICALLY TO HAVE THIS CODE
#   DEVELOPED.
#
#   USER SHOULD HAVE RECEIVED A COPY OF THE GNU GENERAL PUBLIC LICENSE ALONG
#   WITH THIS PROGRAM. IF NOT, SEE <HTTP://WWW.GNU.ORG/LICENSES/>.
#-------------------------------------------------------------------------------
#
# Version:      0.0         sep         20140527    Intial release
#               0.1         sep         20140613    Added Usage instructiuons
#               0.2         sep         20140801    Added varirables to make setup easier
#               0.3         sep         20140912    Added "AD" Direct Mode SoftAP
#               0.4         sep         20141009    Correct
#               0.5         sep         20150123    Added Server mode, Secure Soft AP
#
# Usage:        1.  Set useSoftAP to 1 to use SoftAP for Configuration or to
#                   0 to configure manually (see Join Network section)
#               2.  Set the Protocol and Remote IP address (see Setup and Start
#                   TCP Client section)
#               3.  Determine if your server will echo back what it has been sent?
#                   Reccommend: http://www.hw-group.com/products/hercules/index_en.html
#                   The TCP and UDP servers can be set to echo back what they receive
#                   Set serverEcho to 1 if echoing, O if not.
#                   For the highest throughput please when using Hercules right click
#                   in the "Receive data" and select "Hide Receive Data"
#               4.  Plug in a EVK board (Please note will have needed to install
#                   drivers for the board using the eS-WiFi Demo software)
#               5.  Run the script
#
#-------------------------------------------------------------------------------
import math, sys, serial, serial.tools.list_ports, time, binascii

#Quiet mode, 0 = Quiet, 1 = Verbose(See all AT commands)
quiet = 0

#Send timeout
timeout = 10

#Show Hex data, 0 = Don't show, 1 = Show
showhex = 0

#Send a command to a eS-WiFi module and wait for prompt("\r\n> ") responce
def sendCMDBlocking(serPort,cmd):
    rcvString =""

    #Send Command
    if (quiet == 1):
        sys.stdout.write(cmd)
    serPort.write(cmd + '\r')

    st = time.time()                    #Get time

    #read until "\r\n> " received
    found = 0
    while found != 1:
        for c in serPort.read():
            rcvString += c
            if  '\r\n> ' in rcvString:
                found = 1
            #Endif
        #End for

        #Check for timeout
        if (time.time() - st) > timeout:
            return '-1'                 #Timeout error
        #Endif
    #End while

    #Show responce
    if (quiet == 1):
        if ('\0' in rcvString[2:(len(rcvString)-8)]):
            print rcvString[:1]
            print binascii.hexlify(rcvString[2:(len(rcvString)-8)])
            print rcvString[len(rcvString)-6:]
        else:
            sys.stdout.write(rcvString)
        #End if
    #End if

    #Get payload if OK responce
    if 'OK\r\n> ' in rcvString:
        rcvString=rcvString[2:(len(rcvString)-8)]
    #Endif

    #Return payload or Error
    return rcvString


#Send data to a eS-WiFi module and wait for prompt("\r\n> ") responce
#   Using a byte array with the S3 command embedded in array
#   e.g. S3=100\r<100 bytes of data>
def sendDataBlocking(serPort,data):
    rcvString =""

    #Send Command
    if (quiet == 1):
        #sys.stdout.write(data)
        if ('S0' in data):
            print(str(data[0:3]))
            if (showhex == 1): print binascii.hexlify(data[4:len(data)])
        #End if
        if ('S3' in data):
            tmp = str(data[:8])
            end = tmp.find('\r')
            print(data[:end])
            if (showhex ==1): print binascii.hexlify(data[end+1:len(data)])
        #end if
    #End if
    serPort.write(data)

    st = time.time()                    #Get time

    #read until "\r\n> " received
    found = 0
    while found != 1:
        for c in serPort.read():
            rcvString += c
            if  '\r\n> ' in rcvString:
                found = 1
            #Endif
        #End for

        #Check for timeout
        if (time.time() - st) > timeout:
            return '-1'                 #Timeout error
        #Endif
    #End while

    #Show responce
    if (quiet == 1):
        sys.stdout.write(rcvString[2:])

    #Get payload if OK responce
    if 'OK\r\n> ' in rcvString:
        rcvString=rcvString[2:(len(rcvString)-8)]
    #Endif

    #Return payload or Error
    return rcvString

#Send CMD and wait for responce, waiting nsec seconds before timing out
def sendCMDWait(serPort,cmd,responce,nsec):
    rcvString =""

    #Send Command
    if (quiet == 1):
        sys.stdout.write(cmd)
    serPort.write(cmd + '\r')

    st = time.time()                    #Get time

    #Check each message recieved for responce
    found = 0
    while found != 1:

        #read until "\r\n> " received
        found0 = 0
        while found0 != 1:
            for c in serPort.read():
                rcvString += c
                #if (quiet == 1):
                sys.stdout.write(c)
                if  "\r\n> " in rcvString:
                    found0 = 1
                #Endif
            #End for

            #Check for timeout
            if (time.time() - st) > nsec:
                return '-1'                 #Timeout error
            #Endif
        #End while

        #Show responce
        if (quiet == 1):
            sys.stdout.write(rcvString)

        #Check for responce
        if  responce in rcvString:
            found = 1
        else:
            rcvString = ""                  #Clear string
        #End if
    #End while

    #Show responce
    if (quiet == 1):
        sys.stdout.write(rcvString)

    #Get payload if OK responce
    if 'OK\r\n> ' in rcvString:
        rcvString=rcvString[2:(len(rcvString)-8)]
    #Endif

    #Return payload or Error
    return rcvString

#Send wait for responce, waiting nsec seconds before timing out
def waitResponce(serPort,responce,term,nsec):
    rcvString =""
    serPort.timeout = 10

    st = time.time()                    #Get time

    #Check each message recieved for responce
    found = 0
    while found != 1:

        #read until termination received
        found0 = 0
        while found0 != 1:
            for c in serPort.read():
                rcvString += c
                #if (quiet == 1):
                #    sys.stdout.write(c)
                if  term in rcvString:
                    found0 = 1
                #Endif
            #End for

            #Check for timeout
            if (time.time() - st) > nsec:
                return '-1'                 #Timeout error
            #Endif
        #End while

        #Check for responce
        if  responce in rcvString:
            found = 1
        else:
            rcvString = ""                  #Clear string
        #End if
    #End while

    #Show responce
    if (quiet == 1):
        sys.stdout.write(rcvString)

    #Return payload or Error
    return rcvString


#Search COM port for and eS-WiFi module
def findModule(timeout):
    rcvString =""

    #Get ports
    portList = list(serial.tools.list_ports.comports())
    #print(portList)

    #Search for module
    for index, openPort in enumerate(portList):

        #Serial Port Setup
        port = portList[index][0]
        baud = 115200
        serPort = serial.Serial(port,baud)
        serPort.timeout = 10

        serPort.write('\r')                 #Send CR

        st = time.time()                    #Get time

        #read until "\r\n> " received
        found = 0
        while found != 1:
            for c in serPort.read():
                rcvString += c
                if  '\r\n> ' in rcvString:
                    found = 1
                #Endif
            #End for

            #Check for timeout
            if (time.time() - st) > timeout:
                return '-1'                 #Timeout error
            #Endif
        #End while

        #Try to get info
        rcv = sendCMDBlocking(serPort,"I?")

        #Close serial port
        serPort.close()

        #Found?
        if (found == 1):
            #print("Port = " + port)
            if "ISM4" in rcv:
                #print(rcv)
                return port
            #Endif
        #End if
    #End for
    return -1

#Application
def main():

    #Redirect std err to std out
    sys.stderr = sys.stdout

    #Start Application
    print( "**** eS-WiFi TCP/UDP Client/Server Demo ****" )

    #Serial Port Setup
    port = findModule(10)
    if (port == -1):
        print( "Failed to find an eS-WiFi module!")
        sys.exit(-1)
    #End if
    baud = 115200
    ser = serial.Serial(port,baud)
    ser.timeout = 10

    #Get Firmware information
    #rcv = sendCMDBlocking(ser,"I?")

    #Setup ---------------------------------------------------------------------
    bd = 115200                     #Default Buad Rate

    #Choose baud rate for demo (uncomment choice)
    chgBaudRate = 1                 #Enable change baud rate, 0=Disable, 1=Enable
    #bd = 115200
    #bd = 460800
    #bd = 921600
    #bd = 1152000
    #bd = 1382400
    bd = 1843200
    #bd = 2073600
    #bd = 3916800

    mCnt = 10000000                 #Monitoring Count
    nob = 1152                      #Number of bytes to send/receive
                                    #456 * 1152 =   525,312 (~512K)
    cycle_delay = 0.0               #Delay between sends in seconds
    display_count = 100             #Print modulus

    SOCKET = "0"                    #Select Socket 0-3
    PROTOCOL="0"                    #TCP=0, UDP=1, UDP-Lite=2 TCP-SSL=3(Hercules doesn't support)

    useSoftAP = 0                   #Join using, 0 = Cx commands, 1 = A0 (SoftAP), 2 = AD Direct Mode (SoftAP)
    useSecureAP = 1                 #Use a secure softAP
    secureType = "4"                #Security Type: 0=Open, 2=WPA, 3=WPA2-AES, 4=WPA2-MIXED
    pswdAP = "ism12345"             #Password

    #Local Network
    SSID = "UVXL8"                   #SSID of AP
    PSWD = "ThisIsMyWorkNetwork"               #Password of AP
    SEC="4"                         #Security type of AP: 0-Open, 1-WEP, 2-WPA, 3-WPA2-AES, 4-WPA2-Mixed
    DHCP="1"                        #Get IP address for DHCP, 0-No, 1-Yes

    client_server = 0               #Client=0, Server=1
    #Client Mode
    remoteIP = "10.16.190.139"     #Remote Server IP address (use 192.168.10.100 with AD Direct Mode)
    remotePort = "8002"             #Remote TCP port
    #Server Mode
    clientIP = "192.168.3.41"         #Client IP address, use to validate sever accept

    serverEcho = 1                  #Server is going to echo data back, 0=No, 1=Yes
    printData = 0                   #Print send and receive data, 0=No, 1=Yes
    passfail = 0                    #Pass/Fail flag
   #---------------------------------------------------------------------------

    monitorCount = 0            #Monitor counter

    if chgBaudRate == 1:
        rcv = sendCMDBlocking(ser, "U2=" + str(bd))     #Set Baud
        ser.write("U0\r")                               #Start
        time.sleep(.1)                                  #Wait 100ms
        ser.close()                                     #Close
        ser = serial.Serial(port,bd)                    #Reopen
        rcv = sendCMDBlocking(ser, "U?")                #UART Info
        print ""
        print( "Communications: " + ser.portstr + "@" + str(bd))
    else:
        print ""
        print( "Communications: " + ser.portstr + "@" + str(baud))
    #End if
    print( "Packet Size:    " + str(nob) + " bytes")
    print( "" )


    #Configure LEDs
    rcv = sendCMDBlocking(ser, "G4=3,1")        #Red LED
    rcv = sendCMDBlocking(ser, "G4=4,1")        #Green LED

    #Green - OFF, RED - OFF
    rcv = sendCMDBlocking(ser, "G3=0,1,0")      #Red LED
    rcv = sendCMDBlocking(ser, "G3=1,1,0")      #Green LED


    #Setup data
    data = bytearray("S3=" + str(nob) + "\r")
    cmpData = bytearray()
    for i in range(0, nob):
        data.append(255 - (i % 0x100))
        cmpData.append(255 - (i % 0x100))
    #End for


    #Join Network
    if (useSoftAP == 0):
        rcv = sendCMDBlocking(ser, "CS")                    #Is connected?
        if (rcv == '1'):
            rcv = sendCMDBlocking(ser, "CD")                #Dis-connected
        #End if

        rcv = sendCMDBlocking(ser, "C1="+SSID)              #Set SSID
        rcv = sendCMDBlocking(ser, "C2="+PSWD)              #Set Password
        rcv = sendCMDBlocking(ser, "C3="+SEC)               #Security Type: 0-Open, 1-WEP, 2-WPA, 3-WPA2-AES, 4-WPA2-Mixed
        rcv = sendCMDBlocking(ser, "C4="+DHCP)              #Use DHCP

        #Get start time
        st = time.time()

        #Join
        rcv = sendCMDBlocking(ser, "C0")                    #Join network
        if (rcv != '-1'):
            if "ERROR" in rcv:                              #Check for error
                print( "Join failed to connect to network\r\n> ")
                sys.exit(-1)
            else:
                print( "Time: " + ("%012.3F" % (time.time()-st)) + " Joining: " + rcv[10:] )
            #End if
        else:
            print( "Joined timed out" )
            sys.exit(-1)
        #End if

    elif (useSoftAP == 2):
        #Setup SoftAP, 'AD' mode
        if (client_server == 0):
            rcv = sendCMDBlocking(ser, "AS=1,CLIENT_DEMO")      #Set SoftAP SSID
        else:
            rcv = sendCMDBlocking(ser, "AS=1,SERVER_DEMO")      #Set SoftAP SSID
            #rcv = sendCMDBlocking(ser, "AS=1,TEST_DEMO")      #Set SoftAP SSID
        #Endif

        if (useSecureAP == 1):
            rcv = sendCMDBlocking(ser, "A1=" + secureType)      #Set SoftAP security type
            rcv = sendCMDBlocking(ser, "A2=" + pswdAP)          #Set SoftAP password
        #Endif

        rcv = sendCMDBlocking(ser, "AL=48")                     #Set SoftAP lease time (255 = Infinite)

        rcv = sendCMDBlocking(ser, "Z5")                        #Get MAC address
        print ""

        if (client_server == 0):
            print( "**** Starting Direct Access Point, please join CLIENT_DEMO_" + rcv.replace(':','') + " ****" )
        else:
            print( "**** Starting Direct Access Point, please join SERVER_DEMO_" + rcv.replace(':','') + " ****" )
        #Endif

        rcv = sendCMDBlocking(ser, "AD")                        #Start SoftAp in Direct mode
        rcv = waitResponce(ser,clientIP,"\r\n> ",1000)          #Wait a connect
        time.sleep(1)                                           #Wait a few secs for PC get completely finished

    else:
        #Use SoftAP, 'A0' mode
        rcv = sendCMDBlocking(ser, "CS")                        #Is connected?
        if (rcv == '1'):
            rcv = sendCMDBlocking(ser, "CD")                    #Dis-connected

        rcv = sendCMDBlocking(ser, "AL=0")                      #Set SoftAP lease time (0=30min, 1-254 hr, 255 = Infinite)

        #SoftAP
        rcv = sendCMDBlocking(ser, "Z5")                        #Get MAC address
        if (client_server == 0):
            print( "Starting Configuration Access Point, look for CLIENT_DEMO_" + rcv )
        else:
            print( "Starting Configuration Access Point, look for SERVER_DEMO_" + rcv )
        #Endif

        #Setup SoftAP
        if (client_server == 0):
            rcv = sendCMDBlocking(ser, "AS=1,CLIENT_DEMO")      #Set SoftAP SSID
        else:
            rcv = sendCMDBlocking(ser, "AS=1,SERVER_DEMO")      #Set SoftAP SSID
        #Endif

        #Start and wait for Join message
        rcv = sendCMDWait(ser, "A0","[JOIN   ]",300)            #Start SoftAP
        if (rcv != '-1'):                                       #Check for timeout
            if "ERROR" in rcv:                                  #Check for error
                print( "Join failed to connect to network")
                sys.exit(-1)
            else:
                print( "Time: " + ("%012.3F" % (time.time()-st)) + " Joining: " + rcv[10:] )
            #End if
        else:
            print( "Timeout, failed to connect to a network")
            serPort.write(ctrlQ)                                #Send Quit
            sys.exit(-1)
        #End if
    #End if

    #Disable Async Assign Messages
    #rcv = sendCMDBlocking(ser, "MS=1")                  #0=Disable, 1=Enable

    #Setup and Start Client or Server
    rcv = sendCMDBlocking(ser, "P0="+SOCKET)            #Select socket
    rcv = sendCMDBlocking(ser, "P1="+PROTOCOL)          #TCP/TCP-SSL

    if (client_server == 0):
        rcv = sendCMDBlocking(ser, "P3="+remoteIP)      #Remote IP
        rcv = sendCMDBlocking(ser, "P4="+remotePort)    #Remote Port
    else:
        rcv = sendCMDBlocking(ser, "P2="+remotePort)    #Local Port
    #Endif

    if ((PROTOCOL == 0) or (PROTOCOL == 3)):
        rcv = sendCMDBlocking(ser, "PK=1,300")         #TCP Keep-Alive(ms)
    #Endif

    #TCP-SSL
    if (PROTOCOL == 3):
        rcv = sendCMDBlocking(ser, "P9=0")              #0-No cert validation, 1-Optional, 2-Required
    #Endif

    if (client_server == 0):
        rcv = sendCMDBlocking(ser, "P6=1")              #Start Client
        if (rcv == '-1'):                               #Check for timeout
            if "ERROR" in rcv:                          #Check for error
                print( "Failed to connect to server")
                sys.exit(-1)
            #End if
        #End if
    else:
        print ""
        print( "**** Starting Sever on "+remotePort + " ****")
        rcv = sendCMDWait(ser, "P5=1",clientIP,300)     #Start Server
        if (rcv == '-1'):                               #Check for timeout
            if "ERROR" in rcv:                          #Check for error
                print( "Client failed to connect")
                sys.exit(-1)
            #End if
        #End if
    #Endif

    #rcv = sendCMDBlocking(ser, "R2=5000")           #Read timeout

    #Get start time
    print ""
    print( "**** Sending  ****" )
    st = time.time()

    #Reporting Loop
    while monitorCount < mCnt:

        if (quiet == 0):
            if (((monitorCount + 1) % display_count) == 0):
                seq=(monitorCount + 1)*nob
                print(str(monitorCount + 1) + "(" + str(seq) +"):")  #Count(Byte Count)
            #Endif
        else:
            seq=(monitorCount + 1)*nob
            print(str(monitorCount + 1) + "(" + str(seq) +"):")  #Count(Byte Count)
        #Endif

        rcv0 = sendDataBlocking(ser, data)                  #Send data
        if rcv0 == "-1":
            break;
        #Endif

        if serverEcho == 1:
            rcv1 = bytearray( sendCMDBlocking(ser, "R0") )  #Read echoed data

            if printData == 1:
                print ("Sent Data:")
                print ''.join('{:02x}'.format(x) for x in cmpData)
                print ("Received Data:")
                print ''.join('{:02x}'.format(x) for x in rcv1)
            #End if

            if cmpData != rcv1:
                print( "**** " +str(monitorCount + 1) + " Failed Data Mis-match ****")
                passfail = 1
            else:
                print( "**** " +str(monitorCount + 1) + " Passed ****")
            #End if
        #End if

        #Use to add delay to loop in seconds
        if(cycle_delay > 0):
            time.sleep(cycle_delay)
        #Endif

        monitorCount += 1                       #Monitor counter
    #End while

    #Get end time
    et = time.time()
    print ""
    print( "**** Complete ****" )

    if (client_server == 0):
        rcv = sendCMDBlocking(ser, "P6=0")       #Stop Client
    else:
        rcv = sendCMDBlocking(ser, "P5=0")       #Stop Server
    #Endif

    #Leave Network
    if (useSoftAP == 1):
        rcv = sendCMDBlocking(ser, "CD")         #Leave network
    elif (useSoftAP == 2):
        rcv = sendCMDBlocking(ser, "AE")         #Shutdown SoftAP
    #End if

    if serverEcho == 1:
        #Display results on LEDs: Green - Passed, Red - Failed
        if (passfail == 0):
            #Green - ON, RED - OFF
            rcv = sendCMDBlocking(ser, "G3=0,1,0")      #Red LED
            rcv = sendCMDBlocking(ser, "G3=1,1,1")      #Green LED
            print ""
            print "**** PASSED ****"
        else:
            #Green - OFF, RED - ON
            rcv = sendCMDBlocking(ser, "G3=0,1,1")      #Red LED
            rcv = sendCMDBlocking(ser, "G3=1,1,0")      #Green LED
            print ""
            print "**** FAILED ****"
        #End if
    #End if

    #Statistics
    print( "" )
    print( "Summary:" )
    print( "Total time(sec)      = " + str(et-st))
    print( "Total Packets        = " + str(monitorCount))
    print( "Ave time(sec)/packet = " + str((et-st)/monitorCount))
    print( "Total bytes TX       = " + str(monitorCount * nob))
    if serverEcho == 1:
        print( "Total bytes RX       = " + str(monitorCount * nob))
        nob = nob * 2
    #End if
    print( "Total bytes/sec      = " + str( (monitorCount * nob) / (et-st) ) )
    print( "Total bits/sec       = " + str( ((monitorCount * nob) / (et-st)) * 8 ) )


    #Reset Baud rate
    if chgBaudRate == 1:
        bd = 115200
        rcv = sendCMDBlocking(ser, "U2=" + str(bd))         #Set Baud
        ser.write("U0\r")                                   #Start
        time.sleep(.1)                                      #Wait 100ms
        ser.close()                                         #Close
        ser = serial.Serial(port,bd)                        #Reopen
        rcv = sendCMDBlocking(ser, "U?")                    #UART Info
        #print(rcv)
    #End if

    #Close serial port
    ser.close()

if __name__ == '__main__':
    sys.exit(main())

