import geopandas as gp
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.optimize import curve_fit
import numpy as np

gp_fp="Racial_and_Social_Equity_Composite_Index_Current (1).geojson"
gp_df=gp.read_file(gp_fp)


gp_df.plot(color='white',edgecolor='black')
plt.show()


#Ideas for tidying this data set:
#I can turn quantile into a number scale this will help with analysis later. 
#So for Health Disadvantage Quintile/HEALTH_DISADV_QUINTILE there are 5 rankings : most disadvantaged, lowest, midlle ...
#Lets call give these quantiles a number say 0,1,2,3,4 . 
#If this type of encoding works we can copy the method for all data 


Quantile_cols=['HEALTH_DISADV_QUINTILE','SOCIOECON_DISADV_QUINTILE']
for i in Quantile_cols:
    dict={"Highest Equity Priority/Most Disadvantaged":0,"Second Highest":1,"Middle":2,"Second Lowest":3,
               "Lowest":4}
    gp_df[i]=gp_df[i].map(dict)
    print(gp_df[i])


#so that worked for HEALTH_DISADV_QUINTILE let's try to do this for all the columns

remaining_Quantile_cols=["RACE_ELL_ORIGINS_QUINTILE","COMPOSITE_QUINTILE"]
for i in remaining_Quantile_cols:
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
#dropping columns to remove irrelvant info
gp_df_clean = gp_df.drop(['SHAPE_Length', 'TRACT','NAMELSAD','ACRES_TOTAL','OBJECTID'], axis=1)

pd.set_option('display.max_columns',None)
print(gp_df_clean.head())

#making the HI score
gp_df_clean["HI_score"]=((gp_df_clean["PCT_ADULT_WITH_OBESITY"]+gp_df_clean["PCT_ADULT_MENTALHLTHNOTGOOD"]+gp_df_clean["PCT_ADULT_WITH_ASTHMA"]+gp_df_clean["PCT_ADULT_WITH_DISABILITY"])/5)
print(gp_df_clean["HI_score"])

#plotting socail/HI score

list_int=["HI_score","POP_5_YRS_AND_OLDER","PTL_ADULT_NOLEISUREPHYSACTIV","PTL_LESS_BACHELOR_DEGREE"]

fig_1,axs_1=plt.subplots(nrows=2,ncols=2,figsize=(15,15))
axs_1=axs_1.flatten()

for i in list_int:
    gp_df_clean.plot(ax=axs_1[(list_int.index(i))], column=i,cmap='hot_r',legend=True,edgecolor='black')
    axs_1[(list_int.index(i))].set_title(i)
    axs_1[(list_int.index(i))].axis('off')
plt.show()

#how about we use scatter plots for visulisation

fig_2,axs_2=plt.subplots(nrows=2,ncols=3,figsize=(35,15))
axs_2=axs_2.flatten()

list_int_min=["POP_5_YRS_AND_OLDER","PTL_ADULT_NOLEISUREPHYSACTIV","PTL_LESS_BACHELOR_DEGREE"]

for i in list_int_min:
    sns.regplot(ax=axs_2[(list_int_min.index(i))],fit_reg=True,x="HI_score",y=i,data=gp_df_clean,order=2)
    sns.residplot(ax=axs_2[(list_int_min.index(i))+3],x="HI_score",y=i,data=gp_df_clean,order=2)
    axs_2[(list_int_min.index(i))].set_title(i)
    axs_2[(list_int_min.index(i))+3].set_title('residual plot for abouve figure')
    axs_2[(list_int_min.index(i)) + 3].set_ylabel("residual")
plt.show()

#finding out the mean absaloute error of the fit

def second_order(x,c,m1,m2):
    return c+m1*x+m2*x**2

for i in list_int_min:
    np_HV=gp_df_clean["HI_score"].values
    pars,cov=(curve_fit(second_order,np_HV,gp_df_clean[i].values))
    Fit=(second_order(np_HV,pars[0],pars[1],pars[2]))
    res=np_HV-Fit
    sqr_error=res**2
    mean_squared_error=np.mean(sqr_error)
    print('the mean squared error against the second order fit was', mean_squared_error, 'for the column',i)

# investigating how wealth affects health disadvantage.

wealth_list=["PTL_POP_UNDER200PCT_POVERTY", "HEALTH_DISADV_SCORE"]
fig_3,axs_3=plt.subplots(nrows=2,ncols=2,figsize=(15,15))
axs_3=axs_3.flatten()

#1,2 maps
#4th box plot
box_df=gp_df_clean[["PTL_POP_UNDER200PCT_POVERTY", "HEALTH_DISADV_SCORE"]]
box_melt_df=pd.melt(box_df)
#3rd scatter plot

for i in wealth_list:
    gp_df_clean.plot(ax=axs_3[(wealth_list.index(i))], column=i, cmap='Blues', legend=True,edgecolor='black')
    axs_3[(wealth_list.index(i))].set_title(i)
    axs_3[(wealth_list.index(i))].axis('off')
sns.regplot(ax=axs_3[2],fit_reg=True,x=wealth_list[0],y=wealth_list[1],data=gp_df_clean)
axs_3[2].set_title("Scatter Plot")
sns.boxplot(ax=axs_3[3],x='variable',y='value',data=box_melt_df,color=".8", linecolor="#137", linewidth=.75)
axs_3[3].set_title("Box Plot")
plt.show()

sns.set(rc={'figure.figsize':(11.7,8.27)})
AX=sns.scatterplot(x=wealth_list[0],y=wealth_list[1],data=gp_df_clean,
                hue="RACE_ELL_ORIGINS_QUINTILE",size="RACE_ELL_ORIGINS_QUINTILE",
                sizes=(50,150))
legend_handles, _=AX.get_legend_handles_labels()
AX.legend(legend_handles,["Highest Equity Priority", "Second Highest", "Middle", "Second Lowest",
                 "Lowest"],bbox_to_anchor=(1,1),title="legend")
plt.xlabel('Health Disadvantage Score')
plt.ylabel('Percentage of population under 200% of poverty level')
plt.show()

axs_4=sns.swarmplot(data=gp_df_clean,x="RACE_ELL_ORIGINS_QUINTILE",y="SOCIOECON_DISADV_PERCENTILE",hue="HEALTH_DISADV_QUINTILE")
plt.show()


