# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 19:02:21 2023

@author: Mehran najafoo
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import nltk
# from nltk.corpus import stopwords
import tkinter as tk
from tkinter import simpledialog, filedialog

def get_user_inputs():
    root = tk.Tk()
    root.withdraw()

    base_url = simpledialog.askstring("Input", "Enter the base URL:")
    num_pages = simpledialog.askinteger("Input", "Enter the number of pages:")
    file_name = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    return base_url, num_pages, file_name

class AmazonReviewScraper:
    def __init__(self):
        self.review_list = []
        # nltk.download('stopwords')
        # self.stop_words = set(stopwords.words('english'))

    def get_soap(self, url):
        r = requests.get("http://localhost:8050/render.html", params={"url": url, "wait": 2})
        soap = BeautifulSoup(r.text, "html.parser")
        return soap

    def get_reviews(self, soap):
        reviews = soap.find_all("div", {"data-hook": "review"})
        try:
            for item in reviews:
                review = {
                    "product": soap.title.text.replace("Amazon.ca:Customer reviews:", "").strip(),
                    "title": item.find("a", {"data-hook": "review-title"}).text.strip(),
                    "rating": item.find("i", {"data-hook": "review-star-rating"}).text.replace(" out of 5 stars", "").strip(),
                    "body": item.find("span", {"data-hook": "review-body"}).text.strip().lower()
                }

                self.review_list.append(review)

        except:
            pass

    def scrape_reviews(self, base_url, num_pages):
        for x in range(1, num_pages + 1):
            soap = self.get_soap(f"{base_url}/ref=cm_cr_arp_d_paging_btm_next_{x}?ie=UTF8&pageNumber={x}&reviewerType=all_reviews")
            self.get_reviews(soap)

            if not soap.find("li", {"class": "a-disabled a-last"}):
                pass
            else:
                break

    def save_reviews(self, file_name):
        df = pd.DataFrame(self.review_list)
        df.to_csv(file_name, index=False)
     
   
if __name__ == "__main__":
    scraper = AmazonReviewScraper()

    base_url, num_pages, file_name = get_user_inputs()

    scraper.scrape_reviews(base_url, num_pages)
    scraper.save_reviews(file_name)
    print("Fin")

