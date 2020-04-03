import requests
from bs4 import BeautifulSoup
from ApartmentClasses import ApartmentProperty, Apartment

def get_links(city):
        url = 'http://www.classifiedads.com/search.php?'
        links = []
        for x in range(1, 10):
            r = requests.get(url, params={
                             'cid': '299', 'lid': city.get_id(), 'lname': city.get_name(), 'page': x})
            content = r.text
            soup = BeautifulSoup(content, 'html.parser')
            for div in soup.findAll('div', class_='resultitem'):
                link = div.find('a')['href']
                if link not in links:
                    links.append(link)
                    print('New link from', str(city), link)
        return links


def scrape_apts(links):
    apts = []
    for link in links:
        r = requests.get('http:'+link)
        content = r.text
        soup = BeautifulSoup(content, 'html.parser')
        property = {}
        for first in soup.findAll('span', class_='first'):
            try:
                first_content = str(first.encode_contents())
                next = str(first.next_sibling.encode_contents())
                property[first_content] = next
            except:
                pass
        print('new raw', str(property))
        apts.append(property)
    return apts


def prettify(apts):
    ad_string = "b'Ad number:'"
    count = 0
    apartments = []
    properties = []
    for apt in apts:
        ad_num = apt.get(ad_string).split("'")[1]
        apartment = Apartment(ad_num, 'status')
        print(apartment)
        apartments.append(apartment)
        print('New apartment:', apartment)
        for key in apt.keys():
            if key != ad_string:
                type = key.split("'")[1]
                value = apt.get(key).split("'")[1]
                if type == 'Price:':
                    property = ApartmentProperty(count, ad_num, type, value.split(">")[1].split("<")[0])
                elif type == 'Square\\xc2\\xa0ft:':
                    property = ApartmentProperty(count, ad_num, type.split("\\")[0] + " " + type.split("0")[1], value)
                else:
                    property = ApartmentProperty(count, ad_num, type, value)
                properties.append(property)
                print('New Property:', property)
                count += 1

    return (apartments, properties)
