import requests
from lxml import html


def pull_data_for_listing(listing):
    url = listing.url

    page = requests.get(url)

    tree = html.fromstring(page.content)

    try:
        title_element = tree.get_element_by_id('itemTitle')
        listing.set_title(list(title_element)[0].tail)
    except:
        print("Title error " + listing.url)

    try:
        # TODO: add mechanism for buy it now stripping
        current_bid_element = tree.get_element_by_id('prcIsum_bidPrice')
        listing.set_current_bid(current_bid_element.text)
    except:
        print("Bid price error " + listing.url)

    try:
        shipping_cost_element = tree.get_element_by_id('fshippingCost')
        listing.set_shipping_cost(list(shipping_cost_element)[0].text)
    except:
        print("Shipping price error " + listing.url)

    try:
        user_name_element = tree.find_class('mbg-nw')
        listing.user_name = user_name_element[0].text.lower()
    except:
        print("User name error " + listing.url)

    try:
        user_rating_element = tree.find_class('mbg-l')
        listing.user_rating = list(user_rating_element[0])[0].text
    except:
        print("User rating error " + listing.url)

    try:
        photo_slider_element = list(tree.get_element_by_id('vi_main_img_fs')[0])
        for iterator in photo_slider_element:
            photo_url = list(list(iterator.find_class('tdThumb')[0])[0])[0].get('src').replace('s-l64.jpg',
                                                                                               's-l1600.jpg')
            listing.photo_list.append(photo_url)

    except:
        print("Listing has only one photo " + listing.url)

    return listing


class PullingService:

    def pull_listing_data(self, listings):
        pulled_listings = set([])

        for listing in listings:
            pulled_listings.add(pull_data_for_listing(listing))

        return pulled_listings
