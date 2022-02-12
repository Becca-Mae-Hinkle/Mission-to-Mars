from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/marsdb")

# Create route that renders index.html template and finds data from mongo
@app.route('/')
def home(): 

    # Find data
    mars = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars=mars)

 # Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    mars = mongo.db.mars

    # Run the scrape function
    
    mars_data = scraping.scrape_all()

    # Update the Mongo database using update and upsert=True
    mars.update_one({}, {"$set":mars_data}, upsert=True)

    # Redirect back to home page
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
    