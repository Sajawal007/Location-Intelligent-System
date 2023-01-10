import time
import populartimes

class PeakHours:
    @staticmethod
    def extractPopTimes(api_key,min_place):
        min_place.reverse()
        min_place.sort()
        pop_times = None
        print(min_place[0][1])
        pop_times = populartimes.get_id(api_key, min_place[0][1])
        print(pop_times)
        
        return pop_times

    @staticmethod
    def returnMaxHour(arr):
        max = -1000
        max_ind = 0
        for i in range(len(arr)):
            if max < arr[i]:
                max_ind = i 
                max = arr[i]
        return max_ind

    @staticmethod
    def returnMinHour(arr):
        min = arr[0]
        min_ind = 0
        for i in range(len(arr)):
            if min > arr[i]:
                min_ind = i
                min = arr[i]
        return min_ind

    @staticmethod
    def peakStringGenerator(max_list):
        peak_strings = ""
        print("::Peak TIMEs::")
        l = set(max_list)
        arr = []
        [arr.append(r) for r in l]
        for i in range(len(arr)):
            if arr[i] != None:
                t = time.strptime(str(arr[i]), "%H")
                timevalue_12hour = time.strftime( "%I:%M %p", t )
                if i == len(arr)-1:
                    peak_strings += str(timevalue_12hour)
                else:
                    peak_strings += str(timevalue_12hour)+" | "
        
        return peak_strings

    @staticmethod
    def OffPeakStringGenerator(min_list):
        non_peak_strings = ""
        l = set(min_list)
        arr = []
        [arr.append(r) for r in l]
        for i in range(len(arr)):
            if arr[i] != None:
                t = time.strptime(str(arr[i]), "%H")
                timevalue_12hour = time.strftime( "%I:%M %p", t )
                if i == len(arr)-1:
                    non_peak_strings += str(timevalue_12hour)
                else:
                    non_peak_strings += str(timevalue_12hour)+" | "

        return non_peak_strings

    def barChartArr(pop_times):
        arr = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for i in range(len(pop_times['populartimes'])):
            k = 0
            for j in range(len(pop_times['populartimes'][i]['data'])):
                arr[k] +=  pop_times['populartimes'][i]['data'][j]
                k += 1
        pop_times_str  = str(arr)

        return pop_times_str
