from datetime import datetime
import json

# Load JSON data from the file
with open('D:\programing\Athan claender\prayer_time.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Get today's date in the format used in the JSON file
today_date = datetime.today().strftime('%A %d-%m-%Y')
# print(today_date)
# Find timings for today
today_timings = None
for entry in data:
    if entry['gregorian'] == today_date:
        today_timings = entry['timings']
        break
# print(today_timings)
# Print or use today's timings
if today_timings:
    print(f"Timings for today ({today_date}):")
    print(f"Fajr: {today_timings['Fajr']}")
    print(f"Dhuhr: {today_timings['Dhuhr']}")
    print(f"Asr: {today_timings['Asr']}")
    print(f"Maghrib: {today_timings['Maghrib']}")
    print(f"Isha: {today_timings['Isha']}")
else:
    print("No timings found for today.")


next_prayer = None