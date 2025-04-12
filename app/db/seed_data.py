from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.services.db_service import db_service
# Comprehensive Kuriftu services data
KURIFTU_SERVICES = [
    # Spa & Wellness
    {
        "name": "Kuriftu Signature Massage",
        "description": "A 90-minute full-body massage combining traditional Ethiopian techniques with modern spa therapy, using locally-sourced essential oils and hot stones.",
        "category": "spa",
        "location": "Kuriftu Bishoftu"
    },
    {
        "name": "Couples Harmony Retreat",
        "description": "Indulge in a side-by-side massage experience in our private couples suite, followed by a romantic bath ritual and champagne service.",
        "category": "spa",
        "location": "Kuriftu Bahir Dar"
    },
    {
        "name": "Detox Body Wrap",
        "description": "A purifying treatment using local Ethiopian clay and coffee grounds to draw out impurities, followed by a hydrating body butter application.",
        "category": "spa",
        "location": "Kuriftu Bishoftu"
    },
    {
        "name": "Sunrise Lakeside Yoga",
        "description": "Begin your day with an invigorating yoga session on our private deck overlooking Lake Tana, guided by our experienced instructor.",
        "category": "wellness",
        "location": "Kuriftu Bahir Dar"
    },
    
    # Dining Experiences
    {
        "name": "Waterfront Fine Dining",
        "description": "Experience gourmet cuisine at our signature restaurant with panoramic views of the lake. Our menu features Ethiopian-inspired international dishes using locally-sourced ingredients.",
        "category": "dining",
        "location": "Kuriftu Bahir Dar"
    },
    {
        "name": "Private Island Dinner",
        "description": "Exclusive dining experience on our private island with a personalized menu prepared by our executive chef, complete with butler service and ambient lighting.",
        "category": "dining",
        "location": "Kuriftu Bahir Dar"
    },
    {
        "name": "Traditional Coffee Ceremony",
        "description": "Immerse yourself in Ethiopia's rich coffee culture with our authentic coffee ceremony, where beans are roasted, ground and brewed before you, accompanied by traditional snacks.",
        "category": "dining",
        "location": "All Locations"
    },
    {
        "name": "Sunset Cocktail Experience",
        "description": "Enjoy handcrafted cocktails featuring local ingredients while watching the sun set over the crater lake, with light appetizers and live ambient music.",
        "category": "dining",
        "location": "Kuriftu Bishoftu"
    },
    
    # Water Activities
    {
        "name": "Lake Tana Sunset Cruise",
        "description": "Explore the historic Lake Tana on our private boat, visiting ancient monasteries and enjoying the diverse birdlife while sipping on refreshments as the sun sets.",
        "category": "water",
        "location": "Kuriftu Bahir Dar"
    },
    {
        "name": "Paddleboarding Adventure",
        "description": "Discover the tranquility of paddleboarding on our crater lake with equipment and instruction provided for all skill levels.",
        "category": "water",
        "location": "Kuriftu Bishoftu"
    },
    {
        "name": "Fishing Expedition",
        "description": "Join our expert guides for a fishing trip on Lake Tana, with the option to have our chefs prepare your catch for dinner.",
        "category": "water",
        "location": "Kuriftu Bahir Dar"
    },
    {
        "name": "Water Park Family Package",
        "description": "Full-day access to our water park featuring slides, pools, and splash zones for all ages, with lunch included at our poolside restaurant.",
        "category": "water",
        "location": "Kuriftu Bishoftu"
    },
    
    # Cultural Experiences
    {
        "name": "Blue Nile Falls Excursion",
        "description": "Full-day guided tour to the magnificent Blue Nile Falls (Tis Abay), including transportation, picnic lunch, and insights into local history and ecology.",
        "category": "culture",
        "location": "Kuriftu Bahir Dar"
    },
    {
        "name": "Ethiopian Art Workshop",
        "description": "Learn traditional Ethiopian painting techniques from local artists in our Art Village, creating your own piece to take home as a souvenir.",
        "category": "culture",
        "location": "Kuriftu Bishoftu"
    },
    {
        "name": "Cultural Dance Performance",
        "description": "Evening entertainment featuring dancers from different Ethiopian regions performing traditional dances in authentic costumes, with dinner service available.",
        "category": "culture",
        "location": "All Locations"
    },
    {
        "name": "Local Market Tour",
        "description": "Guided excursion to nearby markets where you can interact with local artisans, purchase authentic crafts, and experience daily Ethiopian life.",
        "category": "culture",
        "location": "All Locations"
    },
    
    # Accommodation
    {
        "name": "Lakefront Villa",
        "description": "Luxurious private villa with direct lake access, featuring a master bedroom, living area, private plunge pool, and dedicated butler service.",
        "category": "accommodation",
        "location": "Kuriftu Bahir Dar"
    },
    {
        "name": "Honeymoon Suite",
        "description": "Romantic suite with panoramic lake views, featuring a four-poster bed, private balcony, couples' spa bath, and complimentary champagne service.",
        "category": "accommodation",
        "location": "All Locations"
    },
    {
        "name": "Family Cottage",
        "description": "Spacious two-bedroom cottage ideal for families, with a living area, private garden, and easy access to all resort facilities including the kids' club.",
        "category": "accommodation",
        "location": "Kuriftu Bishoftu"
    },
    {
        "name": "Presidential Suite",
        "description": "Our most exclusive accommodation featuring multiple bedrooms, a private dining area, panoramic views, and personalized concierge service.",
        "category": "accommodation",
        "location": "Kuriftu Bahir Dar"
    },
    
    # Adventure & Recreation
    {
        "name": "Horseback Safari",
        "description": "Explore the countryside surrounding our Bishoftu resort on horseback, suitable for beginners and experienced riders alike.",
        "category": "adventure",
        "location": "Kuriftu Bishoftu"
    },
    {
        "name": "Mountain Biking Expedition",
        "description": "Guided mountain biking tours through scenic landscapes with various difficulty levels and equipment provided.",
        "category": "adventure",
        "location": "Kuriftu Bishoftu"
    },
    {
        "name": "Bird Watching Tour",
        "description": "Early morning guided bird watching experience around Lake Tana, home to numerous endemic and migratory bird species, with binoculars and refreshments provided.",
        "category": "adventure",
        "location": "Kuriftu Bahir Dar"
    },
    {
        "name": "Tennis Coaching",
        "description": "Private tennis lessons on our professional-grade courts with equipment provided and coaching available for all skill levels.",
        "category": "recreation",
        "location": "Kuriftu Bishoftu"
    }
]

def seed_data():
    db = SessionLocal()
    try:
        # Add Kuriftu services
        for service in KURIFTU_SERVICES:
            db_service.add_kuriftu_service(
                db,
                service["name"],
                service["description"],
                service["category"],
                service["location"]
            )
        
        print("Database seeded with comprehensive Kuriftu services")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()