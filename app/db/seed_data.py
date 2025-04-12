from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.services.db_service import db_service

# Sample Kuriftu services data
SAMPLE_SERVICES = [
    {
        "name": "Kuriftu Spa Signature Massage",
        "description": "A 90-minute full-body massage combining traditional Ethiopian techniques with modern spa therapy, using locally-sourced essential oils.",
        "category": "spa",
        "location": "Wellness Center"
    },
    {
        "name": "Lake Tana Sunset Cruise",
        "description": "A private boat tour on Lake Tana during sunset, with champagne service and views of local wildlife and monasteries.",
        "category": "activity",
        "location": "Lake Tana"
    },
    {
        "name": "Ethiopian Coffee Ceremony",
        "description": "Experience the traditional Ethiopian coffee ceremony with freshly roasted beans and cultural insights from our staff.",
        "category": "activity",
        "location": "Cultural Center"
    },
    {
        "name": "Waterfront Fine Dining",
        "description": "Gourmet dining experience with a fusion of Ethiopian and international cuisine, set on a private deck overlooking the water.",
        "category": "restaurant",
        "location": "Main Restaurant"
    },
    {
        "name": "Couples' Retreat Package",
        "description": "A romantic package including a private dinner, couples massage, and exclusive use of a lakeside hot tub under the stars.",
        "category": "spa",
        "location": "Wellness Center"
    },
    {
        "name": "Kids Adventure Club",
        "description": "Supervised activities for children including nature walks, traditional games, and cultural crafts.",
        "category": "activity",
        "location": "Kids Club"
    },
    {
        "name": "Sunrise Yoga Session",
        "description": "Morning yoga and meditation session on a private deck overlooking the lake, suitable for all experience levels.",
        "category": "activity",
        "location": "Yoga Pavilion"
    },
    {
        "name": "Local Market Excursion",
        "description": "Guided tour to nearby markets with opportunities to purchase authentic crafts and meet local artisans.",
        "category": "activity",
        "location": "Off-site"
    },
    {
        "name": "Traditional Music Night",
        "description": "Evening entertainment featuring local musicians performing traditional Ethiopian music with dinner service available.",
        "category": "event",
        "location": "Cultural Center"
    },
    {
        "name": "Lakeside BBQ Feast",
        "description": "Family-style barbecue featuring fresh seafood and meats with Ethiopian spices, set up on the beach.",
        "category": "restaurant",
        "location": "Beach Area"
    },
    {
        "name": "Detox Wellness Package",
        "description": "A full-day wellness experience including detox treatments, healthy meals, and guided meditation sessions.",
        "category": "spa",
        "location": "Wellness Center"
    },
    {
        "name": "Fishing Expedition",
        "description": "Guided fishing trip on Lake Tana with equipment provided and option to have your catch prepared by our chefs.",
        "category": "activity",
        "location": "Lake Tana"
    }
]

def seed_data():
    db = SessionLocal()
    try:
        # Add sample Kuriftu services
        for service in SAMPLE_SERVICES:
            db_service.add_kuriftu_service(
                db,
                service["name"],
                service["description"],
                service["category"],
                service["location"]
            )
        
        print("Database seeded with sample Kuriftu services")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()