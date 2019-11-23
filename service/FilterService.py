import csv

excluded_names_file = './filters/excluded-terms.txt'


def read_excluded_names():
    excluded_names_list = set([])
    with open(excluded_names_file) as file:
        for row in file:
            excluded_names_list.add(row.replace('\n', '').lower())
    return excluded_names_list


class FilterService:
    def __init__(self, pulled_listings_csv):
        self.pulled_listings_csv = pulled_listings_csv
        self.excluded_names_list = read_excluded_names()
        self.existing_urls = self.read_existing_urls()

    def read_existing_urls(self):
        existing_urls = set([])
        with open(self.pulled_listings_csv, encoding="utf-8") as listings_csv:
            csv_reader = csv.reader(listings_csv, delimiter=',')
            for row in csv_reader:
                existing_urls.add(row[0])
        return existing_urls

    def filter_listings(self, listings):
        filtered_listings = set([])
        for iterator in listings:
            if len(iterator.url) == 0:
                continue
            if len(iterator.photo_list) == 0:
                continue
            if len(iterator.title) == 0 or self.title_contains_excluded_names(iterator.title):
                continue
            if iterator.current_bid > 150:
                continue
            if iterator.shipping_cost > 25:
                continue
            if int(iterator.user_rating) > 300:
                continue
            filtered_listings.add(iterator)
        return filtered_listings

    def filter_duplicates(self, listings):
        filtered_listings = set([])

        for iterator in listings:
            if iterator.url not in self.existing_urls:
                filtered_listings.add(iterator)
        return filtered_listings

    def pre_filter_title(self, listings):
        filtered_listings = set([])
        for iterator in listings:
            if len(iterator.title) == 0 or self.title_contains_excluded_names(iterator.title):
                continue
            filtered_listings.add(iterator)
        return filtered_listings

    def title_contains_excluded_names(self, title):
        for iterator in title.split():
            if iterator in self.excluded_names_list:
                return True
        return False

    def update_existing_urls(self, listings):
        for iterator in listings:
            self.existing_urls.add(iterator.title)
