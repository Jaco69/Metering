from __future__ import print_function 
import time
import MySQLdb
#import httplib

def insert(db, c, v, g):
  global uurstart
  # verbruikt
  print(uurstart, "v =", v)
  print(uurstart, "g =", g)
  if v >= 0:
    c.execute("INSERT INTO feed_1 (time, data) VALUES (%d, %f) ON DUPLICATE KEY UPDATE data = data + %f;" % (uurstart, v*1000, v*1000))   # Watt gemideld per uur
    c.execute("INSERT INTO feed_2 (time, data) VALUES (%d, %f) ON DUPLICATE KEY UPDATE data = data + %f;" % (uurstart/86400*86400, v, v)) # kWh per dag
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
  db.commit()

t_index = 1 # map table index for time
v_index = 2 # map table index for verbruikt
g_index = 5 # map table index for geleverd
db = MySQLdb.connect(db="emoncms", user="root", passwd="raspberry")
cursor = db.cursor()
#akey = "7010d41ba88e410f5929b9a9a6c6c596"
oldt = 0
oldv = 0
oldg = 0
inputfile = "meterdata.txt"
with open(inputfile) as f:
  for line in f:
    list = eval(line)
    if list[t_index].find("-") == 4:
      t = time.mktime(time.strptime(list[1],"%Y-%m-%d %H:%M:%S"))
      v = float(list[v_index])
      g = float(list[g_index])
      if v != oldv or g != oldg:
        #conn = httplib.HTTPConnection("localhost")
        #print("/emoncms/input/post?apikey=%s&time=%d&node=1&json={Meterdata:%d}" % (akey, t, int(v)))
        #conn.request("GET", "/emoncms/input/post?apikey=%s&time=%d&node=1&json={Meterdata:%d}" % (akey, t, int(v)))
        #response = conn.getresponse()
        #conn.close()
        #time.sleep(1)
        #print(t, v)
        if oldt == 0:
          uurstart = (int(t)/3600)*3600
          uureind = uurstart + 3600
          dag = uurstart/3600/24
        else:
          # gemiddeld Watt per uur
          while t > uureind:
            #het huidig vermogen loopt tot volgend uur, we kunnen het gemiddeld uurvermogen berekenen en opslaan
            if oldt > uurstart:
              #print("uur", (uurstart - 1360368000)/3600, "+=", "(v-oldv)*(uureind-oldt)/(t-oldt)*1000", (v-oldv), "*", (uureind-oldt), "/", (t-oldt), "* 1000 =", (v-oldv)*(uureind-oldt)/(t-oldt)*1000, "\nuur", (uurstart - 1360368000)/3600, "==", uurvermogen)
              insert(db, cursor, (v-oldv)*(uureind-oldt)/(t-oldt), (g-oldg)*(uureind-oldt)/(t-oldt))
            else:
              #print("uur", (uurstart - 1360368000)/3600, "+=", vermogen, "\nuur", (uurstart - 1360368000)/3600, "==", uurvermogen)
              insert(db, cursor, (v-oldv)*(uureind-uurstart)/(t-oldt), (g-oldg)*(uureind-uurstart)/(t-oldt))
            #naar volgend uur
            uurstart = uureind
            uureind = uurstart + 3600
            uurvermogen = 0
          #het huidig vermogen eindigd in dit uur, we kunnen bij de tijdelijke berekening optellen
          if oldt > uurstart:
            insert(db, cursor, v-oldv, g-oldg)
            #print("uur", (uurstart - 1360368000)/3600, "+=", "vermogen*(t-oldt)/3600", vermogen*(t-oldt)/3600)
          else:
            insert(db, cursor, (v-oldv)*(t-uurstart)/(t-oldt), (g-oldg)*(t-uurstart)/(t-oldt))
            #print("uur", (uurstart - 1360368000)/3600, "+=", "(v-oldv)*(t-uurstart)/(t-oldt)*1000", (v-oldv), "*", (t-uurstart), "/", (t-oldt), "* 1000 =", (v-oldv)*(t-uurstart)/(t-oldt)*1000)
          
        oldt = t
        oldv = v
        oldg = g
cursor.close()
db.close()
