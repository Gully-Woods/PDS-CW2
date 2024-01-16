#import relevant functions
import geopandas as gp
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.optimize import curve_fit
import numpy as np

# create a file path and read the geojson file
gp_fp="Racial_and_Social_Equity_Composite_Index_Current (1).geojson"
gp_df=gp.read_file(gp_fp)

# create a plot of the borders of Seattle to test the geojson file
gp_df.plot(color='white',edgecolor='black')
# save the figure to a png in our dictonary and show the plot
plt.savefig('Seattle_Outline.png')
plt.show()

'''I can turn quantile into a number scale this will help with analysis later.Say for Health Disadvantage each quantile
can be mapped onto a dictonary that converts the string into a interger.'''

# list the columns of intrest with the same catagories names
Quantile_cols=['HEALTH_DISADV_QUINTILE','SOCIOECON_DISADV_QUINTILE']
for i in Quantile_cols:
    # create a dictonary so that we can give these values some abitary seperating numerical meaning
    dict={"Highest Equity Priority/Most Disadvantaged":0,"Second Highest":1,"Middle":2,"Second Lowest":3,
               "Lowest":4}
    # map the values for each column to the dictonary
    gp_df[i]=gp_df[i].map(dict)
    # print the outputs just to check that we now have a interger column
    print(gp_df[i])
# let's try this for the rest of our discrete quantile columns
remaining_Quantile_cols=["RACE_ELL_ORIGINS_QUINTILE","COMPOSITE_QUINTILE"]
for i in remaining_Quantile_cols:
    # the dictonary is slightly different becuase the names of some of the strings have changed
    dict={"Highest Equity Priority":0 , "Second Highest":1, "Middle":2, "Second Lowest":3,
                 "Lowest":4}
    gp_df[i]=gp_df[i].map(dict)
    print(gp_df[i])

'''
-we could see how health is being affected by social and economical factors
-we make a health score that is not a 'disadvantage score' we can call these health issues
-HI's=Diagnosed diabetes,Obesity,Mental health not good,Asthma and Disability colms
-this will exclude the No leisure-time physical activity and Low life expectancy at birth colms as these puts an
individual at disavantange but we want to see how directly it relates to know issues
- To investigate if certain groups of people have been places at a disavantage we should relate this to the disadvantage 
index
'''
# dropping columns to remove irrelvant info
gp_df_clean = gp_df.drop(['SHAPE_Length', 'TRACT','NAMELSAD','ACRES_TOTAL','OBJECTID','GEOID','SHAPE_Area','TRACTCE'], axis=1)
# print all the new columns so that we can see them
pd.set_option('display.max_columns',None)
print(gp_df_clean.head())
# making the HI score
gp_df_clean["HI_score"]=((gp_df_clean["PTL_ADULT_WITH_OBESITY"]+gp_df_clean["PTL_ADULT_MENTALHLTHNOTGOOD"]+gp_df_clean[
"PTL_ADULT_WITH_ASTHMA"]+gp_df_clean["PTL_ADULT_WITH_DISABILITY"])/5)
print(gp_df_clean["HI_score"])

# plotting Social factors against Health Indicators

# make a list of social factors
list_int=["HI_score","POP_5_YRS_AND_OLDER","PTL_ADULT_NOLEISUREPHYSACTIV","PTL_LESS_BACHELOR_DEGREE"]
readable_titles=["Bad health inidicators (percentile)","Population over 5",
                 "Adults with no leisure activity (percentile)","Education less than degree (percentile)"]
# I want to make plot a chloropleth map of Seattle with subplots for all the different social issues
fig_1,axs_1=plt.subplots(nrows=2,ncols=2,figsize=(15,15))
# This will make it possible to loop through the list and indicate positions
axs_1=axs_1.flatten()
for i in list_int:
    # A variable to give a value of how far through the list we are
    pos=(list_int.index(i))
    # make a plot by itterating through the list
    gp_df_clean.plot(ax=axs_1[pos], column=i,cmap='hot_r',legend=True,edgecolor='black')
    # give the plots readable titles
    axs_1[pos].set_title(readable_titles[pos])
    axs_1[pos].axis('off')
plt.savefig('Chloropleth_Social.png')
plt.show()

# how about we use scatter plots for comparision
fig_2,axs_2=plt.subplots(nrows=2,ncols=3,figsize=(35,15))
axs_2=axs_2.flatten()
list_int_min=["POP_5_YRS_AND_OLDER","PTL_ADULT_NOLEISUREPHYSACTIV","PTL_LESS_BACHELOR_DEGREE"]
readable_titles_min=["Population over 5","Adults with no leisure activity (percentile)",
                     "Education less than degree (percentile)"]
for i in list_int_min:
    # set a position variable
    pos=(list_int_min.index(i))
    # a second order regression plot comparing all indicators against health indiactors
    sns.regplot(ax=axs_2[pos],fit_reg=True,x="HI_score",y=i,data=gp_df_clean,order=2)
    # a residual plot so that we can visually see how well the data fits against the second order regression
    sns.residplot(ax=axs_2[pos+3],x="HI_score",y=i,data=gp_df_clean,order=2)
    # set titles for the first three regression plots
    axs_2[pos].set_title('Regression plot')
    axs_2[pos].set_ylabel(readable_titles_min[pos])
    axs_2[pos].set_xlabel(readable_titles[0])
    # set titles for the next residual plots
    axs_2[pos+3].set_title('Residual plot')
    axs_2[pos + 3].set_ylabel("Residuals")
    axs_2[pos + 3].set_xlabel(readable_titles[0])
# plot and save the subplots as a png
plt.savefig('Social_Regression.png')
plt.show()

'''I think it would be interesting to find a mean abs error for this fit. The way I know how to do this is by defining 
a function for the second order and using scipy to see how this regression fits with the residuals of the columns as 
numpy arrays'''

# defining the second order func
def second_order(x,c,m1,m2):
    return c+m1*x+m2*x**2
# make a loop for all social values
for i in list_int_min:
    # it will be important to have all my columns as numpy arrays
    np_HV=gp_df_clean["HI_score"].values
    # return values using scipy for the second order regression values for each social issue
    pars,cov=(curve_fit(second_order,np_HV,gp_df_clean[i].values))
    # Fit these values to a new variable
    Fit=(second_order(np_HV,pars[0],pars[1],pars[2]))
    # find the residuals
    res=np_HV-Fit
    # print the mean squared error for each social issue to see if the fit is any good
    sqr_error=res**2
    mean_squared_error=np.mean(sqr_error)
    print('the mean squared error against the second order fit was', mean_squared_error, 'for the column',i)

# investigating how wealth affects health disadvantage.
# we can use population under poverty act as an indicator of wealth
wealth_list=["PTL_POP_UNDER200PCT_POVERTY", "HEALTH_DISADV_SCORE"]
wealth_list_readable=["population under 200% poverty(percentile)","Health disadvantage score"]
# Lets make some subplots to investigate this relationship
fig_3,axs_3=plt.subplots(nrows=2,ncols=2,figsize=(15,15))
axs_3=axs_3.flatten()
# The last plot will be a box plot, we need to use the melt function on the two relevant columns
box_df=gp_df_clean[["PTL_POP_UNDER200PCT_POVERTY", "HEALTH_DISADV_SCORE"]]
box_melt_df=pd.melt(box_df)
for i in wealth_list:
    # set a position variable
    pos=(wealth_list.index(i))
    # the first two plots will be chloropleths of Seatle
    gp_df_clean.plot(ax=axs_3[pos], column=i, cmap='Blues', legend=True,edgecolor='black')
    # the title of each plot should be relevant
    axs_3[pos].set_title(wealth_list_readable[pos])
    axs_3[pos].axis('off')
# only one subplot (can be outside loop) this time lets make the regression first order
sns.regplot(ax=axs_3[2],fit_reg=True,x=wealth_list[0],y=wealth_list[1],data=gp_df_clean)
# set relevant titles for regression plot
axs_3[2].set_title("First Order Regression Plot")
axs_3[2].set_ylabel(wealth_list_readable[1])
axs_3[2].set_xlabel(wealth_list_readable[0])
# define box plot with special themes
sns.boxplot(ax=axs_3[3],x='variable',y='value',data=box_melt_df,color=".8", linecolor="#137", linewidth=.75)
# set titles for box plot
axs_3[3].set_title("Box Plot")
# Plot and save the figure to a png
plt.savefig('SUBPLOTS_ECON.png')
plt.show()

# Let's make a scatter plot of these economical issues against wealth
# Set parameters for Seaborn
sns.set(rc={'figure.figsize':(11.7,8.27)})
# Define the scatterplot also investigating race and peoples origin
AX=sns.scatterplot(x=wealth_list[0],y=wealth_list[1],data=gp_df_clean,
                hue="RACE_ELL_ORIGINS_QUINTILE",size="RACE_ELL_ORIGINS_QUINTILE",
                sizes=(50,150))
# Lets define the legend more specifical to set position and also control the output so that they are not just
# incomprehensable numbers
legend_handles, _=AX.get_legend_handles_labels()
AX.legend(legend_handles,["Highest Equity Priority", "Second Highest", "Middle", "Second Lowest",
                 "Lowest"],bbox_to_anchor=(1,1),title="Race/Origins Quantile")
# define the labels
plt.xlabel('Health Disadvantage Score')
plt.ylabel('Percentile of population under 200% of poverty level')
plt.savefig('SCATTER_ECON.png')
plt.show()

# Let us investigate race and origin further by investigating the relationship wiht a swarmplot against social economic
# disadvantage we can also create a different 'hue' for social healdisadvantage
axs_4=sns.swarmplot(data=gp_df_clean,x="RACE_ELL_ORIGINS_QUINTILE",y="SOCIOECON_DISADV_PERCENTILE",hue="HEALTH_DISADV_QUINTILE")
axs_4.legend(legend_handles,["Highest Equity Priority/Most Disadvantaged", "Second Highest", "Middle", "Second Lowest",
                 "Lowest"],title="Health Disadvantage Quantile")
#define the labels
plt.xlabel('Race ')
plt.ylabel('Percentile of population under 200% of poverty level')
# plot the figure and save as a png
plt.savefig('SWARM_ECON.png')
plt.show()

# investigating data distributions
pop=gp_df_clean["POP_5_YRS_AND_OLDER"].values
x=np.linspace(1000,7000,500)
# import relevant modulus
from scipy.stats import norm
# fit a normal distribution to the data
mu_p,sigma_p=norm.fit(pop)
# plot a histagram and the fit
plt.hist(pop,35,density=True,label='histogram true')
plt.plot(x,norm.pdf(x,mu_p,sigma_p),label='normal fit')
plt.xlabel('Population 5 years and older')
plt.ylabel('density')
plt.legend()
plt.savefig('hist_fit.png')
plt.show()
# print the mean and standard deveation
print('population average=',"%.3g" %mu_p)
print('population standard devation=',"%.3g" %sigma_p)

fig_5,axs_5=plt.subplots(nrows=1,ncols=3,figsize=(14,4))
inter_list_2= ["PTL_POP_UNDER200PCT_POVERTY","PTL_ADULT_NOLEISUREPHYSACTIV","PTL_LESS_BACHELOR_DEGREE"]
readable_inter_list_2=["Percentile of population under 200% poverty","Percentile adults with no leisure or physical"
                                                                     "activity","Percentile with less than degree"]
for i in inter_list_2:
    # set a position variable
    pos = (inter_list_2.index(i))
    # kendal density plot
    sns.kdeplot(ax=axs_5[pos], data=gp_df_clean[i], legend=True)
    # set axis titles
    axs_5[pos].set_ylabel("Density")
    axs_5[pos].set_xlabel(readable_inter_list_2[pos])

plt.savefig('kend_dens.png')
plt.show()

