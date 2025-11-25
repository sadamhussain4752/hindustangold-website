#Route methods here will take care of all content pages related to blogs

from flask import Blueprint, render_template
from ... import cache

blog_pages = Blueprint("blogs", __name__)

@blog_pages.route('/blog/', methods=["GET"])
def blogs(): 
    return render_template("blog.html")

@blog_pages.route('/more-blogs/', methods=["GET"])
def more_blogs(): 
    return render_template("more-blogs.html")


@blog_pages.route('/blog/<string:blog_name>/', methods=["GET"])
def selected_blog(blog_name):
    return render_template("/blog/{}.html".format(blog_name))