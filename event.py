from datetime import datetime


class Event:
    def __init__(self, event_dict: dict):
        self.event_dict = event_dict
    
    @property
    def log_stream_name(self) -> str:
        return self.event_dict.get("logStreamName")
    
    @property
    def event_id(self) -> str:
        return self.event_dict.get("eventId")
    
    @property
    def raw_timestamp(self) -> int:
        return int(self.event_dict.get("timestamp"))
    @property
    def timestamp(self) -> datetime:
        return datetime.utcfromtimestamp(int(self.raw_timestamp) / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')
    
    @property
    def message(self) -> str:
        return self.event_dict.get("message")
    
    @property
    def raw_ingestion_time(self) -> int:
        return int(self.event_dict.get("ingestionTime"))
    
    @property
    def ingestion_time(self) -> datetime:
        return datetime.utcfromtimestamp(int(self.raw_ingestion_time) / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')
    
    @property
    def event_id(self):
        return self.event_dict.get("eventId")

    @property
    def source_ip(self) -> str:
        return self.message.split(" ")[3]
    
    @property
    def destination_ip(self) -> str:
        return self.message.split(" ")[4]
    
    @property
    def port(self) -> int:
        return self.message.split(" ")[5]
    
    def __key(self):
        return (self.source_ip, self.destination_ip, self.port)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Event):
            return self.__key() == other.__key()
        return NotImplemented