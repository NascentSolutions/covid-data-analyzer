#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
#
# https://pypi.org/project/uk-covid19/
#
# pip install uk-covid19
#
# Note. You have to download and install the Wheel file manually:
# pip install uk_covid19-1.2.0-py3-none-any.whl
#
# Usage guide:
# https://publichealthengland.github.io/coronavirus-dashboard-api-python-sdk/pages/examples/general_use.html
# https://coronavirus.data.gov.uk/developers-guide
# 
# Other data:
# https://coronavirus.data.gov.uk/details/testing 
#
# 
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #

import os
import numpy

from uk_covid19 import Cov19API
from matplotlib import pyplot

local_temp = os.environ['TMP']
csv_path = os.path.join(local_temp, 'COVID Data Analyzer' + '.csv') #C:\Users\<user_name>\AppData\Local\Temp\COVID Data Analyzer

# England 2018 total deaths and causes
deaths_2018 = 505859 # England and Wales total: 541,589 - Wales is 6.5% of all deaths
deaths_2018_cancer = 120535 * 0.935
deaths_2018_dementia = 69478 * 0.935
deaths_2018_cvd = 55995 * 0.935
deaths_2018_stroke = 31288 * 0.935
deaths_2018_lungcancer = 29626 * 0.935
deaths_2018_flu = 29516 * 0.935
deaths_2018_suicide = 9834 * 0.935
deaths_2018_diabetes = 6349 * 0.935



def downloadCSV():

    # Filters
    england_only = [
        'areaType=nation',
        'areaName=England'
    ]

    # Structure
    cases_and_deaths = {
        'date': 'date',
        'areaName': 'areaName',
        'newCases': 'newCasesByPublishDate',
        'newDeaths': 'newDeathsByDeathDate',
        'hospitalCases': 'hospitalCases',
        'covidOccupiedMVBeds': 'covidOccupiedMVBeds'
    }

    api = Cov19API(filters=england_only, structure=cases_and_deaths)

    csv_output = api.get_csv()

    return csv_output


def IntegerToMonth(number):

    # Create a dictionary
    month_case = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }

    return month_case.get(number)


def saveCSV(csv_to_save, csv_path):
    with open(csv_path, 'w') as csv:
        csv.write(csv_to_save)


def readData(csv_path):

    lines_total = []

    with open(csv_path, 'r') as csv:

        lines = csv.readlines()

        for i in lines:

            i = i.strip('\n')
            i = i.rstrip(',')
            i = i.split(',')

            #if len(i) == 3:
                #i.append('0')

            lines_total.append(i)


    idata_list = []     # Final list of lists

    # Remove column headers
    lines_total.remove(lines_total[0])

    # Remove the first 60 dates (between 03/01/20 and 02/03/20), as they have no death values)
    deaths_start = 59
    hospital_start = 77
    mv_start = 90
    lines_total.reverse()   # By default, the data is received the most recent date first

    for line in lines_total[0:mv_start]:
        lines_total.remove(line)
    
    # Leave out the final 7 days, as it often has missing data
    lines_total = lines_total[:-7]

    # Create a final list, with date split
    for i in lines_total:

        #if len(i) < 4: continue

        #print(i)

        y, m, d = i[0].split('-')
        day = int(d)
        month = int(m)
        year = int(y)

        area = i[1]
        new_cases = int(i[2])
        new_deaths = int(i[3])
        hospital_cases = int(i[4])
        covid_occupied_mv_beds = int(i[5])

        #idata_list.append([day, month, year, area, new_cases, new_deaths])
        idata_list.append([day, month, year, area, new_cases, new_deaths, hospital_cases, covid_occupied_mv_beds])
    
    #print(idata_list)


    return idata_list


def createAverageLine(x_list, cause_of_death):
    
    cod_y_list = []

    for i in x_list:
        cod_y_list.append(cause_of_death)

    return cod_y_list


def PresentGraph(idata_list, istart_month, istart_year, iend_month, iend_year):

    # Generate a subtitle for the month range (e.g. 'June 2020 to March 2021')
    start_month = IntegerToMonth(istart_month)
    end_month = IntegerToMonth(iend_month)
    start_year = str(istart_year)
    end_year = str(iend_year)

    if (start_month == end_month) and (start_year == end_year):
        subtitle = start_month + start_year
    else:
        subtitle = start_month + " " + start_year + ' to ' + end_month + " " + end_year


    # Create X and Y lists using idata_list
    length = len(idata_list)
    xlist = range(1, length + 1)

    ylists = []

    ylist_cases = []
    ylists.append(ylist_cases)

    ylist_deaths = []
    ylists.append(ylist_deaths)

    ylist_hospital_admissions = []
    ylists.append(ylist_hospital_admissions)

    ylist_ventilator_beds = []
    ylists.append(ylist_ventilator_beds)

    for date in idata_list:
        ylist_cases.append(date[4])
        ylist_deaths.append(date[5])
        ylist_hospital_admissions.append(date[6])
        ylist_ventilator_beds.append(date[7])
    

    # Calculate highest Y value
    highest_value = 0
    for i in ylists:
        for j in i:
            if j > highest_value:
                highest_value = j
    print('Highest Y value:', highest_value)


    # Add 2018 averages
    average = createAverageLine(xlist, round(deaths_2018 / 365))
    cancer = createAverageLine(xlist, round(deaths_2018_cancer / 365))
    dementia = createAverageLine(xlist, round(deaths_2018_dementia / 365))
    cvd = createAverageLine(xlist, round(deaths_2018_cvd / 365))


    ### Present plots ###

    # Define stlying
    pyplot.style.use('seaborn-poster')
    """
    Solarize_Light2
    _classic_test_patch
    bmh
    classic
    dark_background
    fast
    fivethirtyeight
    ggplot
    grayscale
    seaborn
    seaborn-bright
    seaborn-colorblind
    seaborn-dark
    seaborn-dark-palette
    seaborn-darkgrid
    seaborn-deep
    seaborn-muted
    seaborn-notebook
    seaborn-paper
    seaborn-pastel
    seaborn-poster
    seaborn-talk
    seaborn-ticks
    seaborn-white
    seaborn-whitegrid
    tableau-colorblind10
    """

    # Average deaths plots
    pyplot.plot(xlist, average, label='Average total (2018)', linestyle='--', color='blue')
    pyplot.plot(xlist, cancer, label='Cancer (2018)', linestyle='--', color='green')
    pyplot.plot(xlist, dementia, label='Dementia (2018)', linestyle='--', color='brown')
    pyplot.plot(xlist, cvd, label='Heart Disease (2018)', linestyle='--', color='navy')

    # Cases plot
    #pyplot.plot(xlist, ylist_cases, label = "Daily Cases", color = "blue")

    # Deaths plot
    pyplot.plot(xlist, ylist_deaths, label = 'COVID-19', color = 'red')

    # Hospital line plots
    '''
    pyplot.plot(xlist, ylist_hospital_admissions, label = "Hospital Admissions", color = "green")
    pyplot.plot(xlist, ylist_ventilator_beds, label = "Vent", color = "orange")
    '''

    #pyplot.title("Cases vs Deaths", fontsize=20)
    #pyplot.title("Cases", fontsize=20)
    
    pyplot.suptitle('Daily Reported COVID-19 Deaths', fontsize=20)
    pyplot.title(subtitle)
    pyplot.xlabel('Days')
    pyplot.axis([1, length, 0, 1500])
    #pyplot.autumn()
    pyplot.grid()
    pyplot.legend()
    pyplot.show()


def PresentScatter(idata_list, istart_month, istart_year, iend_month, iend_year):

    # Note. This graph works best when comparing two results: March to June, and July to September (both in 2019)

    '''
    # Remove data outside of March to June
    title = "Cases vs Deaths:\nMarch to June"
    to_remove = []

    for date in idata_list:
        if date[1] < 3 or date[1] > 6:
            to_remove.append(date)
    
    for i in to_remove:
        idata_list.remove(i)

    #print(idata_list)
    '''


    # Remove data outside of July to September
    title = "Cases vs Deaths:\nJuly to September"
    to_remove = []

    for date in idata_list:
        if date[1] < 7 or date[1] > 9:
            to_remove.append(date)
    
    for i in to_remove:
        idata_list.remove(i)

    #print(idata_list)



    xlist = []
    ylist = []

    for date in idata_list:
        # Append daily cases
        xlist.append(date[4])

        # Append daily deaths
        ylist.append(date[5])
    
    # Calculate highest Y value
    highest_y_value = ylist[0]
    for i in ylist:
        if i > highest_y_value:
            highest_y_value = i
    
    # Calculate highest and lowest X values
    highest_x_value = xlist[0]
    lowest_x_value = xlist[0]
    for i in xlist:
        if i > highest_x_value:
            highest_x_value = i
        if i < lowest_x_value:
            lowest_x_value = i


    # Create linear regression line
    coef = numpy.polyfit(xlist, ylist, 1)
    poly_1d_func = numpy.poly1d(coef)
    # poly1d_func is now a function which takes in x and returns an estimate for y

    # # # # # # # # # # # # # # # # # # # # # # # #
    # Workaround for line not displaying properly #
    # # # # # # # # # # # # # # # # # # # # # # # #
    # Create a pair of lists, each with two items, so the linear regression line plot looks cleaner
    temp_list = poly_1d_func(xlist)
    highest_1d_value = temp_list[0]
    lowest_1d_value = temp_list[0]
    for i in temp_list:
        if i > highest_1d_value:
            highest_1d_value = i
        if i < lowest_1d_value:
            lowest_1d_value = i

    #pyplot.plot(xlist, poly_1d_func(xlist), dashes=[2,6], lw='2', color='pink')
    pyplot.plot([lowest_x_value, highest_x_value], [lowest_1d_value, highest_1d_value], linestyle='--', color='orange')


    # Draw the rest of the graph
    pyplot.title(title, fontsize=16)
    pyplot.xlabel("Daily Cases")
    pyplot.ylabel("Daily Deaths")

    pyplot.scatter(highest_x_value, highest_y_value, color='white')
    pyplot.scatter(xlist, ylist, label='Wee', marker='x')

    pyplot.xlim(1, (highest_x_value * 1.05))
    pyplot.ylim(0, (highest_y_value * 1.05))
    #pyplot.axes([0, 6000, 0, 1000])
    
    pyplot.show()



# 0. Download CSV from coronavirus.data.gov.uk
csv_output = downloadCSV()

# 1. Create and save online data to a CSV
saveCSV(csv_output, csv_path)

# 2. Read data into Python from the saved CSV
data = readData(csv_path)
#print(data)

# 3. Present the data using matplotlib
PresentGraph(data, 3, 2020, 4, 2021)
#PresentScatter(data, 3, 12)


# # # # #
# To Do #
# # # # #

# DONE: Split data into March-June and July-September, to distinguish between before and after mass testing

# DONE: Improve PresentScatter to use the same size X and Y axes for both plots
# Achieved by entering a false data point which is white

# DONE: When downloading a new CSV, delete the dates with no death data, to avoid an IndexError: list index out of range
# Achieved by reversing the final list (so earliest dates are first) then removing the first 60 dates (between 03/01/20 
# and 01/03/20) as they have no death values

# DONE: Daily deaths from all causes
# To show what proportion of deaths are classified as COVID (as a separate project)

# Add dates at the bottom instead of simply 'Days':
# This can be done, apparently (see https://matplotlib.org/stable/gallery/text_labels_and_annotations/date.html)

# Add Testing Capacity plot:
# Cases vs Testing correlation - show the relationship between case numbers and testing capacity (for July to September)

# Hospital admission:
# Perhaps a separate Present(...) function to show the correlation (or lack thereof) between hospital
# admission and mechanical ventilator bed usage. Additionally, I should add some average lines from 2019, to show typical
# hospital admission for other things (diabetes, injury, heart attacks etc.)
# Note. The information for admission on a per category basis is stored separately from coronavirus.gov.uk - it's with NHS 
# Digital, who have their own API:
# https://digital.nhs.uk/developer 
# I might have to do a seperate program for this. It would also be fun to parse their other data.

# Five-year daily average:
# Used to show the variations that occur with the seasons