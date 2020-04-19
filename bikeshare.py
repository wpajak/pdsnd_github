import time
import pandas as pd

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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input('Please specify the city: Chicago, New York City or Washington. \n').lower()
    while city not in CITY_DATA.keys():
        city = input('Invalid city name. Please try again. \n').lower()

    # get user input for month (all, january, february, ... , june)
    months = ['january','february','march','april','may','june']
    month = input('Please specify the month: January, February, March, April, May or June. Insert "all" for all months. \n').lower()
    while month not in months and month !='all':
        month = input('Invalid month. Please try again. \n').lower()
    if month != 'all':
        month = months.index(month)+1

    # get user input for day of week
    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    day = input('Please specify the weekday: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday. Insert "all" for all days. \n').title()
    while day not in days and day != 'All':
        day = input('Invalid weekday. Please try again. \n').title()

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
    # load data for the specified city into a dateframe
    df = pd.read_csv(CITY_DATA[city])
    # convert Start Time column into datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # create new columns with months, days and hours from Start Time column
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month != 'all':
        df = df[df['month'] == month]
    if day != 'All':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):

    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('The most common month is: \n', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The most common day is: \n', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most common hour is: \n', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('The most common start station is: \n', popular_start)

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('The most common end station is: \n', popular_end)

    # display most frequent combination of start station and end station trip
    df['Combination']='>> Start: ' + df['Start Station'] + '  >> End: ' + df['End Station']
    combined = df['Combination'].mode()[0]
    print('The most frequent combination of start station and station is: \n', combined)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_sec = df['Trip Duration'].sum()
    hours = total_sec // 3600
    mins = total_sec % 3600 // 60
    sec= (total_sec % 3600) % 60
    print("Total travel time is {} seconds, which is {} hours, {} minutes and {} seconds.".format(total_sec,hours,mins,sec))

    # Display mean travel time
    mean_sec = df['Trip Duration'].mean()
    hours = mean_sec // 3600
    mins = mean_sec % 3600 // 60
    sec= (mean_sec % 3600) % 60
    print("Average travel time is {} seconds, which is {} hours, {} minutes and {} seconds.".format(mean_sec,hours,mins,sec))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count=df['User Type'].value_counts()
    print("The count of user types is as follows:\n")
    print(user_count)
    print()

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print("The count of genders is as follows:\n")
        print(gender_count)
        print()
    except KeyError:
        print ("Gender data is not available for the selected city.")


    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = int(df['Birth Year'].min())
        recent_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode())
        print("The earliest year of birth is {}.".format(earliest_year))
        print("The most recent year of birth is {}.".format(recent_year))
        print("The most common year of birth is {}.".format(common_year))

    except KeyError:
        print ("Birth year data is not available for the selected city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        ## ask the user if they want to see 5 or more rows of the raw data

        raw_data = input("Would you like to see the first 5 lines of raw data? Enter yes or no \n")
        while raw_data.lower() not in ('yes','no'):
            raw_data = input("Invalid answer. Please insert yes or no \n")
        counter=0
        while raw_data.lower() == 'yes':
            counter+=5
            print(df.iloc[0:counter])
            raw_data = input("Would you like to include the next 5 lines of raw data? Enter yes or no \n")
            while raw_data.lower() not in ('yes','no'):
                raw_data = input("Invalid answer. Please insert yes or no \n")
        ## ask the user if they want to restart the program
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
