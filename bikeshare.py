import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #get user input for city (chicago, new york city, washington).user lower function to standarize all answers
    city = input('Please type the full name of one of these cities \nChicago \nNew york city \nWashington \nto view bikeshare data: ').lower()
    #Use a while loop to handle invalid inputs
    while city not in CITY_DATA.keys():
        print("This is not correct,please check your input")
        #repeat
        city = input('Please type the full name of one of these cities \nChicago \nNew york city \nWashington \nto view bikeshare data: ').lower()
    
    #create a month dictionary to store month data
    months_data = {"january":1,"february":2,"march":3,"april":4,"may":5,"june":6,"all":7}
    #get user input for month (all, january, february, ... , june)
    month = input('to filter by a month Please type \nJanuary \nFebruary \nMarch \nApril \nMay \nJune \nor All to no filter by month: ').lower()
    #Use a while loop to handle invalid input
    while month not in months_data.keys():
        print("This is not correct,please check your input")
        #repeat
        month = input('To filter by a month Please type \nJanuary \nFebruary \nMarch \nApril \nMay \nJune \nor All to no filter by month: ').lower()
    
    #create a week dictionary to store week data        
    week = {"sunday" : 1,"monday":2,"tuesday":3,"wednesday":4,"thursday":5,"friday":6,"saturday":7,"all":8}
    #get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("to filter by a day Please type \nSunday \nMonday \nTuesday \nWednesday \nThursday \nFriday \nSaturday \nor All to no filter: ").lower()
    #Use a while loop to handle invalid input
    while day not in week.keys():
        print("This is not correct,please check your input")
        #repeat
        day = input("to filter by a day Please type \nSunday \nMonday \nTuesday \nWednesday \nThursday \nFriday \nSaturday \nor All to no filter: ").lower()
        
    
    print('-'*40)
    return city , month, day
   
    
    
def load_data(city, month, day):
    
    
    """
    Loads data for the specified city and filters by month and day if applicable.
    
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #Load City Data into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    #Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #Extract month and day of week from Start Time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    #filter by month
    if month != "all":
        months = ["january","february","march","april","may","june"]
        month = months.index(month)+1
        df= df[df['month'] == month]
    
    #filter by day
    if day != 'all':
        df =  df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    most_common_month = df['month'].mode()[0]
    print('most common month ',most_common_month)
    #display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print ('most common day ',most_common_day) 
    #Extract hour from start time
    df['hour'] = df['Start Time'].dt.hour
    #display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print ('most common hour ',most_common_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    most_common_start_station  = df['Start Station'].mode()[0]
    print('common start station is ',most_common_start_station)

    #display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    
    print('common end station is ',most_common_end_station) 

    #Create a column of combination of start station and end station
    df['combination of start & end'] = df['Start Station'] + df['End Station']
    #display most frequent combination of start station and end station trip
    most_common_combo = df['combination of start & end'].mode()[0]
    print('common combination of both is ',most_common_combo)
   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Calculate and display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time is ',total_travel_time)
    #calculate and display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('mean of travel time is ',mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #calculate and display counts of user types
    count_user_types = df['User Type'].count()
    print('Count of User types is ',count_user_types)

    #Display counts of gender
    #Use try and except to handle exceptions in case of washington
    try:
        count_gender = df['Gender'].count()
        print('count of gender is ',count_gender)
    except:
        print("\nSorry,there is no 'Gender' Data in this City file.")
    
    #Display earliest, most recent, and most common year of birth
    #Use try and except to handle exceptions in case of washington
    try:
        earliest_birthdate = int(df['Birth Year'].min())
        most_recent_birthdate = int(df['Birth Year'].max())
        most_common_birthdate = int(df['Birth Year'].mode()[0])
        ("Earliest, most recent and most common birthdates are {}, {}, and {} in order").format(earliest_birthdate,most_recent_birthdate,most_common_birthdate)
    except:
        print("\nSorry,there is no Birth Year Data in this City file")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    '''Ask if the user wants to show raw data'''
    answers = ["yes","no"]
    start = 0
    print("Do you want to display raw data?")
    #take user input
    answer = input("Please answer with  yes or no: ").lower()
    #use while loop to handle invalid inputs
    while answer not in answers:
        print("this is an invalid input")
        #repeat
        print("Do you want to display raw data?")
        answer = input("Please answer yes or no: ").lower()
    
    #use a while loop to show more raw data     
    while answer == "yes" :
        raw = df.iloc[start:start+5]
        print(raw)
        print("Do you want to display more raw Data?")
        answer2 = input("Please answer with yes or no: ").lower()
        if answer2 == "yes":
            start +=5
            print(raw)
        elif answer2 == "no":
            break
        elif answer2 not in answers:
            print("this is an invalid input")
            #repeat
            print("Do you want to display more raw Data?")
            answer2 = input("Please answer with yes or no: ").lower()
            
            
    print("_"*80)
        
def main():
    while True:
        city,month,day = get_filters()
        print(city,month,day)
        df = load_data(city,month,day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()