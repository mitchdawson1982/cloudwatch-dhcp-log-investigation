import boto3
import time
from datetime import datetime as dt
from datetime import timedelta

client = boto3.client('logs', region_name='eu-west-2')
# paginator = client.get_paginator('filter_log_events')

dhcpLogGroupName = 'staff-device-production-dhcp-server-log-group'
# log_stream_name = "eu-west-2-docker-logs/dhcp-server/2a48bd2c31a546b5ad2c42070f6f9212"

startTimeHuman = '2022-10-14T00:00:00.101+01:00'
endTimeHuman = '2022-10-14T11:45:00.101+01:00'

start_time = dt.strptime(startTimeHuman, '%Y-%m-%dT%H:%M:%S.%f+01:00')
end_time =dt.strptime(endTimeHuman, '%Y-%m-%dT%H:%M:%S.%f+01:00')
# end_time = start_time + timedelta(seconds=60)


start_timestamp = int(start_time.timestamp()) * 1000
end_timestamp = int(end_time.timestamp()) * 1000

print(start_time, end_time)
print(start_timestamp, end_timestamp)


dhcp_events = client.filter_log_events(
    logGroupName=dhcpLogGroupName,
    # logStreamNames=[log_stream_name],
    startTime=start_timestamp,
    endTime=end_timestamp,
    limit=1000,
    filterPattern='DUID'
)

# '\"DUID\"'
results = dhcp_events["events"]
timestamps = [result['timestamp']  for result in results]

file = open("logGroupTimestamps.txt", "w")
for ts in timestamps:
    file.write(str(ts) + "\n")
file.close()

