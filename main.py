import geopandas as gp
import matplotlib.pyplot as plt

gp_fp="Racial_and_Social_Equity_Composite_Index_Current (1).geojson"
gp_df=gp.read_file(gp_fp)
print(gp_df)

gp_df.plot(column="POP_5_YRS_AND_OLDER")
plt.show()

'''
Ideas for tidying this data set:
I can turn quantile into a one hot encoded problem where each quantile is turned into a number scale. 
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

