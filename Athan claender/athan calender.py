import requests
from datetime import datetime
import json

country = input('enter country: ').lower().title()
city = input('enter city: ').lower().capitalize()

date_today = datetime.today()
year = date_today.year
month = date_today.month

url = f'http://api.aladhan.com/v1/calendarByCity/{year}/{month}?city={city}&country={country}&method=4'

response = requests.get(url=url)
data = response.json()

output_data = []

for entry in data['data']:
    timings = entry['timings']
    for key, value in timings.items():
        timings[key] = value.split(' ')[0]
        time_obj = datetime.strptime(timings[key], "%H:%M")
        timings[key] = time_obj.strftime("%I:%M %p")

    hijri_day = entry['date']['hijri']['weekday']['en']
    hijri_date = entry['date']['hijri']['date']
    
    gregorian_date = entry['date']['gregorian']['date']
    gregorian_day = entry['date']['gregorian']['weekday']['en']

    date_info = {
        'hijri': f'{hijri_day} {hijri_date}',
        'gregorian': f'{gregorian_day} {gregorian_date}',
        'timings': {
            'Fajr': timings['Fajr'],
            'Dhuhr': timings['Dhuhr'],
            'Asr': timings['Asr'],
            'Maghrib': timings['Maghrib'],
            'Isha': timings['Isha']
        }
    }

    output_data.append(date_info)

# Save data to a JSON file
output_file_path = r'D:\programing\Athan claender\prayer_time.json'
with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(output_data, json_file, indent=4)

print(f'Data has been saved to {output_file_path}')
