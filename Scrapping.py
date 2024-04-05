"""
Nama    : Tirta Rifky Fauzan
NIM     : 231524063
Kelas   : D4-1B
Web Scrapping 1:
Melakukan scrapping terhadap berita terkini dari 
website https://www.republika.co.id/ .

"""


import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from requests.exceptions import HTTPError
import subprocess

def get_content(url):
    try:
        page = requests.get(url)
        page.raise_for_status()  # HTTPError untuk bad response
        return page.text
    except HTTPError as e:
        print("HTTP Error:", e)
        return None

def scrape_web():
    # Fetch the HTML content from the URL
    html_content = get_content("https://www.republika.co.id/")
    if html_content is None:
        return None

    # Parse the HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Create a list to store the extracted information
    data = []

    # Get the current system time
    datetime_system = datetime.now().strftime("%d %B %Y %H:%M:%S")

    # Find all the div elements with class "container-lit"
    container_lit_divs = soup.find_all("div", class_="container-lit")

    # Iterate through each div with class "container-lit"
    for container_lit_div in container_lit_divs:
        # Find all the list items within the current "container-lit" div
        list_items = container_lit_div.find_all("li", class_="list-group-item list-border conten1")

        # Iterate through each list item
        for list_item in list_items:
            # Check if the list item has the class "eksternal"
            if "eksternal" not in list_item.get('class', []):
                # Find the date div within the current list item
                date_div = list_item.find("div", class_="date")

                # Extract the information from the date div

                kanal_info = date_div.find("span", class_="kanal-info").text.strip()
                time_info = date_div.text.strip().replace(kanal_info, "").strip()

                # Remove the leading "- " character from time_info
                time_info = time_info.lstrip("- ")

                # Extract the headline from the corresponding h3 tag
                headline = list_item.find("h3").text.strip() if list_item.find("h3") else None
                # Assign "None" to other values if headline is None
                if headline == "":
                    headline = "SUMBER BERITA PADA POSISI INI SEDANG DOWN!!!!!!!!!!"
                    kanal_info = "DOWN"
                    time_info = "DOWN"

                # Append the extracted information to the data list along with the current time
                data.append({
                    "Judul": headline,
                    "Kategori": kanal_info,
                    "Waktu Publish": time_info,
                    "Waktu Scrapping": datetime_system
                })

    return data


def save_to_json(data):
    if data is not None:
        # Read existing data from JSON file
        try:
            with open("Scrapped.json", "r") as json_file:
                json.load(json_file)
        except FileNotFoundError:
            pass

        # Write the updated data to the JSON file
        with open("Scrapped.json", "w") as json_file:
            json.dump(data, json_file, indent=4)
        print("Data telah disimpan di 'Scrapped.json'.")
    else:
        print("Data tidak ditemukan.")

def commit_and_push_changes():
    try:
        # Add changes to the staging area
        subprocess.run(["git", "add", "."], check=True)
        
        # Commit the changes
        subprocess.run(["git", "commit", "-m", "Update scraping data"], check=True)
        
        # Push the changes to the remote repository
        subprocess.run(["git", "push"], check=True)
        
        print("Changes have been committed and pushed to the remote repository.")
    except subprocess.CalledProcessError as e:
        print("Error:", e)

# Perform scraping
scraped_data = scrape_web()

# Save data to JSON if scraping was successful
save_to_json(scraped_data)

# Commit dan push changes ke GitHub
commit_and_push_changes()
