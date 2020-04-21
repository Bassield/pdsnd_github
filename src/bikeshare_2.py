import time
import sys
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Cities to explore Chicago, New York City or Washington')
    print('Valid entries are: ')
    print('                 Chicago / C            ')
    print('                 New York City / NYC / N')
    print('                 Washington / W         ')
    city = None
    while city not in ['chicago', 'new york city', 'washington']:
        city = input('Please enter a city name: ').lower()
        if city == 'chicago' or city == 'c':
            city = 'chicago'
        elif city == 'new york city' or city == 'nyc' or city == 'n':
            city = 'new york city'
        elif city == 'washington' or city == 'w':
            city = 'washington'
        else:
            print('Invalid Entry - Chicago / C, New York City / NYC / N or Washington / W')
            city = input("Please enter a valid city name: ").lower()

    # get user input for month (all, january, february, ... , june)
    print('Please enter a number for the Month you would like to explore')
    print('January - 1')
    print('February - 2')
    print('March - 3')
    print('April - 4')
    print('May - 5')
    print('June - 6')
    print('All - 0')
    input_month = -1
    month_dict = {1: 'january', 2: 'february', 3: 'march',  4: 'april', 5: 'may', 6: 'june', 0: 'all'}
    while input_month not in month_dict.keys():
        input_month = eval(input("Please enter the month value for data required: "))
        if input_month not in month_dict.keys():
            print('That was a invalid entry, please try again\n')
    month = month_dict[input_month]

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('Please enter a number for the Day you would like to explore')
    print('Sunday - 1')
    print('Monday - 2')
    print('Tuesday - 3')
    print('Wednesday - 4')
    print('Thursday - 5')
    print('Friday - 6')
    print('Saturday - 7')
    print('All - 0')
    input_day = -1
    day_dict = {1: 'sunday', 2: 'monday', 3: 'tuesday', 4: 'wednesday', 5: 'thursday', 6: 'friday', 7: 'saturday', 0: 'all'}
    while input_day not in day_dict.keys():
        input_day = eval(input("Please enter the day value for data required: "))
        if input_day not in day_dict.keys():
            print('That was a invalid entry, please try again: \n')
    day = day_dict[input_day]

    print('-'*40)
    return city, month, day


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
    df = pd.read_csv("{}.csv".format(city.replace(" ","_")))

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['month'] = df['Start Time'].apply(lambda m: m.month)
    df['day_of_week'] = df['Start Time'].apply(lambda d: d.strftime('%A').lower())

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df.loc[df['month'] == month,:]

    if day != 'all':
        df = df.loc[df['day_of_week'] == day,:]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is {}".format(
        str(df['month'].mode().values[0]))
    )

    # display the most common day of week
    print("The most common day of the week is {}".format(
        str(df['day_of_week'].mode().values[0]))
    )

    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    print("The most common start hour is {}".format(
        str(df['start_hour'].mode().values[0]))
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most common start station is {} ".format(
        df['Start Station'].mode().values[0])
    )

    # display most commonly used end station
    print("The most common end station is {}".format(
        df['End Station'].mode().values[0])
    )

    # display most frequent combination of start station and end station trip
    df['routes'] = df['Start Station'] + " " + df['End Station']
    print("The most common start and end station combo is {}".format(
        df['routes'].mode().values[0])
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['duration'] = df['End Time'] - df['Start Time']

    # display total travel time
    print("The total travel time is {}".format(
        str(df['duration'].sum()))
    )

    # display mean travel time
    print("The mean travel time is {}".format(
        str(df['duration'].mean()))
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Here are the counts of various user types:")
    print(df['User Type'].value_counts())

    if city != 'washington':
        # Display counts of gender
        print("Gender Counts: :")
        print(df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        print("The earliest birth year: {}".format(
            str(int(df['Birth Year'].min())))
        )
        print("The latest birth year: {}".format(
            str(int(df['Birth Year'].max())))
        )
        print("The most common birth year: {}".format(
            str(int(df['Birth Year'].mode().values[0])))
        )
    else:
        print("washington file does not contain Gender and Birth Years")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
