import os, subprocess, datetime

def dms_to_decimal(degrees: float, minutes: float, seconds: float) -> float:
    return degrees + minutes / 60.0 + seconds / 3600.0

files = os.listdir('.')
coordinates = []

for file in files:
    if not file.endswith('.jpg'):
        continue
    
    #GPS Position                    : 46 deg 30' 14.40", 17 deg 58' 26.40"
    info = subprocess.run(f'exiftool {file} | tail -n 1', capture_output=True, shell=True).stdout.strip().decode()
    info = info.split(': ')[1].split(', ')
    long = dms_to_decimal(float(info[0].split(' ')[0]), float(info[0].split(' ')[2][:-1]), float(info[0].split(' ')[3][:-1]))
    lat  = dms_to_decimal(float(info[1].split(' ')[0]), float(info[1].split(' ')[2][:-1]), float(info[1].split(' ')[3][:-1]))
    
    timestamp = subprocess.run(f'exiftool -DateTimeOriginal {file}', capture_output=True, shell=True).stdout.strip().decode()
    timestamp = timestamp.split(': ')[1]
    timestamp = datetime.datetime.strptime(timestamp, '%Y:%m:%d %H:%M:%S')

    coordinates.append((timestamp, long, lat))

sorted_coordinates = sorted(coordinates, key=lambda x: x[0])

groups = {}
for i in sorted_coordinates:
    if i[0].strftime('%Y-%m-%d') not in groups:
        groups[i[0].strftime('%Y-%m-%d')] = []
    
    groups[i[0].strftime('%Y-%m-%d')].append(i)

import matplotlib.pyplot as plt

colors = plt.cm.get_cmap('tab20', len(groups)).colors

plt.figure(figsize=(30, 5))
plt.xlabel('Longitude')
plt.ylabel('Latitude')
color_idx = 0

for i in groups:
    dots = groups[i]
    plt.plot([dot[2] for dot in dots], [dot[1] for dot in dots], color=colors[color_idx], linestyle='-', marker='o')
    color_idx += 1

plt.savefig('flag.png')
plt.show()
plt.close()