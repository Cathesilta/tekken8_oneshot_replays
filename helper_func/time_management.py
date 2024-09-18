from datetime import timedelta



def convert_seconds_to_hms(seconds):
    return str(timedelta(seconds=seconds))