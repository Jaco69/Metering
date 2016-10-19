#!/usr/bin/env python
from __future__ import print_function 
from contextlib import closing
import serial
import time
import MySQLdb

def send(port, bytes, tr):
  """ sends an command to serial and reads and checks the echo
      port  - the open serial port
      bytes - the string to be send
      tr    - the responce time
  """
  #print("start send")  
  port.write(bytes)
  time.sleep(tr)
  echo = port.read(len(bytes))
  if (echo != bytes):
    print("echo is not same as send:", bytes, " vs ", echo)
  #print("end send")

def read_datablock():
  ACK = '\x06'
  STX = '\x02'
  ETX = '\x03'
  tr = 0.2
  debugtext = ""
  """ does all that's needed to get meter data from the meter device """ 
  try:
    try:
      IskraMT171=serial.Serial(port='/dev/ttyUSB0', baudrate=300, bytesize=7, parity='E', stopbits=1, timeout=1.5); # open port at specified speed
    except:
      print("Could not open serial port")
      return ""
    # 1 ->
    debugtext = "port open"
    time.sleep(tr)
    Request_message='/?!\r\n' # IEC 62056-21:2002(E) 6.3.1
    send(IskraMT171, Request_message, tr)
    # 2 <- 
    debugtext = "request message send"
    time.sleep(tr)
    try:
      Identification_message=IskraMT171.readline() # IEC 62056-21:2002(E) 6.3.2
    except:
      print("Could not read identification line")
      IskraMT171.close()
      return ""
    debugtext = "ID line read"
    if (len(Identification_message) < 1 or Identification_message[0] != '/'):
      print("no Identification message")
      IskraMT171.close()
      return ""
    if (len(Identification_message) < 7):
      print("Identification message to short")
      IskraMT171.close()
      return ""
    if (Identification_message[4].islower()):
      tr = 0.02
    manufacturers_ID = Identification_message[1:4]
    if (Identification_message[5] == '\\'):
      identification = Identification_message[7:-2]
    else:
      identification = Identification_message[5:-2]
    speed = Identification_message[4]
    #print("speed = ", speed)
    if (speed == "1"): new_baud_rate = 600
    elif (speed == "2"): new_baud_rate = 1200
    elif (speed == "3"): new_baud_rate = 2400
    elif (speed == "4"): new_baud_rate = 4800
    elif (speed == "5"): new_baud_rate = 9600
    elif (speed == "6"): new_baud_rate = 19200
    else:
      new_baud_rate = 300
      speed = "0"
    #print(manufacturers_ID, " ", identification, " speed=", speed)
    # 3 ->
    Acknowledgement_message=ACK + '0' + speed + '0\r\n' # IEC 62056-21:2002(E) 6.3.3
    try:
      send(IskraMT171, Acknowledgement_message, tr)
    except:
      print("Could not send acknowledgement message")
      IskraMT171.close()
      return ""
    debugtext = "ACK send"
    IskraMT171.baudrate=new_baud_rate
    time.sleep(tr)
    debugtext = "speed set"
    # 4 <-
    datablock = ""
    try:
      x = IskraMT171.read()
    except:
      print("Could not read STX")
      IskraMT171.close()
      return ""
    if (x == STX):
      debugtext = "STX found"
      try:
        x = IskraMT171.read()
      except:
        print("Could not read char after STX")
        IskraMT171.close()
        return ""
      BCC = 0
      while (x  != '!'):
        BCC = BCC ^ ord(x)
        datablock = datablock + x
        try:
          x = IskraMT171.read()
        except:
          print("Could not read char for datablock")
          IskraMT171.close()
          return ""
      debugtext = "! found"
      while (x  != ETX):
        BCC = BCC ^ ord(x) # ETX itself is part of block check
        try:
          x = IskraMT171.read()
        except:
          print("Could not read char")
          IskraMT171.close()
          return ""
      debugtext = "EXT found"
      BCC = BCC ^ ord(x)
      try:
        x = IskraMT171.read()   # x is now the Block Check Character
      except:
        print("Could not read block check")
        IskraMT171.close()
        return ""
      # last character is read, could close connection here
      debugtext = "all read"
      if (BCC != ord(x)): # received correctly?
        datablock = ""
        print("Block check not OK")
    else:
      print("No STX found")
    IskraMT171.close()
    return datablock
  except:
    print("Some error reading data")
    print(debugtext)
    if (IskraMT171.isOpen()):
      IskraMT171.close()
    return ""

def meter_data(datablock, map, header):
  """ takes a datablock as received from the meter and returns a list with requested meter data as set in map
      if header != 0 a list with data type and units is returned """
  line = []
  if datablock == "":
    return line
  ## initialise line
  for l in range(len(map)):
    if (header == 1):
      line.append(map[l][1])
    elif (map[l][0] == "time"):
      line.append(time.strftime("%Y-%m-%d %H:%M:%S"))
    else:
      line.append("")
  datasets = datablock.split('\n')
  for dataset in datasets:
    if (dataset != ""):
      x = dataset.split('(')
      address = x[0]
      x = x[1][:-2].split(' ') # the standard seems to have a '*' instead of ' ' here
      value = x[0]
      try:
        unit = '['+x[1]+']'
      except:
        unit = ""
      for l in range(len(map)):
        if (map[l][0] == address):
          if (header == 0):
            line[l] = value
          else:
            line[l] = map[l][1] + unit
          break;
  return line

filename = "meterdata.txt"

def output_to_file(line):
  with open(filename, "a") as f:
    print(line, file=f)

# output_to_database() state variables
oudt = int(time.time())/86400*86400
oudverbruikt = 0.0
oudgeleverd = 0.0
uurstart = oudt/3600*3600
uureind = uurstart + 3600

def insert(db, c, v, g):
  global uurstart
  # verbruikt
  #print(uurstart, "v =", v)
  #print(uurstart, "g =", g)
  if v >= 0:
    c.execute("INSERT INTO feed_1 (time, data) VALUES (%d, %f) ON DUPLICATE KEY UPDATE data = data + %f;" % (uurstart, v*1000, v*1000))   # Watt gemideld per uur
    c.execute("INSERT INTO feed_2 (time, data) VALUES (%d, %f) ON DUPLICATE KEY UPDATE data = data + %f;" % (int(uurstart)/86400*86400, v, v)) # kWh per dag
    c.execute("INSERT INTO feed_3 (time, data) VALUES (%d, %f) ON DUPLICATE KEY UPDATE data = data + %f;" % ((time.localtime(uurstart)).tm_year, v, v)) # kWh per jaar
  else:
    print(uurstart, "v =", v)
  #geleverd
  if g >= 0:
    c.execute("INSERT INTO feed_4 (time, data) VALUES (%d, %f) ON DUPLICATE KEY UPDATE data = data + %f;" % (uurstart, g*1000, g*1000))   # Watt gemideld per uur
    c.execute("INSERT INTO feed_5 (time, data) VALUES (%d, %f) ON DUPLICATE KEY UPDATE data = data + %f;" % (uurstart/86400*86400, g, g)) # kWh per dag
    c.execute("INSERT INTO feed_6 (time, data) VALUES (%d, %f) ON DUPLICATE KEY UPDATE data = data + %f;" % ((time.localtime(uurstart)).tm_year, g, g)) # kWh per jaar
  else:
    print(uurstart, "g =", g)

  # kopieer laatste waarden
  if v >= 0:
    c.execute("UPDATE feeds SET value = (SELECT data FROM feed_1 WHERE time = %d) WHERE id = 1;" % (uurstart)) # Watt gemideld per uur
    c.execute("UPDATE feeds SET value = (SELECT data FROM feed_2 WHERE time = %d) WHERE id = 2;" % (int(uurstart)/86400*86400)) # kWh per dag
    c.execute("UPDATE feeds SET value = (SELECT data FROM feed_3 WHERE time = %d) WHERE id = 3;" % ((time.localtime(uurstart)).tm_year)) # kWh per jaar
  if g >= 0:
    c.execute("UPDATE feeds SET value = (SELECT data FROM feed_4 WHERE time = %d) WHERE id = 4;" % (uurstart)) # Watt gemideld per uur
    c.execute("UPDATE feeds SET value = (SELECT data FROM feed_5 WHERE time = %d) WHERE id = 5;" % (int(uurstart)/86400*86400)) # kWh per dag
    c.execute("UPDATE feeds SET value = (SELECT data FROM feed_6 WHERE time = %d) WHERE id = 6;" % ((time.localtime(uurstart)).tm_year)) # kWh per jaar
 

def output_to_database(list):
  global oudt
  global oudverbruikt
  global oudgeleverd
  global uurstart
  global uureind
  t = time.mktime(time.strptime(list[t_index],"%Y-%m-%d %H:%M:%S"))
  try:
    v = float(list[v_index])
  except:
    print("\nNo value found at list[v_index], check map[].\n")
    v = -0.00000001
  try:
    g = float(list[g_index])
  except:
    print("\nNo value found at list[g_index], check map[].\n")
    g = -0.00000001
  try:
    with closing(MySQLdb.connect(db="emoncms", user="root", passwd="raspberry")) as db:
      with db as cursor:
        # gemiddeld Watt per uur
        while t > uureind:
          #het huidig vermogen loopt tot volgend uur, we kunnen het gemiddeld uurvermogen berekenen en opslaan
          if oudt > uurstart:
            insert(db, cursor, (v-oudverbruikt)*(uureind-oudt)/(t-oudt), (g-oudgeleverd)*(uureind-oudt)/(t-oudt))
          else:
            insert(db, cursor, (v-oudverbruikt)*(uureind-uurstart)/(t-oudt), (g-oudgeleverd)*(uureind-uurstart)/(t-oudt))
          #naar volgend uur
          uurstart = uureind
          uureind = uurstart + 3600
        #het huidig vermogen eindigd in dit uur, we kunnen bij de tijdelijke berekening optellen
        if oudt > uurstart:
          insert(db, cursor, v-oudverbruikt, g-oudgeleverd)
        else:
          insert(db, cursor, (v-oudverbruikt)*(t-uurstart)/(t-oudt), (g-oudgeleverd)*(t-uurstart)/(t-oudt))
        oudt = t
        oudverbruikt = v
        oudgeleverd = g
  except:
    print("Some error writing data to database")

    
map = [
  # The structure of the meter_data() output can be set with this variable 
  # first string on each line is the cosim adress of the data you want to safe or "time" to insert the time
  # the second string on each line is a description of the type of data belonging to the cosim address
  # the order of the lines sets the order of the meter_data() output
  # example
  # header: ['meter ID', 'datum & tijd', 'verbruik totaal[kWh]', 'verbruik tarief1[kWh]', 'verbruik tarief2[kWh]', 'terug totaal[kWh]', 'terug tarief1[kWh]', 'terug tarief2[kWh]']
  # data: ['12345678', '2013-02-08 10:08:41', '0054321', '0000000', '0054321', '0000000', '0000000', '0000000']
  ["1-0:0.0.0*255", "meter ID"],
  ["time", "datum & tijd"],
  ["1-0:1.8.0*255", "verbruikt totaal"],  # output_to_database has hardcoded v = float(list[2]) Change if table order changes!
  ["1-0:1.8.1*255", "verbruikt tarief1"],
  ["1-0:1.8.2*255", "verbruikt tarief2"],
  ["1-0:2.8.0*255", "geleverd totaal"],   # output_to_databasehas hardcoded g = float(list[5]) Change if table order changes!
  ["1-0:2.8.1*255", "geleverd tarief1"],
  ["1-0:2.8.2*255", "geleverd tarief2"]
]
t_index = 1 # map table index for time
v_index = 2 # map table index for verbruikt
g_index = 5 # map table index for geleverd
previous_datalist = []
datalist = meter_data(read_datablock() , map, 0) # reads meter for the first time
# reads old data from file
with open(filename) as f:
  for line in f:
    try:
      list = eval(line)
      if list[1].find("-") == 4: # skips header lines
        oudt = int(time.mktime(time.strptime(list[t_index],"%Y-%m-%d %H:%M:%S")))
        oudverbruikt = float(list[v_index])
        oudgeleverd = float(list[g_index])
    except:
      # Did once get this. Probably because of power disconnect and file not properly closed
      #   File "MT171.py", line 291, in <module>
      #     list = eval(line)
      # TypeError: expected string without null bytes
      print("Skipping line as it has some problems. File needs maintenance removing NULL bytes")
uurstart = oudt/3600*3600
uureind = uurstart + 3600
dag = uurstart/3600/24
print( "laaste tijd =", oudt, "laaste verbruikt =", oudverbruikt, "laatste geleverd =", oudgeleverd, "uurstart =", uurstart, "uureind =", uureind, "dag =", dag)

example_datablock = """0-0:C.1.0*255(12345678)
1-0:0.0.0*255(12345678)
1-0:0.2.0*255(V1.0)
1-0:1.8.0*255(0054321 kWh)
1-0:1.8.1*255(0000000 kWh)
1-0:1.8.2*255(0054321 kWh)
1-0:2.8.0*255(0000000 kWh)
1-0:2.8.1*255(0000000 kWh)
1-0:2.8.2*255(0000000 kWh)
FF(00000000)
"""
            
output_to_file(meter_data(example_datablock , map, 1)) # print a header line to file
             
while (1):
  if (datalist == []):
    print(time.strftime("%Y-%m-%d %H:%M:%S"), "No data received")
  elif (previous_datalist == [] or previous_datalist[v_index] != datalist[v_index] or previous_datalist[g_index] != datalist[g_index]):
    output_to_file(datalist)
    output_to_database(datalist)
    previous_datalist = datalist
  time.sleep(3.5) # minimum waiting time is 3 seconds, less and the meter doesn't return data 
  datalist = meter_data(read_datablock() , map, 0)
