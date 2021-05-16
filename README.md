# Engeto-Project-3
Elections scraper

Scrapes election data for selected county in Czechia (2017) from "https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ". Project for Engeto Academy. Script extracts election results from each municipality od selected county into a csv file.

Czech Parliament elections 2017.

Please select a county through X in a column "Vyber obce" in https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ. Then enter an url of selected county into an imput line of the script. For instance for county Nymburk enter this url: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2108.

Next you are asked for the name of csv file. Please enter just name without .csv.

Csv output file contains a header with each municipality code, municipality name, number of registered voters, accepted envelopes, valid votes and names of political parties. Each municipality numbers are on a separate line in an alphabetical order.

An example of csv output for Nymburk county is to be found in the same directory.
