import os
import csv
from pathlib import Path
import datetime
Path.cwd()
import pynmea2
now = datetime.datetime.now()
#print("Make sure there is no other File in the path except .nmea file only ")

class GPGSArec:
    def __init__(self, res):
        print("GPS DOP and active satellites\n")
        self.res=res
        d=res.split(',')
        if d[1]=='A':
            self.mode='Automatic, 3D/2D'
        elif d[1]=='M':
            self.mode='Manual, forced to operate in 2D or 3D'
        else:
            self.mode='Mode Not Identified'
        if d[2]=='1':
            self.view='Fix not available'
        elif d[2]=='2':
            self.view='2D'
        elif d[2]=='3':
            self.view='3D'
        else:
            self.view='NA'
        self.svid=d[3:15] # Space Vehicle SV ID
        self.pdop=d[15]
        self.hdop=d[16]
        self.vdop=d[17].split('*')[0]
        
class GPRMCrec:
    def __init__(self,res):
        print("Recommended minimum specific GPS/Transit data\n")
        self.res=res
        s=res.split(',')
        self.time=s[1][0:2]+':'+s[1][2:4]+':'+s[1][4:]+' UTC'
        if s[2]=='A':
            self.validity="Valid"
        elif s[2]=='V':
            self.validity="InValid"
        self.lat=s[3]#current Latitude
        self.latd=s[4]
        self.lon=s[5]
        self.lond=s[6]
        self.speed=s[7]
        self.tcourse=s[8]
        self.date=s[9][0:2]+'/'+s[9][2:4]+'/'+s[9][4:6]
        self.magVar=s[10]
        self.magVarDir=s[11].split('*')[0]
        
        
        
class readNmea():
    def __init__(self):
        en_pa = str(input("Kindly Enter path of files Example for Mac: /Users/codar/Desktop/ for Windows 'C:\\Users\\Al\\spam' Else 1 for Default path: "))
        pat = False
        if en_pa == '1':
            en_pa = "/Users/codar/Desktop/Kalpakkam_Interference_Issue/"  # default path
            path = en_pa
            os.chdir(path)
        else:
            #print("Entered else")
            while pat == False:
                #print("Entered while")
                try:
                    #print("Entered try")
                    win_dir = Path(en_pa)
                    win_dir.exists()
                    pat = True
                    os.chdir(en_pa)
                    path = en_pa
                except:
                    pat = False
                    #print("Entered Ezxcept")
                    en_pa = input(" Kindly Enter valid path: ")
                    continue
                
        def RmSpaceConvertFloat(x):
            return float(x.strip())


        def RmSpace(x):
            return x.strip()

        results = []
        # keep only files with extesnion .rdt
        results += [each for each in os.listdir(path) if each.endswith('.nmea')]
        for k in results:
            helloFile = open(path + k)
            helloContent = helloFile.readlines()
            StopCount = len(helloContent)
            for a in range(0, StopCount - 1):
                res = helloContent[a]
                if 'GPGGA' in res:
                    print(res)
                    msg=pynmea2.parse(res)
                    print("Time stamp: "+str(msg.timestamp)+" Lattitude: "+msg.lat+" Lattitude Direction: "+msg.lat_dir+" Longitude: "+msg.lon," Longitude direction: "+str(msg.lon_dir)+" GPS quality: "+str(msg.gps_qual)+" No of satellites: "+msg.num_sats+"\n")
                if 'GPGSA' in res:
                    print(res)
                    x=GPGSArec(res)
                    print("Mode: "+x.mode+" View: "+x.view+" IDs of SVs used in position fix: "+str(x.svid)+" PDOP (dilution of precision): "+x.pdop+" Horizontal dilution of precision(HDOP): "+x.hdop+" Vertical dilution of precision (VDOP): "+x.vdop+"\n")
                if 'GPRMC' in res:
                    print(res)
                    x=GPRMCrec(res)
                    print("Fix taken at: "+x.time+" Validity: "+x.validity+" Latitude: "+x.lat+" Latitude Direction "+x.latd+" Longitude: "+x.lon+" Longitude Direction: "+x.lond+" Speed in knots: "+x.speed+" Track angle in degrees True: "+x.tcourse+" Date: "+x.date+" Magnetic Variation: "+x.magVar+" Magnetic Variation Direction: "+x.magVarDir+"\n") 
                    

#$GPGGA,124632.122,5231.537,N,01320.203,E,1,12,1.0,0.0,M,0.0,M,,*6A
#$GPGSA,A,3,01,02,03,04,05,06,07,08,09,10,11,12,1.0,1.0,1.0*30
#$GPRMC,124633.122,A,5231.938,N,01324.385,E,2228.2,011.3,020622,000.0,W*48



            
