from unittest import result
import requests
import json
import time
import pandas as pd
import ast
import os.path
import os
import subprocess
import geopy.distance
import re
import socket

class HelpingFunction:
    @staticmethod
    def returnLatLongs(radius,location,search_text,type):
        petrol_pumps = []
        params = {}
        endpoint_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+search_text+"&location="+location+"&radius="+str(radius)+"&strictbounds&region=pk&type="+str(type)+"&key=AIzaSyCcaR5M4Osui8-xhn3RtgPIcMw1r4lMiAE"
        #let's send the request for data
        res = requests.get(endpoint_url, params = petrol_pumps)
        results =  json.loads(res.content)
        petrol_pumps.extend(results['results'])
        time.sleep(2)
        while "next_page_token" in results:
            params['pagetoken'] = results['next_page_token'],
            res = requests.get(endpoint_url, params = params)
            results = json.loads(res.content)
            petrol_pumps.extend(results['results'])
            time.sleep(2)
        
        return petrol_pumps
    @staticmethod
    def dfs_concatenator(dfs,filename):
        all_petrol_pumps = pd.concat(dfs)
        all_petrol_pumps.drop_duplicates(['reference'],keep='first',inplace=True)
        all_petrol_pumps.to_excel(filename,index=False)  #xlsx
        return all_petrol_pumps

    @staticmethod
    def findDist(df_):
        str_ = [d for d in df_['geometry']]
        lst = []
        for i in range(len(str_)):
            lst.append(ast.literal_eval(str(str_[i])))
        return lst

    @staticmethod
    def returnLanLat(location_dict):
        lats = []
        longs = []
        for i in range(0,len(location_dict)):
            lats.append(float(location_dict[i]['location']['lat']))
            longs.append(float(location_dict[i]['location']['lng']))
        return lats,longs

    @staticmethod
    def filterOutCompetitors(df,filename):
        PSO = df[df['name'].str.contains("PSO")]
        Shell = df[df['name'].str.contains("Shell")]
        Total = df[df['name'].str.contains("Total")]
        Attock = df[df['name'].str.contains("Attock")]

        competitors = HelpingFunction.dfs_concatenator([PSO,Shell,Total,Attock],filename)

    @staticmethod
    def isFileExist(filename):
        if os.path.exists(filename) == True:
            return True
        else:
            return False

    #10KM
    @staticmethod
    def no_of_locs_within_range(proposed_lat,proposed_long,lats,longs,df):
        count = 0
        locs_detail = []
        location_coordinates_ = (proposed_lat,proposed_long)
        for i in range(len(lats)):
            pump_loc = (lats[i],longs[i])
            distance_ = geopy.distance.geodesic(location_coordinates_, pump_loc).km
            if distance_ < 6:
                locs_detail.append(((distance_,str(df.iloc[i]['place_id']))))
                count += 1
        return count,locs_detail

    @staticmethod
    def loadHTML(url):
        try: # should work on Windows
            os.startfile(url)
        except AttributeError:
            try: # should work on MacOS and most linux versions
                subprocess.call(['open', url])
            except:
                print('Could not open URL')

    @staticmethod
    def extract_city_population(competitors):
        text = str(competitors.iloc[0]['formatted_address'])
        
        lst = text.split(",")

        city_name = lst[len(lst)-2].strip()

        print(city_name)

        URL = f"https://google.com/search?q=population+in+"+city_name

        # desktop user-agent
        USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
        
        headers = {"user-agent" : USER_AGENT}
        resp = requests.get(URL, headers=headers)
        result_str = ""
        result_str = re.findall(r"<div class=\"Z0LcW\">(.*) \(2017\)</div>" ,resp.text)
        digits_ = None
        with_comma = True
        #print(len(result_str))
        if len(result_str) == 0:
            result_str = re.findall(r"<div class=\"ayqGOc kno-fb-ctx KBXm4e\" skp-pat=\"\$v \&lt\;span class=\'kpd-date\'\&gt\;\(\$d\)\&lt\;\/span\&gt\;\">(.*) \(2017\)</div>",resp.text)
            if len(result_str) == 0:
                digits_ = "Population Data not available"
            else:
                digits = re.findall(r"([0-9.]+)",str(result_str[0]))
                digits_ = float(digits[0]) * 1000000
                with_comma = False
        if with_comma == True and len(result_str) > 0:
            digits = re.findall(r"([0-9.]+)",str(result_str[0]))
            digits_ = digits[0] + digits[1]
            digits_ = int(digits_)


        return digits_



    #Function to check internet connectivity
    @staticmethod
    def internet(host="8.8.8.8", port=53, timeout=3):
        """
        Host: 8.8.8.8 (google-public-dns-a.google.com)
        OpenPort: 53/tcp
        Service: domain (DNS/TCP)
        """
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error as ex:
            print(ex)
            return False






    

    
    

