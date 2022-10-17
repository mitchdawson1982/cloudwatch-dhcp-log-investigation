import boto3
import json
from datetime import datetime as dt

from event import Event

class LogExtractor:
    def __init__(self,
    region_name: str, log_group_name: str, start_time: int,
    end_time: int, filter_list: list[str], limit: int = 0, client_type: str = "logs", 
    search_string: str = "") -> None:
        self.region_name = region_name
        self.log_group_name = log_group_name
        self.start_time = start_time
        self.end_time = end_time
        self.filter_list = filter_list
        self.limit = limit
        self.search_string = search_string
        self.client_type = client_type
        self.client = self.create_client()
        self.paginator = self.client.get_paginator('filter_log_events')
        self.events: list[dict] = None
    
    def create_client(self):
        return boto3.client(
            self.client_type,
            self.region_name
        )
    
    def create_unix_millisecond_timestamp(self, timestamp: str) -> int:
        time_obj = dt.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f+01:00')
        return int(time_obj.timestamp()) * 1000
    
    def get_events(self):
        raw_events = self.get_raw_events()
        self.events = self.convert_raw_events(raw_events)

    def get_raw_events(self) -> list[dict]:
        raw_events = []
        logs = self.get_paginated_raw_logs()
        for log in logs:
            print(len(log["events"]))
            raw_events.extend(log["events"])
        return raw_events
    
    def convert_raw_events(self, raw_events: list[dict]) -> None:
        event_objects = []
        for raw_event in raw_events:
            event = Event(raw_event)
            event_objects.append(event)
        return event_objects

    def get_paginated_raw_logs(self):
        return self.paginator.paginate(
            logGroupName=self.log_group_name,
            startTime=self.start_time,
            endTime=self.end_time,
            filterPattern=self.search_string,
        )

    def write_raw_logs_to_json(self, filename: str = "vpc_logs.json") -> None:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.raw_log_data, f, ensure_ascii=False, indent=4)

    def filter_events(self) -> list[dict]:
        filtered_events = []
        for event in self.events:
            if "10.180.81.4" in event.source_ip or "10.180.80" in event.source_ip:
                continue
            if any(f in event.message for f in self.filter_list):
                filtered_events.append(event)
        self.events = filtered_events
    
    def remove_duplicate_events(self):
        print(f"number of existing events {len(self.events)}")
        events = set(self.events)
        print(f"number of unique events {len(events)}")
        self.events = events
    

    # def build_timestamp_src_ip_map(self):
    #     existing_events = self.raw_log_data["events"]
    #     data = {}
    #     for event in existing_events:
    #         message = event["message"]
    #         timestamp = dt.utcfromtimestamp(int(event["ingestionTime"]) / 1000).strftime('%Y-%m-%d %H:%M:%S')
    #         src_ip = message.split(" ")[3]
    #         print(timestamp, src_ip)
        # data[timestamp] = src_ip
        # print(data)

    def run(self) -> None:
        self.get_events()
        self.filter_events()
        self.remove_duplicate_events()
        source_ips = []
        for event in self.events:
            source_ips.append(event.source_ip)
        return source_ips
            # print(
            #     event.timestamp, event.source_ip, 
            #     event.destination_ip, event.port)




    # Convert to real timestamp
    # ingestionTime
