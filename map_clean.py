import tools
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
from astropy.table import Table



parameters = tools.parameters("/Users/ashiriagoel/Documents/surf2024/param_defaults.py")
input = "/Users/ashiriagoel/Downloads/co2_s12_v5_take6_n5_subtr_exper.h5"

map_output = tools.maps(parameters, inputfile=input, reshape=True).map
map_obj=tools.maps(parameters, inputfile=input, reshape=True)

freq_avg = np.nanmean(map_output, axis=0)
np.set_printoptions(threshold=np.inf)

fig, ax = plt.subplots()
ax.pcolormesh(map_obj.rabe, map_obj.decbe, freq_avg)

# for row in freq_avg
Y, X = np.where(np.isnan(freq_avg) == False)
max_x = np.max(X)
min_x = np.min(X)
max_y = np.max(Y)
min_y = np.min(Y)

# 40 80 21 97

print(min_x)
print(max_x)
print(min_y)
print(max_y)



min_dec = map_obj.dec[min_y]
min_ra = map_obj.ra[min_x]
max_dec = map_obj.dec[max_y]
max_ra = map_obj.ra[max_x]

rect_width = max_ra - min_ra 
rect_height = max_dec - min_dec

rect = patches.Rectangle((min_ra, min_dec), rect_width, rect_height, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)



print("min_dec = " + str(min_dec))
print("min_ra = " + str(min_ra))
print("max_dec = " + str(max_dec))
print("max_ra = " + str(max_ra))


tab = Table.read('/Users/ashiriagoel/Downloads/comap_field1.dat', format='ascii')
df = tab.to_pandas()
cut_df = df.query('line_id == "Lya"')
cut_df = cut_df.query('sn > 6.0')
cut_df = cut_df.query('z_hetdex > 2.4')
cut_df = cut_df.query('z_hetdex < 3.4')
cut_df = cut_df.query('RA > 24.16833333333335')
cut_df = cut_df.query('RA < 26.701666666666668')
cut_df = cut_df.query('DEC > -0.6666666666666288')
cut_df = cut_df.query('DEC < 0.6666666666666856')
cut_df = cut_df.query('apcor > 0.6')
cut_df = cut_df.query("source_type=='lae' | source_type=='agn'")
cut_df = cut_df.drop_duplicates(subset = ['RA', 'DEC'])


print(cut_df)
cut_df.to_csv('/Users/ashiriagoel/Documents/surf2024/field_1_sorted_data.csv', index=False)

ra_vals = cut_df.RA.tolist()
dec_vals = cut_df.DEC.tolist()

ax.scatter(ra_vals, dec_vals)
plt.show()


