import requests
import base64
import csv
import time
import argparse
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def wigle_lookup(bssid, headers):
    url = f"https://api.wigle.net/api/v2/network/search?netid={bssid}"

    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()

        if data["success"] and data["resultCount"] > 0:
            rec = data["results"][0]

            return {
                "ssid": rec.get("ssid",""),
                "bssid": bssid,
                "lat": rec.get("trilat",""),
                "lon": rec.get("trilong",""),
                "city": rec.get("city",""),
                "country": rec.get("country","")
            }

    except:
        pass

    return {
        "ssid":"",
        "bssid":bssid,
        "lat":"",
        "lon":"",
        "city":"",
        "country":""
    }


def create_kml(results, filename):

    with open(filename,"w",encoding="utf-8") as f:

        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        f.write('<Document>\n')

        for r in results:

            if r["lat"] and r["lon"]:

                f.write(f'''
<Placemark>
<name>{r["ssid"]}</name>
<description>{r["bssid"]}</description>
<Point>
<coordinates>{r["lon"]},{r["lat"]},0</coordinates>
</Point>
</Placemark>
''')

        f.write('</Document>\n</kml>')


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input",required=True)
    parser.add_argument("-o","--output",default="wigle_results.csv")
    parser.add_argument("--kml",default="wifi_map.kml")
    parser.add_argument("--user",required=True)
    parser.add_argument("--token",required=True)
    parser.add_argument("--threads",type=int,default=5)

    args = parser.parse_args()

    auth = f"{args.user}:{args.token}"
    auth_b64 = base64.b64encode(auth.encode()).decode()

    headers = {
        "Authorization":f"Basic {auth_b64}"
    }

    with open(args.input) as f:
        bssids = list(set(line.strip() for line in f if line.strip()))

    results = []

    with ThreadPoolExecutor(max_workers=args.threads) as executor:

        futures = []

        for bssid in bssids:
            futures.append(executor.submit(wigle_lookup,bssid,headers))

        for future in tqdm(futures):
            results.append(future.result())

    with open(args.output,"w",newline="",encoding="utf-8") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=["ssid","bssid","lat","lon","city","country"]
        )

        writer.writeheader()
        writer.writerows(results)

    create_kml(results,args.kml)

    print("Finished.")
    print("CSV:",args.output)
    print("KML:",args.kml)


if _name_ == "_main_":
    main()
