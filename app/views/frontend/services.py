#Route methods here will take care of all content pages related to services

from flask import Blueprint, render_template
from ... import cache

service_pages = Blueprint("services", __name__)

@service_pages.route('/services/', methods=["GET"])
@cache.cached(timeout=40, key_prefix='our_service')
def our_service(): 
    """
        This is the main service page render method from nav bar
        Methods: GET 
    """
    return render_template("our-services.html")


@service_pages.route('/services/<string:service_name>/', methods=["GET"])
# @cache.cached(timeout=40, key_prefix='selected_service')
def selected_service(service_name):
    """
    This is common render method for all service pages
    Methods: GET 
    @param: service_name - options: best_gold, pledge_gold, sell_gold, valuate_gold
    returns: jinja page with service name as template name
    """
    return render_template("services/{}.html".format(service_name))