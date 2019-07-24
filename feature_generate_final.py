import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
import os
from datetime import date
from datetime import datetime, timedelta
import time
import sys
import numpy as np
import asset_report
engine= create_engine("mysql://root1:Ekryp#1234@35.199.174.191/ml_reference")
conn=mysql.connector.connect( host='35.199.174.191', database='ml_reference',user='root1',password='Ekryp#1234')

def build_feature(product_id,prod_dfs,asset_info,notes_processed,notes,device_sw_date_ver,customer_model_attributes,service_request_history,asset_error_codes,priority,code_id_type,prod_install_date,start_date,end_date,sr_dates):
    try:
        

        
        #device_sw_date_ver = device_sw_date_ver[~device_sw_date_ver.index.duplicated(keep='last')]
        #print(device_sw_date_ver.shape)
        ##device sw install date latest record is for 2020???, 
        device_sw_date_ver = device_sw_date_ver[device_sw_date_ver.customer_asset_identifier == product_id][['device_software_name', 'software_installed_date']]
        device_sw_date_ver.software_installed_date = pd.to_datetime(device_sw_date_ver.software_installed_date)
        device_sw_date_ver.sort_values(['software_installed_date'], inplace = True)
        device_sw_date_ver['software_installed_date'] = pd.to_datetime(device_sw_date_ver.software_installed_date).dt.date
        device_sw_date_ver.set_index('software_installed_date', drop=True, inplace=True)
        # Removing duplicates and keeping the last firmware that was installed for that date
        device_sw_date_ver = device_sw_date_ver[~device_sw_date_ver.index.duplicated(keep='last')]

        

        #device_sw_date_ver =  pd.read_sql("select software_installed_date, device_software_name from device_software_details order by software_installed_date desc limit 1",con = engine)
        #print(device_sw_date_ver.shape)
        
        

        #asset_error = asset_error_codes[asset_error_codes['customer_asset_identifier'] == product_id].copy()
        #asset_error.date = pd.to_datetime(asset_error['date']).dt.date
        
        
        
        
        notes_in_prod=pd.DataFrame()
        notes_in_prod['notes_in']=notes['work_units']
        notes_in_prod['date']=notes['date']
        
        notes_in_prod = notes_in_prod[~notes_in_prod.index.duplicated(keep='last')]
        
        
        
    
        #print(type(notes['date'].min()))
        # define start date based on the install date
        
       # print(notes['date'].min())
        #print(prod_install_date)
        print("Product ID:",product_id)
        

        days_since_install = (start_date - prod_install_date).days
        idx=pd.date_range(start_date, end_date)
        
        notes_in_prod.set_index('date',drop=True,inplace=True)
        #notes_in_prod=pd.Series(notes_in_prod)
        #notes_in_prod.index = pd.DatetimeIndex(notes_in_prod.index)
        notes_in_prod = notes_in_prod.reindex(idx,fill_value=0)
        #print('notes',notes_in_prod)
        cumilative_sum_notes = notes_in_prod.copy()
        #print('n',cumilative_sum_notes)

        #print(customer_model_attributes['prediction_horizon'].min())
        #print(N)
        notes_in_prod_lastN = 	notes_in_prod.rolling(min_periods=0,window = customer_model_attributes['prediction_horizon'].min(),center=False).sum()

        # UPDATE notes_in

        notes_in_prod = notes_in_prod.cumsum() 
        #print('notes_in',notes_in_prod)
        pm_dates = service_request_history.service_request_date[(service_request_history.customer_asset_identifier == product_id) &
                                    (service_request_history.incident_category == 'Preventative Maintenance') &
                                    #(sr.service_request_date >= start_date) &
                                    (service_request_history.service_request_date >= prod_install_date) &
                                    (service_request_history.service_request_date <= end_date)]
        
        vals = np.zeros((notes_in_prod.shape[0], 3))

        #print( customer_model_attributes['periods_for_error'].min() )
        
        failureVals = np.full((notes_in_prod.shape[0], 1), customer_model_attributes['periods_for_error'].min())

        iniBias = (start_date - (prod_install_date if not len(pm_dates) or pm_dates.min() > start_date else pm_dates[pm_dates <= start_date].max())).days

        pm_dates = pm_dates[pm_dates >= start_date]

        seq_start_idx = 0
        seq_start_date = start_date
        for pm_date in pm_dates.sort_values():
            seq_end_idx = (pm_date - start_date).days
            vals[seq_start_idx:seq_end_idx, 0] = range(iniBias, seq_end_idx - seq_start_idx + iniBias)
            
            cumilative_sum_notes.ix[seq_start_date:(pm_date - timedelta(days=1))] = cumilative_sum_notes.ix[seq_start_date:(pm_date - timedelta(days=1))].cumsum()
            seq_start_idx = seq_end_idx
            seq_start_date = pm_date
            iniBias = 0
        cumilative_sum_notes.ix[seq_start_date:end_date] = cumilative_sum_notes.ix[seq_start_date:end_date].cumsum()
        vals[seq_start_idx: len(vals), 0] = range(iniBias, len(vals) - seq_start_idx + iniBias)
        
        
        
        daysSinceFailure = np.zeros((notes_in_prod.shape[0], 1))
        numServiceRequest = sr_dates[sr_dates < start_date].count()
        #print(sr_dates.head())
        iniBias = (start_date - (prod_install_date if sr_dates['service_request_date'].min() > start_date else sr_dates['service_request_date'].max())).days
        sr_dates = sr_dates[sr_dates >= start_date]
        seq_start_idx = 0
        sr_dates = sr_dates['service_request_date'].sort_values()
        
        for sr_date in sr_dates.iteritems():
            #print(sr_date)
            #sr_date = datetime(*sr_date[0:3])
            #print(sr_date[1])
            start_idx = max(0, (sr_date[1] - start_date).days - 30)
            end_idx = (sr_date[1] - start_date).days
            vals[range(start_idx, end_idx + 1), 1] = 1
            vals[seq_start_idx:end_idx, 2] = [numServiceRequest] * (end_idx - seq_start_idx)
        
            daysSinceFailure[seq_start_idx:end_idx, 0] = range(iniBias, end_idx - seq_start_idx + iniBias)
            
            start_idx_df = max(0, (sr_date[1] - start_date).days - 180)
            for i in xrange(start_idx_df, end_idx + 1):
                failureVals[i] = min(failureVals[i], end_idx - i)
            numServiceRequest += 1
            seq_start_idx = end_idx
            iniBias = 0
        
        vals[seq_start_idx:, 2] = [numServiceRequest] * (len(vals) - seq_start_idx)
        #print("vals",vals)
        
        daysSinceFailure[seq_start_idx: len(vals), 0] = range(iniBias, len(vals) - seq_start_idx + iniBias)
        #print(daysSinceFailure)
        #print(type(daysSinceFailure))
        #print(daysSinceFailure.ravel())
        #print(daysSinceFailure[:, 0])
        
        l = vals[:, 0]
        f = vals[:, 1]
        n = vals[:, 2]
        #device_sw_date_ver.set_index('software_installed_date',inplace=True)
        device_sw_date_ver = device_sw_date_ver.reindex(idx, method = 'ffill').bfill()
        daf= failureVals[:,0]
        dsf= daysSinceFailure[:,0]
        lpd = l.tolist()
        last_pm_date=pd.DataFrame(lpd,columns=['last_pm_date'])
        last_pm_date.set_index(idx,inplace=True)
        fe=f.tolist()
        failure_event = pd.DataFrame(fe,columns=['failure_event'])
        failure_event.set_index(idx,inplace=True)
        nI=n.tolist()
        numIncidents = pd.DataFrame(nI,columns=['numIncidents'])
        numIncidents.set_index(idx,inplace=True)
        da=daf.tolist()
        day_to_failure=pd.DataFrame(da,columns=['day_to_failure'])
        day_to_failure.set_index(idx,inplace=True)
        ds=dsf.tolist()
        days_Since_failure=pd.DataFrame(ds,columns=['days_Since_failure'])
        days_Since_failure.set_index(idx,inplace=True)

        ag=range(0 + days_since_install, len(vals) + days_since_install)
        age=pd.DataFrame(ag,columns=['age'])
        age.set_index(idx,inplace=True)
        
    
        #print(range(0 + days_since_install, len(vals) + days_since_install))

        #print('notes in prod', notes_in_prod.head())
        #my_diction = {}
        #print(prod_df)
        #prod_df = pd.DataFrame(np.column_stack([product_id, notes_in_prod,notes_in_prod_lastN,cumilative_sum_notes,numIncidents,last_pm_date,age,failure_event,day_to_failure,days_Since_failure ]),
                                #columns=['customer_asset_identifier','notes_in','notes_in_last_N','notes_in_last_pm','numIncidents','last_pm_date','age','failure_event','day_to_failure','days_Since_failure']              
                        
                    #)
    # print(prod_df.head())
        #print(my_diction)

        #prod_df = pd.DataFrame.from_dict(my_diction)
        #print(prod_df.shape)
        
    
        listOfCombinations = {
        'codeType': code_id_type['code_type'],
        'priority': priority['priority'],
        'highPriorityCodes': code_id_type['code_id']
        }
    # a=customer_model_attributes.iloc[0]['prediction_horizon']
        #print(a)
        
        prod_df = pd.DataFrame( {  'customer_asset_identifier': product_id,
                                'notes_in': notes_in_prod['notes_in'],
                                'notes_in_last_N': notes_in_prod_lastN['notes_in'],
                                'notes_in_last_pm': cumilative_sum_notes['notes_in'],
                                'numIncidents':numIncidents['numIncidents'],
                                'last_pm_date': last_pm_date['last_pm_date'],
                                    'age': age['age'],
                                    'device_software_details': device_sw_date_ver['device_software_name'],#firmwareversionid
                                    'failure_event': failure_event['failure_event'],
                                    'day_to_failure': day_to_failure['day_to_failure'],
                                    'days_Since_failure': days_Since_failure['days_Since_failure'],
                                    'model_name': asset_info['model_name'],
                                    'model_group_id': asset_info['model_group_id'],
                                    'category_id': asset_info['category_id'],
                                    'type_id':asset_info['type_id'],
                                    'capacity': asset_info['capacity']
                                },index=idx)
        #print(prod_df.head())
        prod_df['Avg_notes_in'] = prod_df['notes_in'].astype(float) / prod_df['age']
        prod_df['Avg_notes_in_lastN'] = prod_df['notes_in_last_N'].astype(float) / customer_model_attributes['prediction_horizon'].min()
        #print(prod_df.head())
        #print(pd.__version__)
        for codeType in listOfCombinations['codeType']:
            for p in listOfCombinations['priority']:
        #       print(codeType)
        #       print(p)
                errorCodesCategory = asset_error_codes[(asset_error_codes.code_type == codeType) & (asset_error_codes.priority == p)].groupby('date').count()
        #        print(errorCodesCategory.shape)
                #errorCodesCategory.set_index(idx,inplace=True)
                errorCodeCategory = errorCodesCategory.reindex(idx, fill_value=0)
                errorCodeCount=pd.DataFrame()
                errorCodeCount=errorCodeCategory.copy()
                #print(errorCodeCount)
                errorCodeStd = errorCodeCount['code_type'].rolling(window=30,center=False).std()
                errorCodeCount = errorCodeCount['code_type'].cumsum()
                #print(type(errorCodeCount))
                #calculating seperately
                last30DayErrorCount = errorCodeCount.subtract(errorCodeCount.shift(30), fill_value = 0)
                prod_df['CodeType_'+str(int(codeType)) + '_priority_'+str(int(p))] = last30DayErrorCount
                #criticality = priority column name
                prod_df['CodeType_'+str(int(codeType)) + '_priority_'+str(int(p)) + '_std'] = errorCodeStd
        for errorCode in listOfCombinations['highPriorityCodes']:
                errorCodesCategory = asset_error_codes[(asset_error_codes.code_id == errorCode)].groupby('date').count()
                errorCodeCategory = errorCodesCategory.reindex(idx, fill_value=0)
                errorCodeCount=pd.DataFrame()
                errorCodeCount=errorCodeCategory.copy()
                errorCodeStd = errorCodeCount['code_type'].rolling(window=30,center=False).std()
                errorCodeCount = errorCodeCount['code_type'].cumsum()  
                last30DayErrorCount = errorCodeCount.subtract(errorCodeCount.shift(30), fill_value = 0)
                prod_df['Code_'+str(int(errorCode))] = last30DayErrorCount
                prod_df['Code_'+str(int(errorCode)) + '_std'] = errorCodeStd
                #print(last30DayErrorCount)
        print(prod_df.shape)

        
        
        #deviceFeature  = pd.DataFrame( {  'model_name': asset_info['model_name'],
        #                                  'model_group_id': asset_info['model_group_id'],
        #                                  'category_id': asset_info['category_id'],
        #                                  'type_id':asset_info['type_id'],
        #                                  'capacity': asset_info['capacity']
        #                                },index=idx)
        #for column in deviceFeature.columns:
        #    prod_df[column] = deviceFeature[column].values[0]
        # Adding this DF to the global list
        #appending prod_df
        prod_dfs.append(prod_df[:])
    # return(prod_df)
    #'numIncidents': vals[:, 2]
    except Exception as e:
        print 'There was an error while processing for product id', product_id, e.message
#productStatus = pd.read_csv(os.path.join('valid_assets.csv'), header=None)
productStatus= asset_report.get_valid_assets()
productStatus.columns = ['id']
print(productStatus.head())

prod_dfs = []        
for i, product_id in enumerate(productStatus['id']):
        #print_progress(i, len(productStatus['id']))
        try:
            x = product_id
            query = "SELECT * FROM asset_information WHERE customer_asset_identifier = '%s'" % x
            asset_info = pd.read_sql(query,con = engine)
            #print(asset_info.shape)
            
            x = product_id
            query = "select * from periodic_work_processed WHERE customer_asset_identifier = '%s'" % x
            notes_processed = pd.read_sql(query,con = engine)
            notes = notes_processed[notes_processed['customer_asset_identifier']==product_id].copy()

            device_sw_date_ver =  pd.read_sql("select * from device_software_details",con = engine)
            #print(notes_processed.shape)

            customer_model_attributes = pd.read_sql("select periods_for_error,prediction_horizon,prediction_frequency from Customer_Model_Configuration order by created_at desc limit 1",con = engine)
            #print(customer_model_attributes.shape)

            x = product_id
            query = "select * from service_request_history where customer_asset_identifier= '%s'" % x
            service_request_history = pd.read_sql(query,con = engine)
            #print(service_request_history.shape)

            x = product_id
            query = "select a.code_id,a.date,e.priority,e.code_type from ml_reference.asset_error_codes as a inner join ml_reference.error_code_feature_def as e on a.code_id = e.code_id where a.customer_asset_identifier = '%s'" % x
            asset_error_codes= pd.read_sql(query,con = engine)
            #print(asset_error_codes.head())
            #previously criticality. considering only 1, 2 and 3 levels.
            priority =  pd.read_sql("select priority from error_code_feature_def where priority!=0 group by priority",con = engine)
            #print(priority.head())

            #obtaining  code id(top 11 severity) and code type(1) for priorities(1,2,3)
            code_id_type = pd.read_sql("select a.code_id,e.code_type from asset_error_codes as a,error_code_feature_def as e where e.code_id = a.code_id and e.priority=3 group by a.code_id order by count(a.code_id) desc limit 11", con= engine)
            #print(code_id_type.head())

            prod_install_date = asset_info.install_date[asset_info.customer_asset_identifier == product_id].values[0]
            start_date = max(notes['date'].min(),prod_install_date)

            max_Date = datetime.now().date()
            end_date = max_Date

            x = product_id
            y = start_date
            z = end_date
            query = "select s.service_request_date from service_request_history as s, incident_selection as i where i.incident_category=s.incident_category and i.to_be_selected = 0 and s.customer_asset_identifier = '%s' and s.service_request_date > '%s' and s.service_request_date < '%s'" % (x, y, z) 
            sr_dates  = pd.read_sql(query,con = engine)

            build_feature(product_id,prod_dfs,asset_info,notes_processed,notes,device_sw_date_ver,customer_model_attributes,service_request_history,asset_error_codes,priority,code_id_type,prod_install_date,start_date,end_date,sr_dates)

            
        except:
            print 'Skipping fact creation product_id', product_id
            raise
        time.sleep(0.001)
complete_data = pd.concat(prod_dfs)
complete_data.index.name = 'date'
complete_data.set_index(['customer_asset_identifier'], append=True, drop=True, inplace=True)
complete_data.sort_index(inplace=True)
    #we need these 2 as our indexes
complete_data.to_csv('newFacts-Data_1.csv', index=True, index_label=['date', 'customer_asset_identifier'])
print('Features Generated!')

