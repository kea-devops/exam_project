from dateutil import parser
from datetime import datetime, timedelta

def parse_date(input_date):
    # Unix Epoch
    try:
        epoch = int(input_date)
        return datetime.utcfromtimestamp(epoch)
    except:
        pass
    
    # ISO 8601
    try:
        return parser.parse(input_date)
    except ValueError:
        pass

    raise ValueError("Invalid date format")

def time_from_now(seconds):
    time = datetime.now() + timedelta(seconds=seconds)
    # as ISO 8601
    return time.isoformat() + 'Z'