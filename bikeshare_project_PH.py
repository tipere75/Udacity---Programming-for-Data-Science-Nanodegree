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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Which city are you interested in ? Chicago, New York City or Washington ?\n").lower()
    while city not in ["chicago", "new york city", "washington"]:
        city = input("Please choose one of the folowwing cities : Chicago, New York City or Washington.\n")

    # get user input for month (all, january, february, ... , june)
    month = input("Which month are we focusing on ? January, February, ... June, or all ?\n").lower()
    while month not in ["january", "february", "march", "april", "may", "june", "all"]:
        month = input("Please choose one month among January, February, March, April, May, June or all.\n").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Which day are we focusing on ? Monday, Tuesday, ... Sunday or all ?\n").lower()
    while day not in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]:
        day = input("Please choose one day among Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all.\n").lower()

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
    #reading the file
    df = pd.read_csv(CITY_DATA[city])

    #filtering the month
    df["month"] = pd.to_datetime(df["Start Time"]).dt.month
    if month != "all":
        # use the index of the months list to get the corresponding int
        months = ["january", "february", "march", "april", "may", "june"]
        df = df[df["month"]==months.index(month) + 1]

    #filtering the day
    df["day"] = pd.to_datetime(df["Start Time"]).dt.weekday_name
    if day != "all":
        df = df[df["day"]==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month if not filtered on a particular month
    if len(set(df["month"])) > 1:
        months = ["january", "february", "march", "april", "may", "june"]
        popular_month = months[df["month"].mode()[0]-1].title()
        month_count = max(df["month"].value_counts())
        print("The most common month is {0} with {1} occurences.".format(popular_month, month_count))

    # display the most common day of week if not filtered on a particular day
    if len(set(df["day"])) > 1:
        popular_day = df["day"].mode()[0]
        day_count = df["day"].value_counts()[df["day"].mode()[0]]
        print("The most common day is {0} with {1} occurence.".format(popular_day, day_count))

    # display the most common start hour
    df["hour"] = pd.to_datetime(df["Start Time"]).dt.hour
    popular_hour = df["hour"].mode()[0]
    hour_count = df["hour"].value_counts()[df["hour"].mode()[0]]
    print("The most common hour is {0} with {1} occurences.".format(popular_hour, hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df["Start Station"].mode()[0]
    popular_start_station_count = df["Start Station"].value_counts()[df["Start Station"].mode()[0]]
    print("The most commonly used start station is {0} with {1} occurences.".format(ppopular_start_station, popular_start_station_count))

    # display most commonly used end station
    pop_end_station = df["End Station"].mode()[0]
    pop_end_station_count = df["End Station"].value_counts()[df["End Station"].mode()[0]]
    print("The most commonly used end station is {0} with {1} occurences.".format(pop_end_station, pop_end_station_count))

    # display most frequent combination of start station and end station trip
    df["Start and End Station"] = df["Start Station"] + "," + df["End Station"]  #key to identify the trip with its start station and end station
    pop_trip = df["Start and End Station"].mode()[0]
    pop_trip_count = df["Start and End Station"].value_counts()[df["Start and End Station"].mode()[0]]
    starting_station = pop_trip.split(sep=",")[0]
    ending_station = pop_trip.split(sep=",")[1]
    print("The most commonly used trip starts at {0} and ends at {1} with {2} occurences.".format(starting_station, ending_station, pop_trip_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df["Trip Duration"].sum()
    print("The total duration is {}.".format(total_duration))

    # display mean travel time
    average_duration = df["Trip Duration"].mean()
    print("The average duration is {}.".format(average_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_type = df["User Type"].value_counts()
    print("There are {0} subscriber and {1} customer.".format(count_user_type[0], count_user_type[1]))

    # Display counts of gender
    try:
        count_gender = df["Gender"].value_counts()
        print("There are {0} male and {1} female.".format(count_gender[0], count_gender[1]))
    except:
        print("The gender variable is not available in this dataset.")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = df["Birth Year"].min()
        most_recent_birth_year = df["Birth Year"].max()
        most_common_birth_year = df["Birth Year"].mode()[0]
        print("The eldest client was born in {}.".format(earliest_birth_year))
        print("The youngest client was born in {}.".format(most_recent_birth_year))
        print("The most common year of birth is {}.".format(most_common_birth_year))
    except:
        print("No birth date is available in our data.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def affiche(row):
    """ Print one observation of raw data in a viewable format """
    print("{")
    for ind, val in row.items():
        print("{} : {}".format(ind,val))
    print("}")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        #printing the desired statistics
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        #deleting unnecessary columns
        df = df.drop(["month", "hour", "Start and End Station"], axis=1)

        #printing raw data if requested
        raw_data = input("Would you like to see 5 lines of raw data ?\n").lower()
        while raw_data not in ["yes", "no"]:
            raw_data = input("Please answer by Yes or No.\n").lower()
        while raw_data == "yes":
            z = df.sample(5)
            for row in range(5):
                affiche(z.iloc[row,:])
            raw_data = input("Would you like to see 5 more lines of raw data ?\n").lower()
            while raw_data not in ["yes", "no"]:
                raw_data = input("Please answer by Yes or No.\n").lower()

        #offering the possibility to restart the analysis from the beginning
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
