""" File for processing METAR data at Gingin Aero station, to be joined with data from
    Zadko weather station. PRCP_9AM and PRCP_10 are used to create interval data.
    Each value in final prcp column represents precipitation fallen in the interval
    since the previous record.

    Last updated 24/04/2021 - just interval precip in returned dataframe.

    Author: Matvey Solovyov.
"""

import pandas as pd
import datetime

def make_prcp_interval(df):
    # can have at maximum double the number of rows, if every row has significant 10min precip
    df_new = pd.DataFrame(columns=['date','prcp'], index = range(1,2*len(df)))

    # first row may lose since 9AM information so just take 10min data
    df_new.iloc[0][['date','prcp']] = df.iloc[0][['LSD', 'PRCP_10']]

    # define an index to keep track of new dataframe
    j = 1

    # loop through entire dataframe - AFAIK cannot be done using array manipulations
    for i in range(1, len(df) ):

        # If it's the first row after 9am, will be handled differently. Define Boolean var to be used.
    
        if df.iloc[i]['LSD'].time() > datetime.time(9,0):
            # if current row is after 9 am, check if previous is after 9 and on the same day
            previous_after_9AM = df.iloc[i - 1]['LSD'].date() == df.iloc[i]['LSD'].date() and df.iloc[i - 1]['LSD'].time() > datetime.time(9,0) 
        else:
            # if current row is before 9 am, check if previous row is same day, or previous day but after 9 am on that day.
            previous_after_9AM = df.iloc[i - 1]['LSD'].date() == df.iloc[i]['LSD'].date() or \
                                        (df.iloc[i - 1]['LSD'].date() == df.iloc[i]['LSD'].date() - datetime.timedelta(days= 1) and \
                                         df.iloc[i - 1]['LSD'].time() > datetime.time(9,0))
                
                
        # have some precip in the previous 10 mins, and the previous record was more than 10 mins ago
        if df.iloc[i]['PRCP_10'] > 0 and (df.iloc[i]['LSD'] - df.iloc[i-1]['LSD']).seconds > 600:

            # add one row for precip fallen more than 10 mins before current row, but after previous row
            new_prcp_10 = df.iloc[i]['PRCP_9AM'] - df.iloc[i]['PRCP_10']

            # if previous record was not 9am, need to subtract previous precip
            if previous_after_9AM:
                new_prcp_10 -= df.iloc[i-1]['PRCP_9AM']
                
            # timestamp will be 10 mins before current row
            df_new.iloc[j][['date','prcp']] = (df.iloc[i]['LSD'] - datetime.timedelta(minutes = 10) , abs(round(new_prcp_10,2)) )

            j += 1

            # add a second row for precip fallen in the 10 mins before this row
            df_new.iloc[j][['date','prcp']] = (df.iloc[i]['LSD'], df.iloc[i]['PRCP_10'])

            j += 1

        # don't have precip in last 10 mins, or have, but previous record was 10 or less mins ago
        else:

            # set precip value to difference in 9am precip values
            # unless previous record was 9am, then don't need to subtract previous precip

            new_prcp = df.iloc[i]['PRCP_9AM']

            if previous_after_9AM:
                new_prcp -= df.iloc[i - 1]['PRCP_9AM']

            df_new.iloc[j][['date','prcp']] = (df.iloc[i]['LSD'], abs( round( new_prcp , 2 ) ) )
            j += 1

    # return new DF without NaNs added when initialising the DF
    return df_new.dropna()

def process_files(n = 3):
    """ function processing the files when data is separated into multiple files.
        Argument 'n' represents the number of files. Can add functionality for filenames / paths.
        For now, this is harcoded.
    """
    # initialize empty data frame
    metar_data = pd.DataFrame()

    # loop through number of files
    for i in range( 1 , n+1 ):

        s = "C:\\Users\\Matvey Solovyov\\OneDrive\\Documents\\UWA\\2021_S1\\GinginWx\\gingin-weather\gingin_aero"+str(i)+".csv"
        
        # only read in the required columns, MSG included for confidence checks
        # LSD column is the local time, in datetime format
        subdf = pd.read_csv(s, usecols=['LSD','PRCP_9AM','PRCP_10','MSG'] )
        
        # join dataframe vertically
        metar_data = pd.concat([metar_data, subdf])
    
    # convert local datetime column to pandas datetime format
    metar_data['LSD'] = pd.to_datetime( metar_data['LSD'] )

    # drop any rows where PRCP columns are NaNs.
    metar_data = metar_data.dropna()

    return metar_data

def main():
    metar_data = process_files(3)

    metar_prcp = make_prcp_interval( metar_data )

    metar_prcp.to_csv("C:\\Users\\Matvey Solovyov\\OneDrive\\Documents\\UWA\\2021_S1\\GinginWx\\gingin-weather\\gingin_metar_prcpINT.csv", index=False)

    return True
