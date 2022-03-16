import sys
import mariadb
import time
import logging
from opcua import Client
from opcua.ua.uatypes import _split_list

logging.basicConfig(filename="opcuadb.log", 
					format='%(asctime)s %(message)s', 
					filemode='w') 
logger=logging.getLogger()
logger.setLevel(logging.INFO)

# Connect to SQL MariaDB Platform
try:
    conn = mariadb.connect(
        user="dbuser",
        password="dbpassword",
        host="aaa.bbb.ccc.ddd",
        port=3306,
        database="opcdb"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

opcrobot = 'robotname'
opcurl = 'opc.tcp://192.168.40.101:4840/OPC-SERVER/\n'
client = Client(opcurl)
client.connect()
print('Lettura dati', opcrobot,'\n','Indirizzo: ',opcurl,'\n')

while True:
    SysAnno = client.get_node("ns=2;s=Local HMI.Tags.Sys-Anno")
    AnnoGet = SysAnno.get_value()
    mese = client.get_node("ns=2;s=Local HMI.Tags.Sys-Mese")
    meseget = mese.get_value()
    giorno = client.get_node("ns=2;s=Local HMI.Tags.Sys-Giorno")
    giornoget = giorno.get_value()
    ora = client.get_node("ns=2;s=Local HMI.Tags.Sys-Ora")
    oraget = ora.get_value()
    minuti = client.get_node("ns=2;s=Local HMI.Tags.Sys-Minuti")
    minutiget = minuti.get_value()
    CurrentTimeOpc = client.get_node('i=2258')
    GetCurrentTimeOpc = CurrentTimeOpc.get_value()
    rd1 = client.get_node("ns=2;s=YASKAWA Robot Controller.Tags.RD1")
    rd1get = rd1.get_value()
    rd2 = client.get_node("ns=2;s=YASKAWA Robot Controller.Tags.RD2")
    rd2get = rd2.get_value()
    rd3 = client.get_node("ns=2;s=YASKAWA Robot Controller.Tags.RD3")
    rd3get = rd3.get_value()
    rd4 = client.get_node("ns=2;s=YASKAWA Robot Controller.Tags.RD4")
    rd4get = rd4.get_value()
    rd5 = client.get_node("ns=2;s=YASKAWA Robot Controller.Tags.RD5")
    rd5get = rd5.get_value()
    
#   Insert DataBase
    cursor = conn.cursor()
    query = 'INSERT INTO opctb (OpcRobot, OpcUrl, GetCurrentTimeOpc, oraget, AnnoGet, meseget, giornoget, Rd1, Rd2, Rd3, Rd4, Rd5) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    OpcData = [opcrobot, opcurl, GetCurrentTimeOpc, oraget, AnnoGet, meseget, giornoget, rd1get, rd2get, rd3get, rd4get, rd5get]
    cursor.execute(query,OpcData)
    conn.commit()

    print(opcrobot, opcurl, GetCurrentTimeOpc, oraget, AnnoGet, meseget, giornoget, rd1get, rd2get, rd3get, rd4get, rd5get)
    
#   print([GetCurrentTimeOpc], [rd4get])
    time.sleep(15)
   
