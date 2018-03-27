 # Intervale Time stored here. 


def find_interval_all_device(app):
  interval = { 'time': 0 }
  end_time= app['report']['graph']['timeseries']['inbound'][0][-1][0]  #looks at the end time. 
  start_time= app['report']['graph']['timeseries']['inbound'][0][0][0] #looks at start time. 
    
  time_difference = ((end_time-start_time)/60) # 
    #if block to figure out what iterval we are in. 


  if time_difference <= 30:
    print('1 Minute Interval')
    interval['time'] = 60
  elif time_difference <= 120:
    print('5 Minute Interval')
    interval['time'] = 300
  elif time_difference <= 900:
    print ('30 minute Interval')
    interval['time'] = 1800
  elif time_difference <= 3600:
    print('2 Hour Interval')
    interval['time'] = 7200
  elif time_difference <= 21600:
    print('12 Hours Interval')
    interval['time'] = 43200
  else:
    print('1 Day Interval')
    interval['time'] = 86400

  return(interval)


def find_interval_single_device(app):
  interval = { 'time': 0 }
  end_time= app['report']['graph']['timeseries']['inbound'][0][-1][0]  #looks at the end time. 
  start_time= app['report']['graph']['timeseries']['inbound'][0][0][0] #looks at start time. 
    
  time_difference = ((end_time-start_time)/60) # 
    #if block to figure out what iterval we are in. 


  if time_difference <= 60:
    print('1 Minute Interval')
    interval['time'] = 60
  elif time_difference <= 300:
    print('5 Minute Interval')
    interval['time'] = 300
  elif time_difference <= 1800:
    print ('30 minute Interval')
    interval['time'] = 1800
  elif time_difference <= 7200:
    print('2 Hour Interval')
    interval['time'] = 7200
  elif time_difference <= 43200:
    print('12 Hours Interval')
    interval['time'] = 43200
  else:
    print('1 Day Interval')
    interval['time'] = 86400

  return(interval)