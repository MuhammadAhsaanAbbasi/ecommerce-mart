from datetime import datetime, timedelta

def format_time(time: int) -> str:
    return f"{time:02d}"

# Get the current date and time in UTC
now = datetime.utcnow()

# Get the hours and minutes in UTC
hours_utc = now.hour
minutes_utc = now.minute

# Convert UTC hours to the desired time zone (GMT+5:30)
time_zone_offset = 5 * 60 + 30  # Offset in minutes
hours = hours_utc + time_zone_offset // 60
minutes = minutes_utc

# Adjust minutes for overflow
if minutes >= 60:
    hours += 1
    minutes -= 60

# Adjust hours for negative values or overflow
if hours < 0:
    hours += 24
if hours >= 24:
    hours -= 24

# Format hours and minutes with leading zeros
formatted_hours = format_time(hours)
formatted_minutes = format_time(minutes)

    # Construct the time string
today_date = f"{formatted_hours}:{formatted_minutes}"