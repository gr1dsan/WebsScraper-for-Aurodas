# **Aurodas Web Scraper**

A **web scraper** for rental listings from [Aruodas.lt](https://en.aruodas.lt/butu-nuoma/kaune/), built using **Python**, **Playwright**, and **BeautifulSoup**.  
This project collects detailed property information, including prices, area, rooms, building details, and more, and saves it to a **CSV file**.

The goal of this project is to **automatically extract property data** from the Aruodas website for analysis or record-keeping. This tool is also useful for **learning web scraping with Playwright** and handling websites that require **browser interactions**.

---

**Libraries Used**

- **Python 3.13**
- **Playwright** – for controlling a headless/visible browser to navigate and interact with web pages.
- **BeautifulSoup** – for parsing HTML and extracting data.
- **CSV** – for saving structured output.
- **Random & Time** – for simulating human-like behavior (scrolling and delays) to prevent being blocked.


**How it works:**

- Launches a visible Chromium browser for **better debugging**.
- Visits each page of rental listings and collects links to individual properties.
- Visits each property link and extracts information like name, price, area, rooms, building type, heating system, and crime data.
- Moves the mouse and scrolls randomly on pages to mimic human interaction and avoid detection.
- Saves all collected data into a **CSV file**.

---

## **Installation & Usage**

1. **Clone the repository**:
```bash
git clone https://github.com/gr1dsan/WebsScraper-for-Aurodas.git
```
2. **Enter the repo folder**:
```bash
cd WebsScraper-for-Aurodas
```
3. **Set up your virtual enviroment**:

####    For Mac/Linux:
```bash
python3 venv env
source env/bin/activate
```

#### For Windows:
```bash
python -m venv env
.\env\Scripts\activate
```
4. **Install all dependencies**:
```bash
pip install -r requirements.txt
```
5. **Run the program**:
```bash
python app.py
```
