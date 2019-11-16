from django.shortcuts import render, render_to_response
import csv
from django.http import HttpResponse
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import requests

def get_GPU_info_Newegg(request):
    try:
        page_number = 1
        num_pages = 2
        filename = "GPU_Data_Newegg.csv"
        f = open(filename, "w")
        headers = "brand,product_name,shipping\n"
        f.write(headers)

        while(page_number <= num_pages):
            page_number_url = "&Page=" + str(page_number)
            my_url = 'https://www.newegg.com/p/pl?Submit=StoreIM&Depa=1&Category=38'
            if(page_number != 1):
                my_url = 'https://www.newegg.com/p/pl?Submit=StoreIM&Depa=1&Category=38{}'.format(page_number_url)
            # opening up connection
            uClient = uReq(my_url)
            page_html = uClient.read()
            uClient.close()
            # html parsing
            page_soup = soup(page_html, "html.parser")
            # grabs each product
            containers = page_soup.findAll("div", {"class": "item-container"})
            if(not containers):
                print ("reached end of gpus")
                return
            container = containers[0]
            for container in containers:
                shipping_container = container.findAll("li", {"class": "price-ship"})
                brand = container.find("div", "item-info").div.a.img["title"]
                title = container.a.img["title"]
                shipping_info = shipping_container[0].text.strip()

                f.write(brand + "," + title.replace(",", "|") + "," + shipping_info + "\n")
            page_number += 1
        f.close()
        with open('GPU_Data_Newegg.csv') as myfile:
            response = HttpResponse(myfile, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=GPU_Data_Newegg.csv'
            return response
    finally:
        f.close()
        uClient.close()

def getGPUInfoAmazon(request):
    return HttpResponse("rip")


def get_GPU_info_MicroCenter(request):
    try:
        url = "https://www.microcenter.com/category/4294966937/video-cards"
        """Makes csv file"""
        filename = "GPU_Data_MicroCenter.csv"
        f = open(filename, "w")
        headers = "brand,product_name,availability,price\n"
        f.write(headers)
        """ Get html """
        uClient = uReq(url)
        page_html = uClient.read()
        soup_parser = soup(page_html, "html.parser")
        uClient.close()

        containers = soup_parser.findAll("li",{"class" : "product_wrapper"})
        for container in containers:
            # find containers for rebate, price, product, availability
            product_container = container.find("div", {"class":"pDescription compressedNormal2"})
            availability = container.find("div", {"class":"instore"})
            price = container.find("div", {"class" : "price"}).span.text
            rebate = container.find("div", {"class":"rebate-price"}).span.text

            if(len(rebate) != 0):
                price = "{} after rebate".format(rebate)
            product = product_container.h2.a["data-name"]
            brand = product.split(" ", 1)[0]
            f.write(brand + "," + product.replace(",", "|") + "," + availability.p.text + ',' + price + "\n")
        f.close()

        # build response
        with open('GPU_Data_MicroCenter.csv') as myfile:
            response = HttpResponse(myfile, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=GPU_Data_MicroCenter.csv'
            return response

    finally:
        f.close()
        uClient.close()

def get_GPU_info_Frys(request):
    try:
        url = "https://www.frys.com/search?query_search=&cat=-73022&nearbyStoreName=false&isKeyword=true&pType=pDisplay&fq=a%20Regular%20Items-101536%20Video_Cards&rows=100&sort=&start=0&cat=-73022&from=0&to=19"
        file_name = "GPU_Info_Frys.csv"
        f = open(file_name, "w")
        f.write("brand,product,shipping,price\n")
        uClient = uReq(url)
        page_html = uClient.read()
        uClient.close()
        soup_parser = soup(page_html, "html.parser")
        containers = soup_parser.findAll("div", {"id":"prodCol"})
        for container in containers:
            general_info = container.find("div", {"id":"prodDesc"})
            info_container = "col-xs-6 col-sm-6 col-md-6 font_xs pad_none_tab pad_none_desk grid_p mar-btm"

            product = general_info.p.small.b.a.string
            brand = general_info.findAll("p", {"class": info_container})[1].text.strip('\n')
            shipping = "none"
            price = container.find("div",{"id":"prodOther"}).find("li", {"id":"did_price1valuediv"}).p.label.b.string
            f.write(brand + "," + product.replace(",", "|") + "," + shipping + "," + price.replace(",","") + "\n")
        f.close()

        # build response
        with open("GPU_Info_Frys.csv") as myfile:
            response = HttpResponse(myfile, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=GPU_Data_Frys.csv'
            return response

    finally:
        f.close()
        uClient.close()
