from flask import Flask, request, jsonify
from service.ListingService import ListingService

app = Flask(__name__)

listing_service = ListingService()


@app.route('/classify', methods=['POST'])
def classify():
    worthy_listings = listing_service.get_worthy_listings(request)
    return jsonify(worthy_listings)


if __name__ == '__main__':
    app.run()
