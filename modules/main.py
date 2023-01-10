from os import getuid
from PlotGraph import *
from helpingFunctions import *
from PeakHours import *
from OutputHtml import *
import pandas as pd
from Graphics import *
import tkinter as tk
#global variables


"""
    Proposed Locations Variables
"""

api_key = "AIzaSyCcaR5M4Osui8-xhn3RtgPIcMw1r4lMiAE"
proposed_location = (31.41811331925385,73.1407931992487)
proposed_location_str = "31.41811331925385,73.1407931992487"
latitude = 31.41811331925385
longitude = 73.1407931992487


"""
    Count/Data for Competitors, Schools and Banks
"""

total_no_of_competitors = None
total_no_of_schools = None
total_no_of_banks = None
competitors = None
banks = None
schools = None   


"""
    Extract locations in 5KM Radius Locations i.e Petrol Pumps, Banks, ATMs, Schools and Universitites
"""

def extract_locations(proposed_location_str):
    result_five_km_pumps = HelpingFunction.returnLatLongs(5000,proposed_location_str,"filling+station|petrol+pump","gas+station")
    result_two_km_pumps = HelpingFunction.returnLatLongs(2000,proposed_location_str,"filling+station|petrol+pump","gas+station")
    result_one_km_pumps = HelpingFunction.returnLatLongs(1000,proposed_location_str,"filling+station|petrol+pump","gas+station")
    result_five_km_schools = HelpingFunction.returnLatLongs(5000,proposed_location_str,"school|university","university,school,secondary_school,primary_school")
    result_five_km_banks = HelpingFunction.returnLatLongs(5000,proposed_location_str,"bank|atm","bank,atm")
    #let's make dataframe of the collected data.

    df_five_km_pumps = pd.DataFrame(result_five_km_pumps)
    df_two_km_pumps = pd.DataFrame(result_two_km_pumps)
    df_one_km_pumps = pd.DataFrame(result_one_km_pumps)
    df_five_km_schools = pd.DataFrame(result_five_km_schools)
    df_five_km_banks = pd.DataFrame(result_five_km_banks)

    #adding url to check the site availability

    df_five_km_pumps['url'] = 'https://www.google.com/maps/place/?q=place_id:' + df_five_km_pumps['place_id']
    df_two_km_pumps['url'] = 'https://www.google.com/maps/place/?q=place_id:' + df_two_km_pumps['place_id']
    df_one_km_pumps['url'] = 'https://www.google.com/maps/place/?q=place_id:' + df_one_km_pumps['place_id']
    if len(df_five_km_schools)>1:
        df_five_km_schools['url'] = 'https://www.google.com/maps/place/?q=place_id:' + df_five_km_schools['place_id']
    if len(df_five_km_banks)>=1:
        df_five_km_banks['url'] = 'https://www.google.com/maps/place/?q=place_id:' + df_five_km_banks['place_id']
    


    #save all the petrol pumps in the area to a newly created file

    df = HelpingFunction.dfs_concatenator([df_five_km_pumps,df_two_km_pumps,df_one_km_pumps],proposed_location_str+'.xlsx')

    #extract Competitors Petrol Pumps
    PSO = df[df['name'].str.contains("PSO")]
    Shell = df[df['name'].str.contains("Shell")]
    Total = df[df['name'].str.contains("Total")]
    Attock = df[df['name'].str.contains("Attock")]

    competitors = HelpingFunction.dfs_concatenator([PSO,Shell,Total,Attock],"../cache/"+proposed_location_str+"_C"+'.xlsx')
    schools = HelpingFunction.dfs_concatenator([df_five_km_schools],"../cache/"+proposed_location_str+"_S"+".xlsx")
    banks = HelpingFunction.dfs_concatenator([df_five_km_banks],"../cache/"+proposed_location_str+"_B"+".xlsx")

    return competitors,schools,banks


def extract_locations_offline(lat,long):
    schools_f_name = "../cache/"+str(lat)+", "+str(long)+"_S"+".xlsx"
    banks_f_name = "../cache/"+str(lat)+", "+str(long)+"_B"+".xlsx"
    pumps_f_name = "../cache/"+str(lat)+", "+str(long)+"_C"+".xlsx"
    comp = pd.read_excel(pumps_f_name)
    banks = pd.read_excel(banks_f_name)
    schools = pd.read_excel(schools_f_name)

    return comp,schools,banks

"""
    Normalize Locations and extract latitudes and logitudes
"""
def extract_coordinates(df):
    lats,longs = HelpingFunction.returnLanLat(HelpingFunction.findDist(df))
    return lats,longs


"""
    Calculate places count lying withint the range of 10KM
"""

def returnCount(lat,long,comp,schools,banks):
    c_lats, c_longs = HelpingFunction.returnLanLat(HelpingFunction.findDist(comp))
    s_lats, s_longs = HelpingFunction.returnLanLat(HelpingFunction.findDist(schools))
    b_lats, b_longs = HelpingFunction.returnLanLat(HelpingFunction.findDist(banks))
    c_count,_ = HelpingFunction.no_of_locs_within_range(lat,long,c_lats, c_longs,comp)
    s_count,_ = HelpingFunction.no_of_locs_within_range(lat,long,s_lats, s_longs,schools)
    b_count,_ = HelpingFunction.no_of_locs_within_range(lat,long,b_lats, b_longs,banks)

    return c_count,s_count,b_count

"""
    Let's plot the extracted coordinates, 
    filename: .html file will be created
"""
def plot_graphs(lats,longs,filename,competitors_df):
    gmap = PlotGraph.plotGraph(latitude,longitude)
    PlotGraph.mentionDistance(gmap,latitude,longitude,lats,longs,filename,competitors_df)
    return gmap

"""
    Extracting the peak hours for nearest Pump to Proposed location
"""
def extract_peak_times(pop_times):
    min_list = []
    max_list = []
    for i in range(len(pop_times['populartimes'])):
        min_list.append(PeakHours.returnMinHour(pop_times['populartimes'][i]['data']))
        max_list.append(PeakHours.returnMaxHour(pop_times['populartimes'][i]['data']))


    return PeakHours.peakStringGenerator(max_list),PeakHours.OffPeakStringGenerator(min_list)


"""
    Output the extracted infromation in the form of HTMl/CSS/Javascript Page.
"""
def generateOutput(filename,peak_strings,non_peak_strings,total_no_of_banks,total_no_of_schools,total_no_of_competitors,population,pop_times_str):
    OutputHTML.generate_html(filename,total_no_of_banks,total_no_of_schools,total_no_of_competitors,peak_strings,non_peak_strings,population,pop_times_str)



"""
    Execute all the features
"""

def execute_features(lat,long):
    if lat != None and long != None:
        proposed_location_str = str(lat)+","+str(long)
        latitude, longitude = float(lat),float(long)
        file_name = "../results/" + str(latitude) + "," + str(longitude) + ".html"
        if HelpingFunction.isFileExist(file_name) == False:
            competitors,schools,banks = extract_locations_offline(latitude,longitude)
            # competitors,schools,banks = extract_locations(proposed_location_str)
            lats,longs = extract_coordinates(competitors)
            gmap = PlotGraph.plotGraph(latitude,longitude)
            places_n_distances = PlotGraph.mentionDistance(gmap,latitude,longitude,lats,longs,file_name,competitors)
            time.sleep(2)
            pop_times = PeakHours.extractPopTimes(api_key,places_n_distances)
            peak_str,off_peak_str = extract_peak_times(pop_times)
            total_no_of_competitors,total_no_of_schools,total_no_of_banks = returnCount(latitude, longitude, competitors,schools,banks)
            city_population = HelpingFunction.extract_city_population(competitors)
            pop_times_str = PeakHours.barChartArr(pop_times)
            generateOutput(file_name,peak_str,off_peak_str,total_no_of_banks,total_no_of_schools,total_no_of_competitors,city_population,pop_times_str)
            HelpingFunction.loadHTML(file_name)
        else:
            HelpingFunction.loadHTML(file_name) 

def main():

    lat = None
    long = None
    frame = tk.Tk()
    frame.title("Location Intelligent System")
    frame.geometry('800x800')

    bg = tk.PhotoImage(file = "../src/pso_logo.png")

    label1 = tk.Label(frame, image = bg)
    label1.place(x = 0,y = 0)

    lbl2 = tk.Label(frame,text="Enter Coordinates: (latitude, longitude)")
    lbl2.place(x = 305,y= 380)

    inputtxt = tk.Text(frame, height = 2,width = 50)
    inputtxt.place(x=250,y=400)

    def getInput():
            inp = inputtxt.get(1.0, "end-1c") 
            # Label Creation
            lbl = tk.Label(frame, text = "")
            lbl.place(x=300,y=400)
            lbl2.destroy()
            printButton.destroy()
            inputtxt.destroy()
            if HelpingFunction.internet() == True:
                inp.strip()
                lst_ = inp.split(",")
                if len(lst_) > 1:
                    validInput = True
                    lat,long = lst_[0],lst_[1]
                    lbl.config(text = "Exploration Started :)\nPlease Wait!",fg='#21E1E1',font=('Arial', 20))  
                    execute_features(lat,long)
                else:
                    lbl.config(text = "Please Enter Valid Input!",fg='#C21010',font=('Arial', 20))  
            else:
                    lbl.config(text = "NO INTERNET CONNECTION! :(\nPlease Check Internet",fg='#C21010',font=('Arial', 20))

    printButton = tk.Button(frame,
	text = "Explore", 
	command = getInput)
    printButton.place(x=380,y=431)


    frame.mainloop()


    
main()

    







        
        


         





    