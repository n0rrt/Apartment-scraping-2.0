from City import City
from ScrapingMethods import *
from DBMethods import write, get_old_db


Philadelphia = City('Philadelphia%2C+PA', 'rx2721')
Tempe = City('Tempe%2C+AZ', 'zu85280')
Charlotte = City('Charlotte%2C+NC', 'rx2465')
Kirkland = City('Kirkland%2C+WA', 'zu98033')
Atlanta = City('Atlanta%2C+GA', 'rx394')


links = get_links(Philadelphia) + get_links(Tempe) + get_links(Charlotte) + get_links(Kirkland) + get_links(Atlanta)
apts = scrape_apts(links)
apartments, properties = prettify(apts)
old = get_old_db()
for apt in apartments:
    write(apt)
for prop in properties:
    write(prop)