# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 09:20:49 2017

@author: juan.betancur53
"""
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa',
          'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama',
          'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 
          'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 
          'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 
          'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii',
          'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana',
          'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam',
          'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 
          'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands',
          'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 
          'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 
          'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 
          'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 
          'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 
          'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 
          'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 
          'ND': 'North Dakota','VA': 'Virginia'}
#%%
def get_list_of_university_towns():
    u_t_df=pd.DataFrame(columns=["State","RegionName"])
        
    with open("university_towns.txt",encoding='utf-8') as f:
        lines=f.readlines()
        lines = [x.strip() for x in lines]
        for line in lines:
            f_State=line.find("[edit]")
            if f_State!=-1:
                State=line[:f_State]
            else:
                RegionName=line
                u_t_df=u_t_df.append({"State":State,"RegionName":RegionName},ignore_index=True)
    u_t_df["RegionName"]=u_t_df["RegionName"].str.replace(r"\s+\(.*","")
    u_t_df["RegionName"]=u_t_df["RegionName"].str.replace(r"\[.*\]","")
    return u_t_df
#%%
def get_gdp():
    gdp_df=pd.read_excel("gdplev.xls",
                         sheetname="Sheet1",
                         header=None,
                         skiprows=220,
                         parse_cols="E,G",
                         names=["Year-Quarter","Chained 2009 Dollars"])
    gdp_df=gdp_df.set_index("Year-Quarter")
    gdp_df["diff"]=gdp_df.diff()>0
    gdp_df["diff"]=gdp_df["diff"].astype("int")
    return gdp_df
#%%
def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    gdp_df=get_gdp()
    string="".join(map(str,gdp_df["diff"].values))
    pattern="0011"
    ind_pattern=string.index(pattern)
    start_ress=string.rindex("1",0,ind_pattern)
    return gdp_df.index[start_ress]
get_recession_start()
#%%
def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    gdp_df=get_gdp()
    string="".join(map(str,gdp_df["diff"].values))
    pattern="0011"
    ind_pattern=string.index(pattern)
    end_ress=ind_pattern+len(pattern)-1
    return gdp_df.index[end_ress]
get_recession_end()
#%%
def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    gdp_df=get_gdp()
    string="".join(map(str,gdp_df["diff"].values))
    pattern="0011"
    ind_pattern=string.index(pattern)
    start_ress=string.rindex("1",0,ind_pattern)+1
    end_ress=ind_pattern+len(pattern)-1
    bottom_ress=gdp_df["Chained 2009 Dollars"].iloc[start_ress:end_ress+1].idxmin()
    return bottom_ress
get_recession_bottom()
#%%
def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa',
          'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama',
          'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 
          'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 
          'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 
          'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii',
          'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana',
          'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam',
          'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 
          'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands',
          'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 
          'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 
          'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 
          'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 
          'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 
          'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 
          'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 
          'ND': 'North Dakota','VA': 'Virginia'}
    
    housing_df=pd.read_csv("City_Zhvi_AllHomes.csv",index_col=["State","RegionName"])
    housing_df=housing_df[pd.date_range("2000-01","2016-09",freq="M").strftime("%Y-%m")]
    housing_df.columns = pd.to_datetime(housing_df.columns).to_period("m")
    housing_df=housing_df.resample("q",axis=1).mean()
    housing_df.columns=housing_df.columns.strftime('%Yq%q')
    housing_df.rename(states,inplace=True)
    return housing_df
convert_housing_data_to_quarters()
#%%
def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    #star_rec=get_recession_start()
    gdp_df=get_gdp()
    string="".join(map(str,gdp_df["diff"].values))
    pattern="0011"
    ind_pattern=string.index(pattern)
    start_ress=string.rindex("1",0,ind_pattern)
    bfr_rec=gdp_df.index[start_ress-1]
    
    bottom_rec=get_recession_bottom()
    
    housing_df=convert_housing_data_to_quarters()
    #housing_df=housing_df.reset_index()
    
    university_towns=get_list_of_university_towns()
    university_towns=university_towns.set_index(["State","RegionName"])
    
    housing_df['PriceRatio'] = housing_df[bfr_rec].div(housing_df[bottom_rec])
    
    university_towns = housing_df.loc[university_towns.index].dropna(how="any")
    #not sure why, I will update you when I know, this following doesnt always work
    #non_uni_towns = hdf.loc[~uni_list_of_tuples]
    not_university_towns = housing_df[~housing_df.index.isin(university_towns.index)].dropna(how="any")
    
    statistc,pvalue=ttest_ind(university_towns["PriceRatio"],not_university_towns["PriceRatio"])
    if pvalue<0.01:
        different=True
    else:
        different=False
    u_mean=university_towns["PriceRatio"].mean()
    not_u_mean=not_university_towns["PriceRatio"].mean()
    if u_mean<not_u_mean:
        better="university town"
    else:
        better="non-university town"

    return (different,pvalue,better)
a=run_ttest()
#%%
# test output type (different, p, better)
def test_q6():
    q6 = run_ttest()
    different, p, better = q6

    res = 'Type test: '
    res += ['Failed\n','Passed\n'][type(q6) == tuple]

    res += 'Test "different" type: '
    res += ['Failed\n','Passed\n'][type(different) == bool or type(different) == np.bool_]

    res += 'Test "p" type: '
    res += ['Failed\n','Passed\n'][type(p) == np.float64]

    res +='Test "better" type: '
    res += ['Failed\n','Passed\n'][type(better) == str]
    if type(better) != str:
        res +='"better" should be a string with value "university town" or  "non-university town"'
        return res
    res += 'Test "different" spelling: '
    res += ['Failed\n','Passed\n'][better in ["university town", "non-university town"]]
    return res
print(test_q6())