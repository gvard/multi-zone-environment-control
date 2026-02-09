"""Python script for plotting temperature monitoring data
"""

from datetime import datetime, timedelta
from argparse import ArgumentParser

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator

parser = ArgumentParser(
    description="Python script for plotting temperature monitoring data"
)
parser.add_argument("filenames", type=str, default="", nargs='+', metavar='FILES',
                    help="input CSV data file(s)")
args = parser.parse_args()

FORMAT = "%d.%m.%Y %H:%M:%S"
XMAJOR_LOCATOR = 4
XMINOR_LOCATOR = 1
YMINOR_LOCATOR = 0.5
columns = ["date", "time", "temp"]

fig, ax = plt.subplots(figsize=(16, 9))

xlims = []
extremes = []
for i, nam in enumerate(args.filenames):
    data = pd.read_csv(nam, header=0, names=columns)
    data['datetime'] = pd.to_datetime(data['date'] + ' ' + data['time'], format=FORMAT)
    xlims.append((data['datetime'].iloc[0], data['datetime'].iloc[-1]))
    extremes.append(min(data['temp']))
    extremes.append(max(data['temp']))
    if not i:
        plt.plot(data['datetime'], data['temp'], "-o", lw=1, color='blue', label='Температура с USB термодатчика')
    else:
        plt.plot(data['datetime'], data['temp'], "-o", lw=1, color='blue')

temp_delta = 0.5
ylims = (min(extremes) - temp_delta, max(extremes) + temp_delta)

current_date = xlims[0][0].replace(hour=0, minute=0, second=0, microsecond=0)
while current_date <= xlims[-1][-1]:
        plt.plot((current_date, current_date), ylims, "-k", lw=2, zorder=-5)
        current_date += timedelta(days=1)

plt.title('Изменения температуры в помещении')
plt.xlabel('Время, ДД ЧЧ:ММ')
plt.ylabel('Температура, °C')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
td = timedelta(minutes=50)
plt.xlim(xlims[0][0] - td, xlims[-1][-1] + td)
plt.ylim(ylims)
plt.legend(loc="upper left")

ax.xaxis.set_major_locator(mdates.HourLocator(interval=XMAJOR_LOCATOR))
ax.xaxis.set_minor_locator(mdates.HourLocator(interval=XMINOR_LOCATOR))
date_form = mdates.DateFormatter('%d %H:%M')
ax.xaxis.set_major_formatter(date_form)
ax.yaxis.set_minor_locator(MultipleLocator(YMINOR_LOCATOR))
ax.tick_params(which="major", length=3.5)
ax.tick_params(which="minor", length=2.5)
# plt.show()
plt.savefig("temperatures.png", dpi=160)
