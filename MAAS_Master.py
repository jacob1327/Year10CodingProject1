import requests
import json
import time
import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import RangeSlider
from matplotlib.widgets import Button
from matplotlib.widgets import RadioButtons
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.collections import LineCollection


current_url = "https://api.maas2.apollorion.com"
current_response = (requests.get(current_url)).json()
current_sol = current_response["sol"]
current_season = current_response['season']
current_atmo_opacity = current_response['atmo_opacity']
current_sunrise = current_response['sunrise']
current_sunset = current_response['sunset']
uv_irradiance_index = current_response['local_uv_irradiance_index']

print(f'Today is Sol {current_sol}. Pick a Sol range from 1 to {current_sol}(~range of 100 sol values for quick use).')
start_sol = int(input("Enter start sol: "))
end_sol = int(input("Enter end sol: "))

def json_print(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

pressure_data = []
time_interval = []

def pressure_append(start_sol_initial, end_sol_initial, a, b):
    while start_sol_initial <= end_sol_initial:
        a.append(start_sol_initial)
        url = "https://api.maas2.apollorion.com/" + str(start_sol_initial)
        response = (requests.get(url)).json()
        print(start_sol_initial)
        if "pressure" in response:
            pressure = response["pressure"]
        else:
            pressure = None
        b.append(pressure)
        start_sol_initial += 1

pressure_append(start_sol, end_sol, time_interval, pressure_data)

#    print(pressure)
print(pressure_data)
time_interval2 = []

def max_temp_append(start_sol_initial, end_sol_initial, a, b):
    while start_sol_initial <= end_sol_initial:
        a.append(start_sol_initial)
        url = "https://api.maas2.apollorion.com/" + str(start_sol_initial)
        response = (requests.get(url)).json()
        print(start_sol_initial)
        if "max_temp" in response:
            max_temp = response["max_temp"]
        else:
            max_temp = None
        b.append(max_temp)
        start_sol_initial += 1

def min_temp_append(start_sol_initial, end_sol_initial, b):
    while start_sol_initial <= end_sol_initial:
        url = "https://api.maas2.apollorion.com/" + str(start_sol_initial)
        response = (requests.get(url)).json()
        print(start_sol_initial)
        if "min_temp" in response:
            min_temp = response["min_temp"]
        else:
            min_temp = None
        b.append(min_temp)
        start_sol_initial += 1

def gts_temp_append(start_sol_initial, end_sol_initial, a, b):
    while start_sol_initial <= end_sol_initial:
        b.append(start_sol_initial)
        url = "https://api.maas2.apollorion.com/" + str(start_sol_initial)
        response = (requests.get(url)).json()
        print(start_sol_initial)
        if "max_gts_temp" in response and type(response["max_gts_temp"]) == int:
            avg_gts_temp = (response["max_gts_temp"] + response["min_gts_temp"]) / 2
        else:
            avg_gts_temp = None
        a.append(avg_gts_temp)
        start_sol_initial += 1

fig = plt.figure(figsize=(18, 8.1))

ax = plt.axes()

pos = ax.get_position()
pos.x0 = 0.25       # for example 0.2, choose your value
ax.set_position(pos)

min_max_list1 = []
for i in pressure_data:
    if type(i) == int:
        min_max_list1.append(i)

avg_pressure = sum(min_max_list1) / len(min_max_list1)
filtered_list = []
for i in pressure_data:
    if type(i) == int:
        filtered_list.append(i)
    else:
        filtered_list.append(avg_pressure)


x = np.array(time_interval)
y1a = np.array(filtered_list)
y = np.array(pressure_data)
y_1 = np.array(filtered_list)
g, = plt.plot(x, y, 'r', label="atmospheric pressure")
x1b = np.array([])
y1b = np.array([])
h, = plt.plot(x1b, y1b, 'b')
m, b = np.polyfit(x, y_1, 1)
fill_between_col1 = ax.fill_between(x, y1a, y1a, color='red', alpha=0)
fill_between_col2 = ax.fill_between(x, y1a, y1a, color='red', alpha=0)

r, = plt.plot(x, m*x + b, 'g')

plt.text(0.075, 0.7, f"Today is Sol {current_sol} \n Season: {current_season} \n Opacity: {current_atmo_opacity} \n "
                     f"Sunrise: {current_sunrise} \n Sunset: {current_sunset} \n UV Index: {uv_irradiance_index}", fontfamily='monospace', fontsize=11, fontweight='bold', bbox=dict(boxstyle='square', fc="w", ec="k"), transform=plt.gcf().transFigure)

plt.title('Atmospheric Pressure on Mars')
plt.xlabel('Mars Sol')
plt.ylabel('Atmospheric Pressure(kPa)')
increment1 = round((max(time_interval) - min(time_interval))/5)
plt.xticks(np.arange(min(time_interval), max(time_interval)+increment1, increment1))


# l = plt.legend(loc="upper left")


# Create the RangeSlider
slider_ax = plt.axes([0.15, 0.02, 0.53, 0.03])
# slider = RangeSlider(slider_ax, "Martian Sol  ", 1, current_sol, (3000, current_sol))
slider = RangeSlider(slider_ax, "Martian Sol ", 0, current_sol, (start_sol, end_sol))


radio_ax = plt.axes([0.036, 0.1, 0.2, 0.2], frameon=True, aspect='equal')
radio = RadioButtons(radio_ax, ('pressure', 'max/min temp', 'gts_temp'))

for circle in radio.circles: # adjust radius here. The default is 0.05
    circle.set_radius(0.05)

# update figure to range slider values

def update(val):
    global start_point
    global end_point
    start_point = round(val[0])
    end_point = round(val[1])


def refresh(val):
    global cbar
    global lc
    global start_point
    print(start_point)
    print(end_point)
    global time_interval
    global max_temp_data
    global min_temp_data
    global fill_between_col1
    global fill_between_col2
    radio_value = radio.value_selected
    if radio_value == "pressure":
        time_interval = []
        pressure_data = []
        pressure_append(start_point, end_point, time_interval, pressure_data)
        print(time_interval)
        print(pressure_data)
        min_max_list = []
        for i in pressure_data:
            if type(i) == int:
                min_max_list.append(i)

        avg_pressure = sum(min_max_list) / len(min_max_list)
        print(avg_pressure)
        filtered_list = []
        for i in pressure_data:
            if type(i) == int:
                filtered_list.append(i)
            else:
                filtered_list.append(avg_pressure)

        increment2 = round((max(time_interval) - min(time_interval)) / 5)
        increment3 = round((max(min_max_list) - min(min_max_list)) / 6)
        ax.set_xlim([min(time_interval), max(time_interval)])
        ax.set_ylim([min(min_max_list), max(min_max_list)])
        ax.set_yticks(np.arange(min(min_max_list), max(min_max_list) + 1, increment3))
        ax.set_xticks(np.arange(min(time_interval), max(time_interval) + 1, increment2))
        # set x and y values of updated figure
        g.set_xdata(time_interval)
        g.set_ydata(pressure_data)

        x1 = np.array(time_interval)
        y2 = np.array(filtered_list)
        m, b = np.polyfit(x1, y2, 1)
        r.set_xdata(time_interval)
        r.set_ydata(m * x1 + b)

        # Redraw the figure to ensure it updates
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.1)

    elif radio_value == "max/min temp":

        max_temp_data = []
        min_temp_data = []
        time_interval2 = []
        ax.set_title('Maximum/Minimum Temperature on Mars')
        ax.set_ylabel('Temperature(°C)')
        max_temp_append(start_point, end_point, time_interval2, max_temp_data)
        min_temp_append(start_point, end_point, min_temp_data)

        print(max_temp_data)
        print(min_temp_data)
        min_max_list1 = []
        for i in max_temp_data:
            if type(i) == int:
                min_max_list1.append(i)

        avg_max_temp = sum(min_max_list1) / len(min_max_list1)
        filtered_list1 = []
        for i in max_temp_data:
            if type(i) == int:
                filtered_list1.append(i)
            else:
                filtered_list1.append(avg_max_temp)

        min_max_list2 = []
        for i in min_temp_data:
            if type(i) == int:
                min_max_list2.append(i)

        avg_min_temp = sum(min_max_list2) / len(min_max_list2)
        filtered_list2 = []
        for i in min_temp_data:
            if type(i) == int:
                filtered_list2.append(i)
            else:
                filtered_list2.append(avg_min_temp)

        total_list = []
        for i in min_max_list1:
            total_list.append(i)
        for i in min_max_list2:
            total_list.append(i)
        print(filtered_list1)
        print(filtered_list2)
        print(time_interval2)
        increment2 = round((max(time_interval2) - min(time_interval2)) / 5)
        increment3 = round((max(total_list) - min(total_list)) / 6)
        ax.set_xlim([min(time_interval2), max(time_interval2)])
        ax.set_ylim([min(total_list), max(total_list)])
        ax.set_yticks(np.arange(min(total_list), max(total_list) + 1, increment3))
        ax.set_xticks(np.arange(min(time_interval2), max(time_interval2) + 1, increment2))

        g.set_xdata(time_interval2)
        g.set_ydata(filtered_list1)

        h.set_xdata(time_interval2)
        h.set_ydata(filtered_list2)

        fill_between_col1 = ax.fill_between(time_interval2, filtered_list1, 0, color='red', alpha=0.30, figure=fig)
        fill_between_col2 = ax.fill_between(time_interval2, filtered_list2, filtered_list1, color='blue', alpha=0.30, figure=fig)

        # ax.get_legend().remove()

        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.1)

    elif radio_value == "gts_temp":

        cbar.remove()
        lc.remove()

        gts_temp_data = []
        time_interval3 = []
        gts_temp_append(start_point, end_point, gts_temp_data, time_interval3)

        if fill_between_col1 in ax.collections:
            ax.collections.remove(fill_between_col1)
            ax.collections.remove(fill_between_col2)

        gts_min_max_list = []
        for i in gts_temp_data:
            if type(i) == float:
                gts_min_max_list.append(i)

        average = sum(gts_min_max_list) / len(gts_min_max_list)

        filtered_list3 = []
        for i in gts_temp_data:
            if type(i) == float:
                filtered_list3.append(i)
            else:
                filtered_list3.append(average)

        ax.set_title('GTS Temperature on Mars')
        ax.set_ylabel('Temperature(ºK)')
        increment2 = round((max(time_interval3) - min(time_interval3)) / 5)
        increment3 = round((max(gts_min_max_list) - min(gts_min_max_list)) / 6)
        ax.set_xlim([min(time_interval3), max(time_interval3)])
        ax.set_ylim([min(gts_min_max_list), max(gts_min_max_list)])
        ax.set_yticks(np.arange(min(gts_min_max_list), max(gts_min_max_list) + 1, increment3))
        ax.set_xticks(np.arange(min(time_interval3), max(time_interval3) + 1, increment2))

        print(time_interval3)
        print(filtered_list3)

        x2 = np.array(time_interval3)
        y2 = np.array(filtered_list3)

        # set x and y values of updated figure
        g.set_xdata(time_interval3)
        g.set_ydata(filtered_list3)

        points = np.array([x2, y2]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        print(segments)
        # Create a continuous norm to map from data points to colors
        norm = plt.Normalize(min(gts_min_max_list), max(gts_min_max_list))
        lc = LineCollection(segments, cmap='autumn', norm=norm)
        # Set the values used for colormapping
        lc.set_array(filtered_list3)
        lc.set_linewidth(3)
        line = ax.add_collection(lc)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.2)

        cbar = fig.colorbar(line, ax=ax, cax=cax)

        # Redraw the figure to ensure it updates
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.1)




def visualization_selection(graph_type):
    global cbar
    global lc
    global line
    global cax
    global segments
    global norm
    global filtered_list1
    global filtered_list2
    global time_interval3
    global filtered_list3
    global fill_between_col1
    global fill_between_col2

    starting_point = round(slider.val[0])
    ending_point = round(slider.val[1])

    if graph_type == 'max/min temp':
        if ax.get_title() == "GTS Temperature on Mars":
            cbar.remove()
            lc.remove()


        max_temp_data = []
        min_temp_data = []
        time_interval2 = []
        ax.set_title('Maximum/Minimum Temperature on Mars')
        ax.set_ylabel('Temperature(°C)')
        max_temp_append(starting_point, ending_point, time_interval2, max_temp_data)
        min_temp_append(starting_point, ending_point, min_temp_data)

        print(max_temp_data)
        print(min_temp_data)
        min_max_list1 = []
        for i in max_temp_data:
            if type(i) == int:
                min_max_list1.append(i)

        avg_max_temp = sum(min_max_list1) / len(min_max_list1)
        filtered_list1 = []
        for i in max_temp_data:
            if type(i) == int:
                filtered_list1.append(i)
            else:
                filtered_list1.append(avg_max_temp)

        min_max_list2 = []
        for i in min_temp_data:
            if type(i) == int:
                min_max_list2.append(i)

        avg_min_temp = sum(min_max_list2) / len(min_max_list2)
        filtered_list2 = []
        for i in min_temp_data:
            if type(i) == int:
                filtered_list2.append(i)
            else:
                filtered_list2.append(avg_min_temp)

        total_list = []
        for i in min_max_list1:
            total_list.append(i)
        for i in min_max_list2:
            total_list.append(i)
        print(filtered_list1)
        print(filtered_list2)
        increment2 = round((max(time_interval) - min(time_interval)) / 5)
        increment3 = round((max(total_list) - min(total_list)) / 6)
        ax.set_xlim([min(time_interval), max(time_interval)])
        ax.set_ylim([min(total_list), max(total_list)])
        ax.set_yticks(np.arange(min(total_list), max(total_list) + 1, increment3))
        ax.set_xticks(np.arange(min(time_interval), max(time_interval) + 1, increment2))

        g.set_xdata(time_interval)
        g.set_ydata(filtered_list1)

        h.set_xdata(time_interval)
        h.set_ydata(filtered_list2)

        fill_between_col1 = ax.fill_between(time_interval, filtered_list1, 0, color='red', alpha=0.30, figure=fig)
        fill_between_col2 = ax.fill_between(time_interval, filtered_list2, filtered_list1, color='blue', alpha=0.30, figure=fig)

        # ax.get_legend().remove()

        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.1)

    if graph_type == 'gts_temp':

        gts_temp_data = []
        time_interval3 = []
        gts_temp_append(starting_point, ending_point, gts_temp_data, time_interval3)

        if fill_between_col1 in ax.collections:
            ax.collections.remove(fill_between_col1)
            ax.collections.remove(fill_between_col2)

        gts_min_max_list = []
        for i in gts_temp_data:
            if type(i) == float:
                gts_min_max_list.append(i)

        average = sum(gts_min_max_list) / len(gts_min_max_list)

        filtered_list3 = []
        for i in gts_temp_data:
            if type(i) == float:
                filtered_list3.append(i)
            else:
                filtered_list3.append(average)

        ax.set_title('GTS Temperature on Mars')
        ax.set_ylabel('Temperature(ºK)')
        increment2 = round((max(time_interval3) - min(time_interval3)) / 5)
        increment3 = round((max(gts_min_max_list) - min(gts_min_max_list)) / 6)
        ax.set_xlim([min(time_interval3), max(time_interval3)])
        ax.set_ylim([min(gts_min_max_list), max(gts_min_max_list)])
        ax.set_yticks(np.arange(min(gts_min_max_list), max(gts_min_max_list) + 1, increment3))
        ax.set_xticks(np.arange(min(time_interval3), max(time_interval3) + 1, increment2))

        print(time_interval3)
        print(filtered_list3)

        x2 = np.array(time_interval3)
        y2 = np.array(filtered_list3)

        # set x and y values of updated figure
        g.set_xdata(time_interval3)
        g.set_ydata(filtered_list3)

        points = np.array([x2, y2]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        print(segments)
        # Create a continuous norm to map from data points to colors
        norm = plt.Normalize(min(gts_min_max_list), max(gts_min_max_list))
        lc = LineCollection(segments, cmap='autumn', norm=norm)
        # Set the values used for colormapping
        lc.set_array(filtered_list3)
        lc.set_linewidth(3)
        line = ax.add_collection(lc)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.2)

        cbar = fig.colorbar(line, ax=ax, cax=cax)

        # Redraw the figure to ensure it updates
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.1)

    if graph_type == "pressure":
        if fill_between_col1 in ax.collections:
            ax.collections.remove(fill_between_col1)
            ax.collections.remove(fill_between_col2)
        if ax.get_title() == "GTS Temperature on Mars":
            cbar.remove()
            lc.remove()

        time_interval4 = []
        pressure_data = []
        pressure_append(starting_point, ending_point, time_interval4, pressure_data)


        print(time_interval4)
        print(pressure_data)

        min_max_list = []
        for i in pressure_data:
            if type(i) == int:
                min_max_list.append(i)

        avg_pressure = sum(min_max_list) / len(min_max_list)
        print(avg_pressure)

        filtered_list = []
        for i in pressure_data:
            if type(i) == int:
                filtered_list.append(i)
            else:
                filtered_list.append(avg_pressure)

        increment2 = round((max(time_interval4) - min(time_interval4)) / 5)
        increment3 = round((max(min_max_list) - min(min_max_list)) / 6)
        ax.set_xlim([min(time_interval4), max(time_interval4)])
        ax.set_ylim([min(min_max_list), max(min_max_list)])
        ax.set_yticks(np.arange(min(min_max_list), max(min_max_list) + 1, increment3))
        ax.set_xticks(np.arange(min(time_interval4), max(time_interval4) + 1, increment2))
        # set x and y values of updated figure
        g.set_xdata(time_interval4)
        g.set_ydata(pressure_data)
        ax.set_title('Atmospheric Pressure on Mars')
        ax.set_ylabel('Atmospheric Pressure on Mars(kPa)')
        x1 = np.array(time_interval4)
        y2 = np.array(filtered_list)
        m, b = np.polyfit(x1, y2, 1)
        r.set_xdata(time_interval4)
        r.set_ydata(m * x1 + b)

        # Redraw the figure to ensure it updates
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.1)

radio.on_clicked(visualization_selection)

# Create the Button
button_ax = plt.axes([0.769, 0.015, 0.1, 0.040])

# Create the Download Button
button_ax2 = plt.axes([0.84, 0.015, 0.1, 0.040])

def download(val):
    radio_value = radio.value_selected
    if radio_value == 'pressure':
        categories = ['Sol', 'Pressure']

        sol_column = time_interval
        weather_data = pressure_data
        print('hi')

        with open('mars_weather_data.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(categories)
            writer.writerows(zip(sol_column, weather_data))

    elif radio_value == 'max/min temp':
        categories = ['Sol', 'Maximum Temperature', 'Minimum Temperature']

        sol_column = time_interval
        weather_data = filtered_list1
        weather_data2 = filtered_list2

        with open('mars_weather_data.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(categories)
            writer.writerows(zip(sol_column, weather_data, weather_data2))
    elif radio_value == 'gts_temp':
        categories = ['Sol', 'GTS Temperature']

        sol_column = time_interval3
        weather_data = filtered_list3

        with open('mars_weather_data.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(categories)
            writer.writerows(zip(sol_column, weather_data))


download_image = plt.imread('download_button.jpg')
download_button = Button(button_ax2, "", image=download_image, color='0.85', hovercolor='0.95')
download_button.on_clicked(download)

# slider = RangeSlider(slider_ax, "Martian Sol  ", 1, current_sol, (3000, current_sol))
refresh_button = Button(button_ax, "Refresh", image=None, color='0.85', hovercolor='0.95')
refresh_button.on_clicked(refresh)

slider.on_changed(update)

mng = plt.get_current_fig_manager()
mng.full_screen_toggle()

plt.show()
