"""Python script for plotting temperature monitoring data
Example usage:
python plot_temperature_data.py data/260129-0201.log data/260206-0222.log -o data/odtemp-260206-0208.log data/odtemp-260208.log data/odtemp-260210-0213.log data/odtemp-260215.log data/odtemp-260222.log
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

fig, ax = plt.subplots(figsize=(16, 9))

for i, nam in enumerate(args.filenames):
    data = pd.read_csv(nam, header=0, names=columns)
    data["datetime"] = pd.to_datetime(data["date"] + " " + data["time"], format=FORMAT)
    xlims.append(data["datetime"].iloc[0])
    xlims.append(data["datetime"].iloc[-1])
    extremes.append(min(data["temp"]))
    extremes.append(max(data["temp"]))
    if not i:
        plt.plot(data["datetime"], data["temp"], "ok", lw=1, label="Показания термометров")
        datad = data[data["flag"] == "d"]
        plt.plot(datad["datetime"], datad["temp"], "og", lw=1, markeredgecolor="k", mew=0.5, ms=MS, zorder=7,
                 label="Показания термометра c фоторегистрацией")
        datad = data[data["flag"] == "t"]
        plt.plot(datad["datetime"], datad["temp"], "or", lw=1, markeredgecolor="k", mew=0.5, ms=MS, zorder=7,
                 label="Показания термометра на высоте 2 м")
    else:
        plt.plot(data["datetime"], data["temp"], "ok", lw=1)
        datad = data[data["flag"] == "d"]
        plt.plot(datad["datetime"], datad["temp"], "og", lw=1, markeredgecolor="k", mew=0.5, ms=MS, zorder=7)
        datad = data[data["flag"] == "t"]
        plt.plot(datad["datetime"], datad["temp"], "or", lw=1, markeredgecolor="k", mew=0.5, ms=MS, zorder=7)

columns = ["date", "time", "temp"]
for i, nam in enumerate(args.odtfnames):
    data = pd.read_csv(nam, header=0, names=columns)
    data["datetime"] = pd.to_datetime(data["date"] + " " + data["time"], format=FORMAT)
    xlims.append(data["datetime"].iloc[0])
    xlims.append(data["datetime"].iloc[-1])
    extremes.append(min(data["temp"]))
    extremes.append(max(data["temp"]))
    if not i:
        plt.plot(data["datetime"], data["temp"], "-o", lw=1, color="blue", markeredgecolor="k", mew=0.5, ms=MS,
                 label="Температура с USB термодатчика")
    else:
        plt.plot(data["datetime"], data["temp"], "-o", lw=1, color="blue", markeredgecolor="k", mew=0.5, ms=MS)

temp_delta = 0.3
ylims = (min(extremes) - temp_delta, max(extremes) + temp_delta)

current_date = min(xlims).replace(hour=0, minute=0, second=0)
day = timedelta(days=1)
while current_date <= max(xlims) + day:
        plt.plot((current_date, current_date), ylims, "--k", lw=1, zorder=-5)
        current_date += day

plt.title("Измерения температуры в помещении")
plt.xlabel("Время, ДД.ММ", fontsize=12)
plt.ylabel("Температура, °C", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.7)
plt.tight_layout()
td = timedelta(minutes=180)
xlims = min(xlims) - td, max(xlims) + 2.5*td
plt.xlim(xlims)
plt.ylim(ylims)
plt.legend(loc="upper left")
plt.plot(xlims, [15, 15], "--r", lw=1, zorder=-5)
plt.plot(xlims, [18, 18], "--r", lw=1, zorder=-5)

ax.xaxis.set_major_locator(mdates.DayLocator(interval=XMAJOR_LOCATOR))
date_form = mdates.DateFormatter("%d.%m")  #  %H:%M
ax.xaxis.set_major_formatter(date_form)
ax.minorticks_on()
ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=XMINOR_LOCATOR))
ax.yaxis.set_major_locator(MultipleLocator(YMAJOR_LOCATOR))
ax.yaxis.set_minor_locator(MultipleLocator(YMINOR_LOCATOR))
ax.tick_params(which="major", length=3.5)
ax.tick_params(which="minor", length=2.5)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
# fig.set_dpi(DPI_SCREEN)
# plt.get_current_fig_manager().window.state('zoomed')
# plt.show()
plt.savefig("temperatures.png", dpi=DPI)
