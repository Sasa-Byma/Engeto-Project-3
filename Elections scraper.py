"""
Elections 2017 scraper
Project No. 3
"""

import requests
import csv
from bs4 import BeautifulSoup
import sys


def check_args(bad_urls, base_url, argv):
    if len(argv) == 3:

        try:
            url = str(argv[1])
            csv_file = str(argv[2])

            if (base_url not in url) or url in bad_urls:
                sys.exit("Wrong URL for scraping")
            else:
                return url, csv_file

        except ValueError:
            sys.exit("Wrong type of arguments")
    else:
        sys.exit("Wrong number of arguments")


def get_municip_info(district_url, muni_code):
    try:
        electweb = requests.get("https://volby.cz/pls/ps2017nss/" + district_url)
        bouillon = BeautifulSoup(electweb.text, "html.parser")
        el_data = [muni_code]

    except requests.exceptions.ConnectionError as e:
        sys.exit(f"Problem with connection: {e}")

    # print(bouillon)
    for i in bouillon.find_all("h3"):
        if "Obec" in i.text:
            el_data.append(i.text.split(":")[-1].strip())
    el_data.append(bouillon.find("td", attrs={"headers": "sa2"}).text.replace("\xa0", ""))
    el_data.append(bouillon.find("td", attrs={"headers": "sa3"}).text.replace("\xa0", ""))
    el_data.append(bouillon.find("td", attrs={"headers": "sa6"}).text.replace("\xa0", ""))
    for x in bouillon.find_all("td", attrs={"headers": "t1sa2 t1sb3"}):
        el_data.append(x.text.replace("\xa0", " "))
    for x in bouillon.find_all("td", attrs={"headers": "t2sa2 t2sb3", "class": "number"}):
        el_data.append(x.text.replace("\xa0", " "))
    return el_data


def write_csv(header, el_data, filename):
    f = open(filename + ".csv", "w", newline="\n")
    entry = csv.writer(f)
    entry.writerow(header)
    entry.writerows(el_data)
    f.flush()
    f.close()


def source(url):
    source = requests.get(url)
    soup = BeautifulSoup(source.text, "html.parser")
    return soup


def header(district_url):
    electweb = requests.get("https://volby.cz/pls/ps2017nss/" + district_url)
    zuppa = BeautifulSoup(electweb.text, 'html.parser')
    head22 = ["muni_code", "municipality", "registered voters", "envelopes", "valid votes"]
    for x in zuppa.find_all("td", attrs={"headers": "t1sa1 t1sb2"}):
        head22.append(x.text)
    for x in zuppa.find_all("td", attrs={"headers": "t2sa1 t2sb2", "class": ""}):
        head22.append(x.text)
    return head22


def el_data(source):
    el_data = [get_municip_info(x.find("a")["href"], x.text) for x in source.find_all("td", attrs={"class": "cislo"})]
    head22 = header(source.find("td", attrs={"class": "cislo"}).find("a")["href"])
    return (head22, el_data)


def checkurl(url):
    if "https://volby.cz/pls/ps2017nss/ps32" not in url:
        print("No reference to district selection page, please try again")
        return False
    else:
        return True


rightUrl = False
print("Using 'X', in 'Vyber obce' pick up a selection of municipalities to process from this address {}".format(
    "https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"))
while rightUrl == False:
    address = input("Copy the page reference here:")
    rightUrl = checkurl(address)
    csvfile = input("Please enter the csv file name")
    print("Processing ...")
    write_csv(*el_data((source(address))), csvfile)
    print(f"Done. The output is in  file {csvfile}.csv.")

