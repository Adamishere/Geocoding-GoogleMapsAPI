import os
import requests as r
import pandas as pd

#Set Workspace
os.chdir("")

#API Key #DO NOT SHARE
geo_key = "[INSERT YOUR OWN API KEY HERE"
#Google Geocode settings:
#To Return Address from Coordinates
geo_request = "https://maps.googleapis.com/maps/api/geocode/json?address="
#Provided

#############################################
#Update these parameters:
#############################################

#Location of file to import. Default CSV format only
in_file_location = "INPUT.csv"
out_file_location = "OUTPUT.txt"

#Variable that contains the geocode lookup information
location_name   = "MY_ADDRESS"
#Unique ID to track and merge new geocode data
id_name         = "MY_ID"

############################################

imp_dat = pd.read_csv(in_file_location)
imp_list =  imp_dat[location_name]

#Initializing variables
columns = ["frame_id",
           "frame_loc",
           "py_status", 
           "gc_fulladdress", 
           "gc_lat", 
           "gc_lng"]
df = pd.DataFrame(index=range(0,len(imp_list)), columns=columns)

for x in range(0,len(imp_list)):
    df.loc[x,"frame_loc"] = imp_list.loc[x]
    df.loc[x,"frame_id"]  = imp_dat[id_name][x]
    
    request1 = geo_request + df.loc[x,"frame_loc"] + "&key=" + geo_key
    
    try:#Error catch around API request
        request_out = r.get(request1)
        result = request_out.json()
        
        print(result['status']+": "+str(round(x/len(imp_list)*100,2))+"% complete")
        #print(result)
        
    except:
        print("Error: Request Error")
        print(result['status'])
        df["py_status"][x]       = "Error: Request Error"
    
    try:#Error catch around writing data to frame
        
        if result['status'] == 'OK':
            
            df["py_status"][x]      = result['status']
            df["gc_fulladdress"][x] = result["results"][0]["formatted_address"]
            df["gc_lat"][x]         = result["results"][0]["geometry"]['location']['lat']
            df["gc_lng"][x]         = result["results"][0]["geometry"]['location']['lng']
        
        else:#Error catch around API status
            
            df["py_status"][x]       = result['status']
            
    except: #everything else....
        
        df["py_status"][x]       = "Error: General Python Error"
        
    #clear variable for looping just incase it fails
    result = []
        
df.head()           

df.to_csv(out_file_location)           
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
