import json, time, requests, datetime, time

def test():
    with open("logs.json", "r") as f:
        contenu = json.load(f)
    
    status_site_1 = (requests.get(f'{url_site_1}')).status_code
    status_site_2 = (requests.get(f'{url_site_2}')).status_code
    temps = (datetime.datetime.now()).strftime('%H:%M:%S')



    contenu["site_1"]['status'].append(f"{status_site_1}")
    contenu["site_1"]['time_test'].append(f"{temps}")
    contenu["site_2"]['status'].append(f"{status_site_2}")
    contenu["site_2"]['time_test'].append(f"{temps}")

    # print(contenu)

    with open("logs.json", "w") as f:
        json.dump(contenu, f, indent=4)
# test()
# while True:
#     time.sleep(3)
#     test()