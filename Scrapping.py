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
    # Mendapatkan content dari website republika
    html_content = get_content("https://www.republika.co.id/")
    if html_content is None:
        return None

    # Parsing HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # List untuk penyimpanan data
    data = []

    # Mendapatkan waktu sistem sekarang
    datetime_system = datetime.now().strftime("%d %B %Y %H:%M:%S")

    # Mencari semua div pada class container-lit
    container_lit_divs = soup.find_all("div", class_="container-lit")

    # Iterasi terdahap setiap div "container-lit"
    for container_lit_div in container_lit_divs:
        # Mencari seluruh list pada class "list-group-item list-border conten1"
        list_items = container_lit_div.find_all("li", class_="list-group-item list-border conten1")

        # iterasi terhadap semua list pada class "list-group-item list-border conten1"
        for list_item in list_items:
            # check apabila terdapat class "eksternal" pada list item (class ini digunakan untuk iklan)
            if "eksternal" not in list_item.get('class', []):
                # Mencari div dengan class "date" pada list "list-group-item list-border conten1"
                date_div = list_item.find("div", class_="date")

                # Mengambil informasi kanal (kategori) dan waktu publish dari div "date"
                kanal_info = date_div.find("span", class_="kanal-info").text.strip()
                time_info = date_div.text.strip().replace(kanal_info, "").strip()

                # Menghapus karakter "- " dan spasi pada awal kalimat karena data waktu push dalam web 
                # memiliki String "- " di awal kalimat yang tidak diperlukan
                time_info = time_info.lstrip("- ")

                # Mendapatkan headline dari h3 pada list "list-group-item list-border conten1"
                headline = list_item.find("h3").text.strip() if list_item.find("h3") else None
                # Pengisian String apabila headline tidak ditemukan (headline kosong)
                if headline == "":
                    headline = "SUMBER BERITA PADA POSISI INI SEDANG DOWN!!!!!!!!!!"
                    kanal_info = "DOWN"
                    time_info = "DOWN"

                # Append seluruh data ke dalam list data
                data.append({
                    "Judul": headline,
                    "Kategori": kanal_info,
                    "Waktu Publish": time_info,
                    "Waktu Scrapping": datetime_system
                })
    # Mengembalikan List data
    return data

# Fungsi untuk menyimpan data ke dalam file JSON
def save_to_json(data):
    if data is not None:
        # Membaca data dalam file JSON
        try:
            with open("Scrapped.json", "r") as json_file:
                json.load(json_file)
        except FileNotFoundError:
            pass

        # Write data ke dalam file JSON
        with open("Scrapped.json", "w") as json_file:
            json.dump(data, json_file, indent=4)
        print("Data telah disimpan di 'Scrapped.json'.")
    else:
        print("Data tidak ditemukan.")

# Fungsi untuk commit dan push perubahan ke GitHub
def commit_and_push_changes():
    try:
        # Menambah perubahan ke staging area
        subprocess.run(["git", "add", "."], check=True)
        
        # Commit perubahan
        subprocess.run(["git", "commit", "-m", "Update scraping data"], check=True)
        
        # Push perubahan ke remote repository
        subprocess.run(["git", "push"], check=True)
        
        print("Commit dan Push Berhasil.")
    except subprocess.CalledProcessError as e:
        print("Error:", e)

# Pelaksanaan Scrapping
scraped_data = scrape_web()

# Save data ke dalam file JSON
save_to_json(scraped_data)

# Commit dan push perubahan ke GitHub
commit_and_push_changes()
