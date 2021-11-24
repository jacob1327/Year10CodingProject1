import requests
import json

start_sol = int(input("Enter start sol: "))
end_sol = int(input("Enter end sol: "))

def jsonPrint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

scatterplot_data = []

while start_sol <= end_sol:
    url = "https://api.maas2.apollorion.com/" + str(start_sol)
    response = (requests.get(url)).json()
    min_temp = response["min_temp"]
    max_temp = response["max_temp"]
    average_temp = (min_temp + max_temp)/2
    print(average_temp)
    jsonPrint(response)

    start_sol += 1

