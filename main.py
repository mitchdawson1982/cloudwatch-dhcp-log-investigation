import boto3
import time
from datetime import datetime as dt
from datetime import timedelta

from log_extractor import LogExtractor

REGION_NAME = "eu-west-2"
VPC_LOG_GROUP_NAME = "staff-device-dns-dhcp-production-vpc-flow-logs-log-group"
DHCP_LOG_GROUP_NAME = "staff-device-production-dhcp-server-log-group"
VPC_FILTER_STRING = "ACCEPT OK" # -"10.180.80" "ACCEPT OK"
PRIMARY_FILTER_LIST = ["10.180.80.4", "10.180.81.4"]
DHCP_FILTER_STRING = ""
# START_TIME = "2022-10-14T01:00:00.000+01:00"
# END_TIME = "2022-10-14T01:00:10.000+01:00"
CLIENT_TYPE = "logs"
LIMIT = 10000

# client = boto3.client('logs', region_name='eu-west-2')
# paginator = client.get_paginator('filter_log_events')


# results = paginator.paginate(
#     logGroupName=VPC_LOG_GROUP_NAME,
#     startTime=int(dt.strptime(START_TIME,'%Y-%m-%dT%H:%M:%S.%f+01:00').timestamp() * 1000),
#     endTime=int(dt.strptime(END_TIME,'%Y-%m-%dT%H:%M:%S.%f+01:00').timestamp() * 1000),
#     filterPattern=VPC_FILTER_STRING,
# )

# counter = 0
# for result in results:

#     print(len(result["events"]))


# start_timestamp = int(start_time.timestamp()) * 1000
# end_timestamp = int(end_time.timestamp()) * 1000

# print(start_time, end_time)
# print(start_timestamp, end_timestamp)


# vpc_events = client.filter_log_events(
#     logGroupName=vpcLogGroupName,
#     startTime=start_timestamp,
#     endTime=end_timestamp,
#     filterPattern="ACCEPT OK"
# )

# results = vpc_events["events"]
# print(len(results))
# result = results[0]

# main timestamp value
# main_timestamp = dt.utcfromtimestamp(int(result["timestamp"]) / 1000).strftime('%Y-%m-%d %H:%M:%S')

# (result["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')
# print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
# ingestionTime
# ingestion_timestamp = dt.utcfromtimestamp(int(result["ingestionTime"]) / 1000).strftime('%Y-%m-%d %H:%M:%S')

# print(main_timestamp, ingestion_timestamp)

# file = open("vpc_log_group_events.txt", "w")

# for result in results:
#     message = result["message"]
#     if "ACCEPT OK" in message:
#         data = message.split(" ")
#         if not int(data[5]) == 67:
#             continue
#         dst = data[4]
#         if dst != "10.180.80.4":
#             continue
#         src = data[3]
#         ts = dt.utcfromtimestamp(int(result["ingestionTime"]) / 1000).strftime('%Y-%m-%d %H:%M:%S')
        
#         line = f"{src},{ts}"
#         file.write(line + "\n")

# file.close()


# vpc_logs = open("vpc_log_group_events.txt", "r").read().splitlines()
# vpc_log_data = {}

# for vpl in vpc_logs:
#     ip, ts = vpl.split(",")
#     vpc_log_data[ts] = ip

# print(vpc_log_data)



# timestamps = [result['timestamp']  for result in results]

# file = open("logGroupTimestamps.txt", "w")
# for ts in timestamps:
#     file.write(str(ts) + "\n")
# file.close()




def main():
    unique_ips = dict()
    dhcp_timestamps = open("dhcp_ts.txt", "r").read().splitlines()
    for ts in dhcp_timestamps:
        print(ts)
        # start_time = dt.strptime(str(ts),'%Y-%m-%dT%H:%M:%S.%f+01:00') - timedelta(seconds=1)
        start_time = dt.fromisoformat(ts) - timedelta(seconds=1)
        print(start_time)
        start_time = int(start_time.timestamp()  * 1000)
        end_time = dt.fromisoformat(ts) + timedelta(seconds=2)
        print(end_time)
        end_time = int(end_time.timestamp() * 1000)
        
        vpc = LogExtractor(
        region_name=REGION_NAME, log_group_name=VPC_LOG_GROUP_NAME,
        start_time=start_time, end_time=end_time, filter_list=PRIMARY_FILTER_LIST,
        limit=LIMIT, search_string=VPC_FILTER_STRING, client_type=CLIENT_TYPE
        )

        source_ips = vpc.run()
        print(f"Source Ips =  {len(source_ips)}")
        source_ips = list(set(source_ips))
        print(f"Unique Source Ips =  {len(source_ips)}")

        for ip in source_ips:
            if ip in unique_ips.keys():
                unique_ips[ip] += 1
            else:
                unique_ips[ip] = 1


    sorted_by_val = {k: b for k, b in sorted(unique_ips.items(), key=lambda element: element[1], reverse=True)}

    print(sorted_by_val)
    # print(unique_ips)
        # unique_ips.extend(source_ips)
        # unique_ips = set(unique_ips)
        # print(len(unique_ips))

        



        # int(dt.strptime(ts,'%Y-%m-%dT%H:%M:%S.%f+01:00').timestamp() * 1000),


    
    # vpc = LogExtractor(
    #     region_name=REGION_NAME, log_group_name=VPC_LOG_GROUP_NAME,
    #     start_time=START_TIME, end_time=END_TIME, filter_list=PRIMARY_FILTER_LIST,
    #     limit=LIMIT, search_string=VPC_FILTER_STRING, client_type=CLIENT_TYPE
    # )
    # vpc.run()
    # print(vpc.number_of_events)
    # vpc.filter_raw_logs(VPC_ADDITIONAL_FILTER_LIST)
    # vpc.write_raw_logs_to_json()
    # vpc.build_timestamp_src_ip_map()

if __name__ == "__main__":
    main()
