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
CLIENT_TYPE = "logs"
LIMIT = 10000



def main():
    unique_ips = dict()
    dhcp_timestamps = open("dhcp_ts.txt", "r").read().splitlines()
    for ts in dhcp_timestamps:
        print(ts)
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
    out = dict(list(sorted_by_val.items())[0: 30])

    print(f"number of iterations = {len(dhcp_timestamps)} ")
    print(out)

 
if __name__ == "__main__":
    main()
