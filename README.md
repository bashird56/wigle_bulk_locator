# wigle_bulk_locator
python script to extract wigle data in mass 

Tracking the Suspect’s Precise Location Using Wigle.net 

every project starts with a problem we faced one to 

the problem was to extract the exact location of a suspect's location but not one but many 
the locations were many in this case to many
we looked every were to bypass the manual work but no use 
after a long reserch we were not able to automate this work so we build a script for us 
so we are sharing it with comunity 
for more context visit this site 
https://hackers-arise.com/osint-tracking-the-suspects-precise-location-using-wigle-net/

usage 

python wigle_bulk_locator.py 
-i bssid_list.txt 
-o results.csv 
--kml wifi_map.kml 
--user YOUR_WIGLE_USERNAME 
--token YOUR_WIGLE_API_TOKEN 
--threads 10
