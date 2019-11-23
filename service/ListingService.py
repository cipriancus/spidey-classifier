from model.Listing import Listing
from service.PullingService import PullingService
from classification.ClassificationService import ClassificationService
from service.FilterService import FilterService
import csv

pulled_listings_csv = "./pulled-listings/listings.csv"


def unpack_listings_in_request(request):
    json_list = request.get_json()
    listings_list = set([])
    for iterator in json_list:
        listing = Listing()
        listing.url = iterator['listingUrl']
        listing.set_title(iterator['title'])
        listings_list.add(listing)
    return listings_list


def strip_classification_information(listings):
    listings_dto_list = []
    for iterator in listings:
        listings_dto_list.append({'listingUrl': iterator.url})
    return listings_dto_list


def save_link(listing):
    shortcut = open("./pulled-listings/" + ''.join(e for e in listing.title if e.isalnum() or e == ' ') + ".url", 'w+')
    shortcut.write('[InternetShortcut]\n')
    shortcut.write('URL=%s' % listing.url)
    shortcut.close()


def save_pulled_listings(listings):
    with open(pulled_listings_csv, mode='a', encoding="utf-8", newline='') as listings_csv:
        fieldnames = ['url', 'photo_list', 'title', 'current_bid', 'shipping_cost', 'user_name', 'user_rating']
        writer = csv.DictWriter(listings_csv, fieldnames=fieldnames)
        # writer.writeheader()
        for iterator in listings:
            writer.writerow({'url': iterator.url, 'photo_list': iterator.get_photo_list_comma_separated(),
                             'title': iterator.title, 'current_bid': iterator.current_bid,
                             'shipping_cost': iterator.shipping_cost,
                             'user_name': iterator.user_name, 'user_rating': iterator.user_rating})
            save_link(iterator)


class ListingService:
    def __init__(self):
        self.pulling_service = PullingService()
        self.classification_service = ClassificationService()
        self.filter_service = FilterService(pulled_listings_csv)

    def get_worthy_listings(self, request):
        listings = unpack_listings_in_request(request)
        listings = self.filter_service.filter_duplicates(listings)
        listings = self.filter_service.pre_filter_title(listings)
        listings = self.pulling_service.pull_listing_data(listings)
        listings = self.filter_service.filter_listings(listings)
        self.filter_service.update_existing_urls(listings)
        save_pulled_listings(listings)
        return strip_classification_information(self.classification_service.classify_listings(listings))
