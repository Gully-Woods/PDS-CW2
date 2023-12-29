import pandas as pd
import geopandas as gp
import matplotlib.pyplot as plt

gp_fp="Racial_and_Social_Equity_Composite_Index_Current (1).geojson"
gp_df=gp.read_file(gp_fp)
print(gp_df)

gp_df.plot(column="POP_5_YRS_AND_OLDER")
plt.show()
