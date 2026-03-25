"""Python script for plotting temperature monitoring data along with weather data
Example usage:
python plot_temperature_data_with_weather.py 260129-0201.log 260206-0228.log 2603.log -o odtemp-260206-0208.log odtemp-260208.log odtemp-260210-0213.log odtemp-260215.log odtemp-260222.log odtemp-260227-0228.log odtemp-260301.log odtemp-260306.log odtemp-260313.log odtemp-260322.log
"""

from datetime import timedelta
from argparse import ArgumentParser

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator

parser = ArgumentParser(
    description="Python script for plotting temperature monitoring data"
)
parser.add_argument("filenames", nargs="+", metavar="FILES",
                    help="input CSV data file(s)")
parser.add_argument("-o", "--odtfnames", nargs="+", metavar="ODTFILES",
                    help="input CSV data file(s)")
args = parser.parse_args()

DATA_DIR = "data/"
FORMAT = "%d.%m.%Y %H:%M:%S"
XMAJOR_LOCATOR = 1
XMINOR_LOCATOR = range(0, 24, 6)
YMAJOR_LOCATOR = 1
YMINOR_LOCATOR = 0.5
MS = 7
DPI_SCREEN = 200
DPI = 160
columns = ["date", "time", "temp", "flag"]
xlims = []
extremes = []

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), sharex=True)

for i, nam in enumerate(args.filenames):
    data = pd.read_csv(DATA_DIR + nam, header=0, names=columns)
    data["datetime"] = pd.to_datetime(data["date"] + " " + data["time"], format=FORMAT)
    xlims.append(data["datetime"].iloc[0])
    xlims.append(data["datetime"].iloc[-1])
    extremes.append(min(data["temp"]))
    extremes.append(max(data["temp"]))
    if not i:
        ax1.plot(data["datetime"], data["temp"], "ok", lw=1, label="Показания термометров")
        datad = data[data["flag"] == "d"]
        ax1.plot(datad["datetime"], datad["temp"], "og", lw=1, markeredgecolor="k", mew=0.5, ms=MS, zorder=7,
                 label="Показания термометра c фоторегистрацией")
        datad = data[data["flag"] == "t"]
        ax1.plot(datad["datetime"], datad["temp"], "or", lw=1, markeredgecolor="k", mew=0.5, ms=MS, zorder=7,
                 label="Показания термометра на высоте 2 м")
    else:
        ax1.plot(data["datetime"], data["temp"], "ok", lw=1)
        datad = data[data["flag"] == "d"]
        ax1.plot(datad["datetime"], datad["temp"], "og", lw=1, markeredgecolor="k", mew=0.5, ms=MS, zorder=7)
        datad = data[data["flag"] == "t"]
        ax1.plot(datad["datetime"], datad["temp"], "or", lw=1, markeredgecolor="k", mew=0.5, ms=MS, zorder=7)

columns = ["date", "time", "temp"]
for i, nam in enumerate(args.odtfnames):
    data = pd.read_csv(DATA_DIR + nam, header=0, names=columns)
    data["datetime"] = pd.to_datetime(data["date"] + " " + data["time"], format=FORMAT)
    xlims.append(data["datetime"].iloc[0])
    xlims.append(data["datetime"].iloc[-1])
    extremes.append(min(data["temp"]))
    extremes.append(max(data["temp"]))
    if not i:
        ax1.plot(data["datetime"], data["temp"], "-o", lw=1, color="blue", markeredgecolor="k", mew=0.5, ms=MS,
                 label="Температура с USB термодатчика")
    else:
        ax1.plot(data["datetime"], data["temp"], "-o", lw=1, color="blue", markeredgecolor="k", mew=0.5, ms=MS)

temp_delta = 0.3
ylims = (min(extremes) - temp_delta, max(extremes) + temp_delta -1)

current_date = min(xlims).replace(hour=0, minute=0, second=0)
day = timedelta(days=1)
while current_date <= max(xlims) + day:
        ax1.plot((current_date, current_date), ylims, "--k", lw=1, zorder=-5)
        current_date += day

td = timedelta(minutes=180)
xlims = min(xlims) - td, max(xlims) + 2.0*td

plt.suptitle("Измерения температуры в помещении и температура воздуха на улице: Гидрометцентр России (Москва, ВДНХ)")
plt.xlabel("Время, ДД ЧЧ:ММ", fontsize=12)
fig.supylabel("Температура, °C", fontsize=12, x=0.01)
plt.tight_layout()

ax1.grid(True, linestyle="--", alpha=0.7)
ax1.set_xlim(xlims)
ax1.set_ylim(ylims)
ax1.legend(loc="upper left")
ax1.plot(xlims, [15, 15], "--r", lw=1, zorder=-5)
ax1.plot(xlims, [18, 18], "--r", lw=1, zorder=-5)

ax1.xaxis.set_major_locator(mdates.DayLocator(interval=XMAJOR_LOCATOR))
date_form = mdates.DateFormatter("%d.%m")  #  %H:%M
ax1.xaxis.set_major_formatter(date_form)
ax1.minorticks_on()
ax1.xaxis.set_minor_locator(mdates.HourLocator(byhour=XMINOR_LOCATOR))
ax1.yaxis.set_major_locator(MultipleLocator(YMAJOR_LOCATOR))
ax1.yaxis.set_minor_locator(MultipleLocator(YMINOR_LOCATOR))
ax1.tick_params(which="major", length=3.5)
ax1.tick_params(which="minor", length=2.5)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

XMAJOR_LOCATOR = 1
YMAJOR_LOCATOR = 1
YMINOR_LOCATOR = 0.5
columns = ["date", "time", "temp", "flag"]
xlims = []
extremes = []

weather_data = ["weather-2601-03.log",]
for i, nam in enumerate(weather_data):
    data = pd.read_csv(DATA_DIR + nam, header=0, names=columns)
    data["datetime"] = pd.to_datetime(data["date"] + " " + data["time"], format=FORMAT)
    xlims.append(data["datetime"].iloc[0])
    xlims.append(data["datetime"].iloc[-1])
    extremes.append(min(data["temp"]))
    extremes.append(max(data["temp"]))
    ax2.plot(data["datetime"], data["temp"], "ok", ms=5, lw=1, label="Температура на улице")

temp_delta = 0.3
ylims = (min(extremes) - temp_delta, max(extremes) + temp_delta)

current_date = min(xlims).replace(hour=0, minute=0, second=0)
day = timedelta(days=1)
while current_date <= max(xlims) + day:
        ax2.plot((current_date, current_date), ylims, "--k", lw=1, zorder=-5)
        current_date += day

ax2.xaxis.set_major_formatter(date_form)
ax2.minorticks_on()
ax2.xaxis.set_minor_locator(mdates.HourLocator(byhour=XMINOR_LOCATOR))
ax2.yaxis.set_major_locator(MultipleLocator(2))
ax2.tick_params(which="major", length=3.5)
ax2.tick_params(which="minor", length=2.5)
ax2.grid(True, linestyle="--", alpha=0.7)

ax2.set_ylim(-21.9, 2.9)
xlims = min(xlims) - td, max(xlims) + 2.0*td
plt.xlim(min(data["datetime"]), max(data["datetime"]))
ax2.legend(loc="upper left")

# plt.show()
plt.savefig("temperatures-with-weather.png", dpi=DPI)
