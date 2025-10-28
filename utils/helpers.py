# You can add helper functions here
def format_time(dt_string):
    from datetime import datetime
    try:
        dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M")
        return dt.strftime("%d %b %Y, %I:%M %p")
    except ValueError:
        return dt_string