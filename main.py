import geopandas as gp
import matplotlib.pyplot as plt
import pandas as pd


gp_fp="Racial_and_Social_Equity_Composite_Index_Current (1).geojson"
gp_df=gp.read_file(gp_fp)


gp_df.plot(color='white',edgecolor='black')
plt.show()

'''
Ideas for tidying this data set:
I can turn quantile into a number scale this will help with analysis later. 
So for Health Disadvantage Quintile/HEALTH_DISADV_QUINTILE there are 5 rankings : most disadvantaged, lowest, midlle ...
Lets call give these quantiles a number say 0,1,2,3,4 . 
If this type of encoding works we can copy the method for all data 
'''

Quantile_cols=['HEALTH_DISADV_QUINTILE','SOCIOECON_DISADV_QUINTILE']
for i in Quantile_cols:
    gp_df[i].replace('Highest Equity Priority/Most Disadvantaged',0,inplace=True)
    gp_df[i].replace('Lowest',4,inplace=True)
    gp_df[i].replace('Middle',2,inplace=True)
    gp_df[i].replace('Second Highest',1,inplace=True)
    gp_df[i].replace('Second Lowest',3,inplace=True)
    print(gp_df[i])


'''so that worked for HEALTH_DISADV_QUINTILE let's try to do this for all the columns'''

remaining_Quantile_cols=["RACE_ELL_ORIGINS_QUINTILE","COMPOSITE_QUINTILE"]
for i in remaining_Quantile_cols:
    gp_df[i].replace('Highest Equity Priority', 0, inplace=True)
    gp_df[i].replace('Lowest', 4, inplace=True)
    gp_df[i].replace('Middle', 2, inplace=True)
    gp_df[i].replace('Second Highest', 1, inplace=True)
    gp_df[i].replace('Second Lowest', 3, inplace=True)
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

fig,axs=plt.subplots(nrows=2,ncols=2,figsize=(25,25))
axs=axs.flatten()

for i in list_int:
    gp_df_clean.plot(ax=axs[(list_int.index(i))], column=i,cmap='hot_r',legend=True)
    axs[(list_int.index(i))].set_title(i)
    axs[(list_int.index(i))].axis('off')
plt.show()


