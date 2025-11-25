from app import app

from app.views import (
    home,
    auth,
    gold_prices,
    customers,
    state,
    city,
    branch,
    api,
    seo,
    careers,
    service_pages,
    blog_pages,
    branch_pages,
    career_pages
)



app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(gold_prices)
app.register_blueprint(customers)
app.register_blueprint(state)
app.register_blueprint(city)
app.register_blueprint(branch)
app.register_blueprint(api)
app.register_blueprint(seo)
app.register_blueprint(careers)
app.register_blueprint(service_pages)
app.register_blueprint(blog_pages)
app.register_blueprint(branch_pages)
app.register_blueprint(career_pages)

if __name__ == "__main__":
    app.run()
