import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('fatalities.csv')

#Reading the details of the data and its attributes
print("--------------------Data before Cleaning--------------------")
print(data.info())

#removing the column with null values more than 25% of the total data 
for col in data.columns:
    per = (data[col].isnull().sum()/data.shape[0])
    if per >= 0.25:
        print(col)
        data.drop([col],axis=1,inplace=True)

#Notes column is unnecessary for the visualization
data.drop("notes", inplace=True, axis=1)
print("--------------------Data after Cleaning--------------------")
print(data.info())


#Converting the date_of_events and date_of_deaths column to pandas datetime format
data['date_of_event'] = pd.to_datetime(data['date_of_event'])
data['date_of_death'] = pd.to_datetime(data['date_of_death'])

#isarlie an dpalestinian data
israeli_data = data[data["citizenship"] == "Israeli"]
palestinian_data = data[data["citizenship"] == "Palestinian"]

#PLOTS FUNCTIONS
#LINE PLOT
def plot_line(data, mark, title, xlabel, ylabel, name):
    '''
      saves and displays a line plot
      can be used to plot multi line plot by giving list of lists 

    Parameters
    ----------
    data : list containig x y and name  or list of lists containig x y and name
        takes dafarmae with columns for line plot.
    mark : type of marker 
        generally its is star or dot to represent data.
    title : String
        Title of the line plot.
    xlabel : string
        name of x axis
    ylabel : string
        name of y axis
        
    name : string
        name of png file .

    Returns
    -------
    None.

    '''
    plt.figure(figsize=(16, 8))
    for i in range(len(data)):    
        x=data[i][0]
        y=data[i][1]
        lbl = data[i][2]
        plt.plot(x, y, marker=mark,label=lbl)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.savefig(name)
    plt.show()
    

    
#BAR PLOT
def plot_bar(x, y, clr, title, xlabel, ylabel, name):
    '''
    To plot a bar graph and save it as png image

    Parameters
    ----------
    x : List/array
        INDEX 
    y : List/array
        VALUES/COUNNTS.
    clr : string
        Colour.
    title : string
        Title of the plot.
     xlabel : string
         name of x axis
     ylabel : string
         name of y axis
         
     name : string
         name of png file .

    Returns
    -------
    None.

    '''
    plt.figure(figsize=(16, 6))
    plt.bar(x, y, color=clr)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(name)
    plt.show()   

#SCATTER PLOT
def get_eventvdeath(data,name):
    '''
    generates a scatter plot 

    Parameters
    ----------
    data : dataframe 
        dataframe consisting columns to .
    name : string
        name of png file .

    Returns
    -------
    None.

    '''
    plt.figure(figsize=(16, 8))
    data['date_of_event'].value_counts().sort_index().plot(color='red', linestyle='solid')
    data['date_of_death'].value_counts().sort_index().plot(color='blue', linestyle='dotted')
    plt.title('Events and Deaths Over Time')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.legend()
    plt.savefig(name)
    plt.show()
    
#PIE CHART
def plot_pie(dx, dy, name):
    '''
    

    Parameters
    ----------
    dx : list
        
    dy : list
    
    name : string
        name of png file 
        
    Returns
    -------
    None.

    '''
    plt.figure(figsize=(7, 7))
    plt.pie(x=dx, labels=dy, autopct='%1.2f%%')
    plt.legend()
    plt.savefig(name)
    plt.show()   
     
     
          

#1 . Line plot for fatalities by year

fatality_by_year = data.groupby(data['date_of_event'].dt.year).size().reset_index(name='fatalities')  
fatality_total = [
                    [fatality_by_year['date_of_event'], fatality_by_year['fatalities'], 'Total']
                 ]

plot_line(fatality_total, '.', 'Fatality Trends from 2000 to 2023', 'Year', 'Number of Fatalities', 'fatality_per_year.png')





#2 . multi line plot year wise deaths of Israelis vs Palestinians

fatality_by_year_is = israeli_data.groupby(israeli_data['date_of_event'].dt.year).size().reset_index(name='fatalities')
fatality_by_year_pal = palestinian_data.groupby(palestinian_data['date_of_event'].dt.year).size().reset_index(name='fatalities')
fatality= [
            [fatality_by_year_is['date_of_event'], fatality_by_year_is['fatalities'], 'ISRAEL'],
            [fatality_by_year_pal['date_of_event'], fatality_by_year_pal['fatalities'], 'PALESTINE']
          ]
plot_line(fatality, '.', 'Fatality Trends from 2000 to 2023', 'Year', 'Number of Fatalities', 'fatalit_IsrvPls.png')




#3. Bar plot for high fatality event locations 

#----------------Considering 12 locations with highest fatalities------------------------
isr = israeli_data["event_location_district"].value_counts().head(12)
pls = palestinian_data["event_location_district"].value_counts().head(12)
plot_bar(isr.index, isr.values, 'blue', 'Isralie Count', 'Location', 'Count of fatalities', 'Israeli_count.png')
plot_bar(pls.index, pls.values, 'orange', 'Palestinian Count', 'Location', 'Count of fatalities', 'Palestinian_count.png')




#4 scatter plot events vs death 
get_eventvdeath(data,'eventsvsdeath.png')




#5 Pie Chart representing the distribution of fatalities by their citizenships
plot_pie(data['citizenship'].value_counts().values, data['citizenship'].value_counts().index, 'Pie_Chart_fatalities')


