from utils.CurrencyStripper import convert_currency


class Listing:
    def __init__(self):
        self.url = ""
        self.photo_list = []  # photo URLs
        self.title = ""
        self.current_bid = 0.0
        self.shipping_cost = 0.0
        self.user_name = ""
        self.user_rating = ''

    def get_photo_list_comma_separated(self):
        comma_separated_str = ''
        for iterator in self.photo_list:
            comma_separated_str = comma_separated_str + iterator + ','
        return comma_separated_str[:-1]  # remove last comma

    def set_shipping_cost(self, shipping_cost_raw):
        if "FREE" in shipping_cost_raw or 'KOSTENLOS' in shipping_cost_raw:
            self.shipping_cost = 0
        else:
            self.shipping_cost = convert_currency(shipping_cost_raw)

    def set_current_bid(self, current_bid_raw):
        self.current_bid = convert_currency(current_bid_raw)

    def set_title(self, title):
        self.title = title.lower()
