# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 16:58:43 2016

@author: Rob
To clean the data
"""
## panda panda panda
import pandas as pd
import datetime as dt
from pandasql import sqldf
import numpy as np


## read data
diio_data1 = pd.read_csv('G:/RevNetworkAnalysis/Economic & Industry Analysis/Projects/OA Capacity/Data/20170117_diio raw/Schedule_Dynamic_Table_Report_119188.tsv',skiprows=3,skipfooter=16,sep='\t')

diio_data2 = pd.read_csv('G:/RevNetworkAnalysis/Economic & Industry Analysis/Projects/OA Capacity/Data/20170117_diio raw/Schedule_Dynamic_Table_Report_119187.tsv',skiprows=3,skipfooter=16,sep='\t')

diio_data4 = pd.read_csv('G:/RevNetworkAnalysis/Economic & Industry Analysis/Projects/OA Capacity/Data/20170126_diio raw/5.tsv',skiprows=3,skipfooter=16,sep='\t')



#diio_data = pd.concat([diio_data1,diio_data2,diio_data3])
print("Begin...")
diio_data=diio_data4
diio_data=diio_data.reset_index(drop=True)

orig_coterm = pd.read_csv('G:/RevNetworkAnalysis/Economic & Industry Analysis/Projects/OA Capacity/Data/orig_coterms.csv')
dest_coterm = pd.read_csv('G:/RevNetworkAnalysis/Economic & Industry Analysis/Projects/OA Capacity/Data/orig_coterms.csv')



## add dates
print("Adding dates")
diio_data['eff_fm'] = dt.date.today()
diio_data['eff_to'] =dt.date(2099,12,31)


## write data

#diio_data.to_csv('G:/RevNetworkAnalysis/Economic & Industry Analysis/Projects/OA Capacity/Data/latest_data.csv')

## manipulaitons
print("Assigning airline codes")
diio_data["Airline"]=""

## set airline codes
diio_data['Airline']=np.where((diio_data['Airline Code']=="AA") | (diio_data['Airline Code']=="US"),"AA",
                    np.where((diio_data['Airline Code']=="UA") | (diio_data['Airline Code']=="CO"),"UA",
                    np.where((diio_data['Airline Code']=="NW") | (diio_data['Airline Code']=="DL"),"DL",
                    np.where((diio_data['Airline Code']=="WN") | (diio_data['Airline Code']=="FL"),"WN",
                    np.where((diio_data['Airline Code']=="AS") ,"AS",
                    np.where((diio_data['Airline Code']=="B6"), "B6",
                    np.where((diio_data['Airline Code']=="F9"),"F9",
                    np.where((diio_data['Airline Code']=="G4"),"G4",
                    np.where((diio_data['Airline Code']=="NK"),"NK",
                    np.where((diio_data['Airline Code']=="VX"),"VX",
                    "Other"))))))))))
print("Pivoting dataset")
#seats
seat_df= diio_data.pivot(columns='Airline',values ='Seats') #create airline columns
seat_df.fillna(0,inplace=True) #replace NaN with 0s
seat_df.columns=[str(col)+'_seats' for col in seat_df.columns]    
#asms
asm_df= diio_data.pivot(columns='Airline',values ='ASMs') #create airline columns
asm_df.fillna(0,inplace=True) #replace NaN with 0s
asm_df.columns=[str(col)+'_asms' for col in asm_df.columns]    
#trips
trip_df= diio_data.pivot(columns='Airline',values ='Flights') #create airline columns
trip_df.fillna(0,inplace=True) #replace NaN with 0s
trip_df.columns=[str(col)+'_trips' for col in trip_df.columns]    



## add proper dates
print("Adding correct date formats")
diio_data['Date'] =pd.to_datetime(pd.Series(diio_data['Travel Month'])).dt.date

## merge tables
print("Creating huge table")
mega_table = pd.concat([diio_data,seat_df,asm_df,trip_df],axis=1,join_axes=[diio_data.index])

#mega_table =  mega_table.loc[1:50000]
## Same store and comp overlap 
print("Querying beginsssss......................")
overlap_table = sqldf("""
                       
                       select 
                       t1.flt_qtr as flt_qtr,
                       t1.flt_year as flt_year,
                       t1.origin_code as origin_code,
                       t1.dest_code as dest_code,
                       
                       orig.Orig_Coterm as orig_coterm,
                       orig.Orig_Region as orig_region,
                       orig.`Orig_Airport name` as orig_arpt_name,
                       orig.`Orig_Coterm name` as orig_coterm_name,
                       
                       dest.Orig_Coterm as dest_coterm,
                       dest.Orig_Region as dest_region,
                       dest.`Orig_Airport name` as dest_arpt_name,
                       dest.`Orig_Coterm name` as dest_coterm_name,
                       
                       
                       sum(cy.AA_seats) as AA_seats_cy,
                       sum(py.AA_seats) as AA_seats_py,
                       
                       sum(cy.AS_seats) as AS_seats_cy,
                       sum(py.AS_seats) as AS_seats_py,
                       
                       sum(cy.B6_seats) as B6_seats_cy,
                       sum(py.B6_seats) as B6_seats_py,
                       
                       sum(cy.DL_seats) as DL_seats_cy,
                       sum(py.DL_seats) as DL_seats_py,
                       
                       sum(cy.F9_seats) as F9_seats_cy,
                       sum(py.F9_seats) as F9_seats_py,
                       
                       sum(cy.G4_seats) as G4_seats_cy,
                       sum(py.G4_seats) as G4_seats_py,
                       
                                           
                       sum(cy.NK_seats) as NK_seats_cy,
                       sum(py.NK_seats) as NK_seats_py,
                       
                       
                       sum(cy.WN_seats) as WN_seats_cy,
                       sum(py.WN_seats) as WN_seats_py,
                       
                       sum(cy.Other_seats) as Other_seats_cy,
                       sum(py.Other_seats) as Other_seats_py,
                       
                       sum(cy.UA_seats) as UA_seats_cy,
                       sum(py.UA_seats) as UA_seats_py,
                       
                       sum(cy.VX_seats) as VX_seats_cy,
                       sum(py.VX_seats) as VX_seats_py,
                       
                       ---------------------
                        sum(cy.AA_asms) as AA_asms_cy,
                       sum(py.AA_asms) as AA_asms_py,
                       
                       sum(cy.AS_asms) as AS_asms_cy,
                       sum(py.AS_asms) as AS_asms_py,
                       
                       sum(cy.B6_asms) as B6_asms_cy,
                       sum(py.B6_asms) as B6_asms_py,
                       
                       sum(cy.DL_asms) as DL_asms_cy,
                       sum(py.DL_asms) as DL_asms_py,
                       
                       sum(cy.F9_asms) as F9_asms_cy,
                       sum(py.F9_asms) as F9_asms_py,
                       
                       sum(cy.G4_asms) as G4_asms_cy,
                       sum(py.G4_asms) as G4_asms_py,
                       
                                           
                       sum(cy.NK_asms) as NK_asms_cy,
                       sum(py.NK_asms) as NK_asms_py,
                       
                       
                       sum(cy.WN_asms) as WN_asms_cy,
                       sum(py.WN_asms) as WN_asms_py,
                       
                       sum(cy.Other_asms) as Other_asms_cy,
                       sum(py.Other_asms) as Other_asms_py,
                       
                       sum(cy.UA_asms) as UA_asms_cy,
                       sum(py.UA_asms) as UA_asms_py,
                       
                       sum(cy.VX_asms) as VX_asms_cy,
                       sum(py.VX_asms) as VX_asms_py,
                       
                       --------------------------
                       
                        sum(cy.AA_trips) as AA_trips_cy,
                       sum(py.AA_trips) as AA_trips_py,
                       
                       sum(cy.AS_trips) as AS_trips_cy,
                       sum(py.AS_trips) as AS_trips_py,
                       
                       sum(cy.B6_trips) as B6_trips_cy,
                       sum(py.B6_trips) as B6_trips_py,
                       
                       sum(cy.DL_trips) as DL_trips_cy,
                       sum(py.DL_trips) as DL_trips_py,
                       
                       sum(cy.F9_trips) as F9_trips_cy,
                       sum(py.F9_trips) as F9_trips_py,
                       
                       sum(cy.G4_trips) as G4_trips_cy,
                       sum(py.G4_trips) as G4_trips_py,
                       
                                           
                       sum(cy.NK_trips) as NK_trips_cy,
                       sum(py.NK_trips) as NK_trips_py,
                       
                       
                       sum(cy.WN_trips) as WN_trips_cy,
                       sum(py.WN_trips) as WN_trips_py,
                       
                       sum(cy.Other_trips) as Other_trips_cy,
                       sum(py.Other_trips) as Other_trips_py,
                       
                       sum(cy.UA_trips) as UA_trips_cy,
                       sum(py.UA_trips) as UA_trips_py,
                       
                       sum(cy.VX_trips) as VX_trips_cy,
                       sum(py.VX_trips) as VX_trips_py
                       
                       -------------------------
                       from
                       
                       (
                                     
                                
                    select * from
                    (
                             select 
                   
                   case when cast(strftime('%m',Date) as integer) in (1,2,3) then '1Q'
                        when cast(strftime('%m',Date) as integer) in (4,5,6) then '2Q'
                        when cast(strftime('%m',Date) as integer) in (7,8,9) then '3Q'
                        when cast(strftime('%m',Date) as integer) in (10,11,12) then '4Q'
                        else null end as flt_qtr,
                   cast(strftime('%Y',Date) as integer) as flt_year,     
                   mega.`Origin Code` as origin_code ,
                   mega.`Destination Code` as dest_code
                  
                   
                   from 
                       mega_table mega
                       
                     
                   
                   group by 1,2,3,4 
                              
                              
                
                union all 
                
                                
                             
                             select 
                   
                   case when cast(strftime('%m',Date) as integer) in (1,2,3) then '1Q'
                        when cast(strftime('%m',Date) as integer) in (4,5,6) then '2Q'
                        when cast(strftime('%m',Date) as integer) in (7,8,9) then '3Q'
                        when cast(strftime('%m',Date) as integer) in (10,11,12) then '4Q'
                        else null end as flt_qtr,
                   cast(strftime('%Y',Date) as integer)+1 as flt_year,     
                   mega.`Origin Code` as origin_code ,
                   mega.`Destination Code` as dest_code
                  
                   
                   from 
                       mega_table mega
                       
                     
                   
                   group by 1,2,3,4 
                              
             )
            group by 1,2,3,4
                       ) T1
                       
                   left join    
                       
                       (
                             
                             select 
                   
                   case when cast(strftime('%m',Date) as integer) in (1,2,3) then '1Q'
                        when cast(strftime('%m',Date) as integer) in (4,5,6) then '2Q'
                        when cast(strftime('%m',Date) as integer) in (7,8,9) then '3Q'
                        when cast(strftime('%m',Date) as integer) in (10,11,12) then '4Q'
                        else null end as flt_qtr,
                   strftime('%Y',Date) as flt_year,     
                   mega.`Origin Code` as origin_code ,
                   mega.`Destination Code` as dest_code,
                   
                  sum(mega.Seats) as total_seats,
                   sum(mega.AA_seats) as AA_seats,
                   sum(mega.`AS_seats`) as AS_seats,
                   sum(mega.B6_seats) as B6_seats,
                   sum(mega.DL_seats) as DL_seats,
                   sum(mega.F9_seats) as F9_seats,
                   sum(mega.G4_seats) as G4_seats,
                   sum(mega.NK_seats) as NK_seats,
                   sum(mega.Other_seats) as Other_seats,
                   sum(mega.UA_seats) as UA_seats,
                   sum(mega.VX_seats) as VX_seats,
                   sum(mega.WN_seats) as WN_seats,
                   
                   sum(mega.ASMs) as total_asms,
                   sum(mega.AA_asms) as AA_asms,
                   sum(mega.`AS_asms`) as AS_asms,
                   sum(mega.B6_asms) as B6_asms,
                   sum(mega.DL_asms) as DL_asms,
                   sum(mega.F9_asms) as F9_asms,
                   sum(mega.G4_asms) as G4_asms,
                   sum(mega.NK_asms) as NK_asms,
                   sum(mega.Other_asms) as Other_asms,
                   sum(mega.UA_asms) as UA_asms,
                   sum(mega.VX_asms) as VX_asms,
                   sum(mega.WN_asms) as WN_asms,
                   
                   sum(mega.Flights) as total_trips,
                   sum(mega.AA_trips) as AA_trips,
                   sum(mega.`AS_trips`) as AS_trips,
                   sum(mega.B6_trips) as B6_trips,
                   sum(mega.DL_trips) as DL_trips,
                   sum(mega.F9_trips) as F9_trips,
                   sum(mega.G4_trips) as G4_trips,
                   sum(mega.NK_trips) as NK_trips,
                   sum(mega.Other_trips) as Other_trips,
                   sum(mega.UA_trips) as UA_trips,
                   sum(mega.VX_trips) as VX_trips,
                   sum(mega.WN_trips) as WN_trips
                   
                   from 
                       mega_table mega
                       
                       left join
                           orig_coterm orig
                        on orig.Orig_Airport = mega.`Origin Code`
                        
                        left join
                            dest_coterm dest
                        on dest.Orig_Airport = mega.`Destination Code`
                   
                   
                   group by 1,2,3,4 
                              
                              )cy
                       
                            on t1.flt_qtr = cy.flt_qtr
                            and cast(t1.flt_year as integer)= cast(cy.flt_year as integer)
                            and t1.origin_code = cy.origin_code
                            and t1.dest_code = cy.dest_code
                
                left join
                (
                                
                                select 
                   
                   case when cast(strftime('%m',Date) as integer) in (1,2,3) then '1Q'
                        when cast(strftime('%m',Date) as integer) in (4,5,6) then '2Q'
                        when cast(strftime('%m',Date) as integer) in (7,8,9) then '3Q'
                        when cast(strftime('%m',Date) as integer) in (10,11,12) then '4Q'
                        else null end as flt_qtr,
                   strftime('%Y',Date) as flt_year,     
                   mega.`Origin Code` as origin_code ,
                   mega.`Destination Code` as dest_code,
                   
                   sum(mega.Seats) as total_seats,
                   sum(mega.AA_seats) as AA_seats,
                   sum(mega.`AS_seats`) as AS_seats,
                   sum(mega.B6_seats) as B6_seats,
                   sum(mega.DL_seats) as DL_seats,
                   sum(mega.F9_seats) as F9_seats,
                   sum(mega.G4_seats) as G4_seats,
                   sum(mega.NK_seats) as NK_seats,
                   sum(mega.Other_seats) as Other_seats,
                   sum(mega.UA_seats) as UA_seats,
                   sum(mega.VX_seats) as VX_seats,
                   sum(mega.WN_seats) as WN_seats,
                   
                   sum(mega.ASMs) as total_asms,
                   sum(mega.AA_asms) as AA_asms,
                   sum(mega.`AS_asms`) as AS_asms,
                   sum(mega.B6_asms) as B6_asms,
                   sum(mega.DL_asms) as DL_asms,
                   sum(mega.F9_asms) as F9_asms,
                   sum(mega.G4_asms) as G4_asms,
                   sum(mega.NK_asms) as NK_asms,
                   sum(mega.Other_asms) as Other_asms,
                   sum(mega.UA_asms) as UA_asms,
                   sum(mega.VX_asms) as VX_asms,
                   sum(mega.WN_asms) as WN_asms,
                   
                    sum(mega.Flights) as total_trips,
                   sum(mega.AA_trips) as AA_trips,
                   sum(mega.`AS_trips`) as AS_trips,
                   sum(mega.B6_trips) as B6_trips,
                   sum(mega.DL_trips) as DL_trips,
                   sum(mega.F9_trips) as F9_trips,
                   sum(mega.G4_trips) as G4_trips,
                   sum(mega.NK_trips) as NK_trips,
                   sum(mega.Other_trips) as Other_trips,
                   sum(mega.UA_trips) as UA_trips,
                   sum(mega.VX_trips) as VX_trips,
                   sum(mega.WN_trips) as WN_trips
                   
                   from 
                       mega_table mega
                       
                       left join
                           orig_coterm orig
                        on orig.Orig_Airport = mega.`Origin Code`
                        
                        left join
                            dest_coterm dest
                        on dest.Orig_Airport = mega.`Destination Code`
                   
                   
                   group by 1,2,3,4 
                
                )py
                
            on t1.flt_qtr = py.flt_qtr
                            and cast(t1.flt_year as integer)-1 = cast(py.flt_year as integer)
                            and t1.origin_code = py.origin_code
                            and t1.dest_code = py.dest_code
            
          
            
            left join
            orig_coterm orig
            on orig.Orig_Airport = t1.origin_code
            
            Left join
            dest_coterm dest
            on dest.Orig_Airport =t1.dest_code
           
           group by 1,2,3,4
           
           """)
print("Replacing nulls with 0") 
overlap_table.fillna(0,inplace=True)
print("DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!")

#overlap_table.to_csv('G:/RevNetworkAnalysis/Economic & Industry Analysis/Projects/OA Capacity/Data/overlap_data_2.csv')

#overlap_table.to_csv('G:/RevNetworkAnalysis/Economic & Industry Analysis/Projects/OA Capacity/Data/overlap_data_20170126.csv',header=True,index=False)
overlap_table.to_csv('G:/RevNetworkAnalysis/Economic & Industry Analysis/Projects/OA Capacity/Data/overlap_data_20170126.csv',header=False,index=False,mode='a')

overlap_table.tail()
#==============================================================================
# 
#==============================================================================
#==============================================================================
# sqldf("""
#       select * 
#       from overlap_table 
#       where origin_code  in ('IAH','DAL')
#       and dest_code in ('DAL','IAH')
#       and flt_qtr = '4Q'
#       and flt_year = 2015
# 
# """)
# 
# 
# 
# test = sqldf("""
#                      
#                     select * from
#                     (
#                              select 
#                    
#                    case when cast(strftime('%m',Date) as integer) in (1,2,3) then '1Q'
#                         when cast(strftime('%m',Date) as integer) in (4,5,6) then '2Q'
#                         when cast(strftime('%m',Date) as integer) in (7,8,9) then '3Q'
#                         when cast(strftime('%m',Date) as integer) in (10,11,12) then '4Q'
#                         else null end as flt_qtr,
#                    cast(strftime('%Y',Date) as integer) as flt_year,     
#                    mega.`Origin Code` as origin_code ,
#                    mega.`Destination Code` as dest_code
#                   
#                    
#                    from 
#                        mega_table mega
#                        
#                      
#                    
#                    group by 1,2,3,4 
#                               
#                               
#                 
#                 union all 
#                 
#                                 
#                              
#                              select 
#                    
#                    case when cast(strftime('%m',Date) as integer) in (1,2,3) then '1Q'
#                         when cast(strftime('%m',Date) as integer) in (4,5,6) then '2Q'
#                         when cast(strftime('%m',Date) as integer) in (7,8,9) then '3Q'
#                         when cast(strftime('%m',Date) as integer) in (10,11,12) then '4Q'
#                         else null end as flt_qtr,
#                    cast(strftime('%Y',Date) as integer)+1 as flt_year,     
#                    mega.`Origin Code` as origin_code ,
#                    mega.`Destination Code` as dest_code
#                   
#                    
#                    from 
#                        mega_table mega
#                        
#                      
#                    
#                    group by 1,2,3,4 
#                               
#              )
#             group by 1,2,3,4
#            
#            """)
#==============================================================================
