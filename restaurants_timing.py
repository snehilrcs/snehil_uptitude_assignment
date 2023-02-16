class restaurant_open_time():
    
    def __init__(self,date_time_object,csv_file_name):
        
        self.date_time_object = date_time_object
        self.csv_file_name = csv_file_name
        
    def convert_to_24_hrs_format(self,time_string):
        '''Converts the am pm format to 24 hour format'''
        
        try:
            time_obj = datetime.strptime(time_string, '%I:%M %p')
        except ValueError:
            time_obj = datetime.strptime(time_string, '%I %p')
        time_obj = time_obj.strftime('%H:%M')

        return(time_obj)

    def convert_string_to_day_time(self,timing_string):
        
        '''Converts the arbitrary timing into structured timing'''
        
        day_time = {}
        hours = re.findall(r'(\w{3}(?:-\w{3})?(?:, \w{3})?) (\d{1,2}:\d{2} [ap]m|\d{1,2} [ap]m) - (\d{1,2}:\d{2} [ap]m|\d{1,2} [ap]m)', timing_string)
        #print(hours)
        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        for hour in hours:
            opening_time = convert_to_24_hrs_format(hour[-2])
            closing_time = convert_to_24_hrs_format(hour[-1])
            day_ranges=hour[0].split(",")
            for day_range in day_ranges:
                if(len(day_range.split("-"))>1):
                    start_day = day_range.split("-")[0]
                    end_day = day_range.split("-")[1]
                    start_index = days.index(start_day)
                    end_index = days.index(end_day)
                    #print(f"start_index={start_index},end_index={end_index}")
                    for i in range(start_index,end_index+1):
                        #print(days[i],opening_time,closing_time)
                        day_time[days[i]] = [opening_time,closing_time]
                else:
                    #print(day_range.strip(),(opening_time),closing_time)
                    day_time[day_range.strip()] = [opening_time,closing_time]
                    #if(opening_time<closing_time):
                     #   print("Hi Hello")
                    #else:
                     #   print("YO")
                    day_time[day_range.strip()] = [opening_time,closing_time]
        return day_time

    def read_csv_file(self):
        
        '''Reads the csv file and transforms it into computable date type'''
        
        df = pd.read_csv(self.csv_file_name,names = ["restaurants","date_time"])
        #df.head()
        dict_list = []
        for string in df["date_time"].iteritems():
            #print((string[1]))
            dict_list.append(self.convert_string_to_day_time(string[1]))
        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        days_start = ["Mon_start","Tue_start","Wed_start","Thu_start","Fri_start","Sat_start","Sun_start"]
        final_data = []
        for obj in dict_list:
            columns = days
            data = []
            for day in days:

                data.append(obj.get(day,[0,0])[0])
            final_data.append(data)
            df_days_start = pd.DataFrame(final_data,columns = days_start)
            #df_days.head(-5)
        final_data = []
        days_end = ["Mon_end","Tue_end","Wed_end","Thu_end","Fri_end","Sat_end","Sun_end"]
        for obj in dict_list:
            columns = days
            data = []
            for day in days:

                data.append(obj.get(day,[0,0])[1])
            final_data.append(data)
        df_days_end = pd.DataFrame(final_data,columns = days_end)
        df_days_end.head()
        df_days = pd.concat([df_days_start,df_days_end],axis = 1)
        df_days.head()
        #Lets Join the Dataframe
        df_concat = pd.concat([df, df_days], axis=1)
        df_concat.head()
        return df_concat

    def split_date_time_object(self,date_time_object):
        
        '''Extracts the days and time from the date time object'''
        
        day_time = []
        #dt = date_time_object.strptime(date_time_object, '%Y-%m-%d %H:%M:%S.%f')
        day = date_time_object.strftime('%A')
        time = date_time_object.strftime('%H:%M')
        day_time = [day[:3],time]
        return day_time
    
    def get_open_restaurants(self):
        
        '''Lists out the restaurants which are open during that hours on a particular day'''
        df_concat = self.read_csv_file()
        date_time = self.split_date_time_object(self.date_time_object)
        print(f"These are the restaurants which will be opened on {date_time[0]} at {date_time[1]}")
        day = date_time[0]
        #print(day)
        time = date_time[1]
        day_start= day + "_start"
        day_end = day + "_end"
        time_filter = (df_concat[day_start].astype(str) < time) & (df_concat[day_end].astype(str) > time)
        selected_rows = df_concat.loc[time_filter]
        return selected_rows["restaurants"]

        
if __name__ == "__main__":
    
    date = int(input("Enter the Day of the Month - "))
    month = int(input("Enter the month in integer - "))
    year = int(input("Enter the year - "))
    hour = int(input("Enter the hour - "))
    minute = int(input("Enter the minutes - "))
    file_name = input("Enter the file name")
    
    obj = restaurant_open_time(datetime(year, month, date, hour, minute),file_name)
    lst = obj.get_open_restaurants()
    if(len(lst) > 0):
        print(lst)
    else:
        print("Sorry there are no restaurants opened at this time")
