# app/data/seed.py
# Dummy data — replace with DB queries in production

from typing import List, Dict, Any

CATERERS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "name": "Grand Feast Catering",
        "emoji": "🍛",
        "rating": 4.9,
        "reviews": 120,
        "cuisines": ["South Indian", "North Indian", "Telugu"],
        "tags": ["Live Dosa", "Veg Options", "Elder-friendly", "Large Events"],
        "price_min": 16,
        "price_max": 22,
        "price_display": "$16–$22",
        "price_note": "per plate, vegetarian menu",
        "min_guests": 50,
        "max_guests": 1000,
        "location": "San Jose, CA",
        "phone": "+1 (408) 555-0100",
        "email": "info@grandfeast.com",
        "verified": True,
        "description": (
            "Known for authentic Telugu wedding feasts with live dosa and chaat counters. "
            "Specializes in large events up to 1,000 guests with full-service setup and "
            "experienced, uniformed staff."
        ),
        "specialties": ["Weddings", "Engagements", "Religious Events"],
        "menu": [
            "Live Dosa Counter", "Pulao", "Sambar Rice",
            "Paneer Tikka", "Gulab Jamun", "Live Chaat Station",
            "Rasam", "Payasam",
        ],
        "photos_count": 24,
        "match_keywords": ["telugu", "south indian", "vegetarian", "veg", "dosa",
                           "live counter", "wedding", "engagement", "elder"],
    },
    {
        "id": 2,
        "name": "Sri Sai Catering",
        "emoji": "🥘",
        "rating": 4.8,
        "reviews": 98,
        "cuisines": ["Telugu", "South Indian"],
        "tags": ["Dosa", "Chaat", "Veg", "Live Counters"],
        "price_min": 15,
        "price_max": 20,
        "price_display": "$15–$20",
        "price_note": "per plate, vegetarian menu",
        "min_guests": 30,
        "max_guests": 500,
        "location": "San Jose, CA",
        "phone": "+1 (408) 555-0200",
        "email": "hello@srisai.com",
        "verified": True,
        "description": (
            "Beloved Telugu caterer with a focus on traditional recipes and modern presentation. "
            "Excellent reviews for engagement and wedding ceremonies throughout the Bay Area."
        ),
        "specialties": ["Engagements", "Weddings", "Birthdays"],
        "menu": ["Pesarattu", "Pulihora", "Vada Sambar", "Payasam", "Live Chaat", "Biryani"],
        "photos_count": 18,
        "match_keywords": ["telugu", "south indian", "vegetarian", "veg", "dosa",
                           "chaat", "engagement", "wedding", "birthday"],
    },
    {
        "id": 3,
        "name": "Flavors of India",
        "emoji": "🌶️",
        "rating": 4.7,
        "reviews": 74,
        "cuisines": ["North Indian", "Chaat"],
        "tags": ["Veg", "North Indian", "Live Counters", "Large Events"],
        "price_min": 14,
        "price_max": 18,
        "price_display": "$14–$18",
        "price_note": "per plate, vegetarian menu",
        "min_guests": 50,
        "max_guests": 800,
        "location": "Sunnyvale, CA",
        "phone": "+1 (408) 555-0300",
        "email": "contact@flavorsofindia.com",
        "verified": True,
        "description": (
            "Specializes in North Indian vegetarian menus with popular live chaat and pani puri "
            "stations. Great for corporate events and large community gatherings."
        ),
        "specialties": ["Corporate Events", "Community Events", "Birthdays"],
        "menu": ["Pani Puri Counter", "Biryani", "Dal Makhani", "Paneer Butter Masala", "Kulfi"],
        "photos_count": 12,
        "match_keywords": ["north indian", "vegetarian", "veg", "chaat", "pani puri",
                           "corporate", "community", "birthday", "large event"],
    },
    {
        "id": 4,
        "name": "Royal Bites",
        "emoji": "🍱",
        "rating": 4.6,
        "reviews": 52,
        "cuisines": ["Multi Cuisine"],
        "tags": ["Multi Cuisine", "Non-Veg", "Premium"],
        "price_min": 18,
        "price_max": 24,
        "price_display": "$18–$24",
        "price_note": "per plate, includes non-veg options",
        "min_guests": 25,
        "max_guests": 400,
        "location": "Santa Clara, CA",
        "phone": "+1 (408) 555-0400",
        "email": "bookings@royalbites.com",
        "verified": False,
        "description": (
            "Premium multi-cuisine caterer offering both vegetarian and non-vegetarian menus. "
            "Perfect for corporate events and upscale celebrations with professional table service."
        ),
        "specialties": ["Corporate Events", "Upscale Parties", "Weddings"],
        "menu": ["Tandoori Chicken", "Mutton Biryani", "Veg Biryani", "Salad Bar", "Dessert Counter"],
        "photos_count": 9,
        "match_keywords": ["non-veg", "nonveg", "chicken", "mutton", "multi cuisine",
                           "premium", "corporate", "upscale", "wedding"],
    },
    {
        "id": 5,
        "name": "Spice Garden",
        "emoji": "🌱",
        "rating": 4.5,
        "reviews": 41,
        "cuisines": ["South Indian", "Vegan"],
        "tags": ["Vegan", "Gluten-Free", "South Indian", "Health-Focused"],
        "price_min": 18,
        "price_max": 26,
        "price_display": "$18–$26",
        "price_note": "per plate, fully plant-based",
        "min_guests": 20,
        "max_guests": 300,
        "location": "Cupertino, CA",
        "phone": "+1 (408) 555-0500",
        "email": "hello@spicegarden.com",
        "verified": True,
        "description": (
            "Bay Area's premier fully plant-based South Indian caterer. Specializes in "
            "vegan and gluten-free menus without compromising on authentic flavor."
        ),
        "specialties": ["Health Events", "Corporate Lunches", "Small Gatherings"],
        "menu": ["Millet Dosa", "Avocado Chutney", "Quinoa Biryani", "Coconut Payasam", "Raw Salads"],
        "photos_count": 7,
        "match_keywords": ["vegan", "plant-based", "gluten-free", "health", "south indian",
                           "small event", "corporate", "cupertino"],
    },
    {
        "id": 6,
        "name": "Dawat Express",
        "emoji": "🫕",
        "rating": 4.4,
        "reviews": 33,
        "cuisines": ["Mughlai", "North Indian", "Non-Veg"],
        "tags": ["Non-Veg", "Mughlai", "Biryani", "Premium"],
        "price_min": 20,
        "price_max": 30,
        "price_display": "$20–$30",
        "price_note": "per plate, mixed menu",
        "min_guests": 40,
        "max_guests": 350,
        "location": "Fremont, CA",
        "phone": "+1 (510) 555-0600",
        "email": "info@dawatexpress.com",
        "verified": True,
        "description": (
            "Authentic Mughlai and North Indian non-veg specialist. Famous for slow-cooked "
            "dum biryani and seekh kebabs. Perfect for large family celebrations."
        ),
        "specialties": ["Weddings", "Eid Celebrations", "Family Gatherings"],
        "menu": ["Dum Biryani", "Seekh Kebab", "Nihari", "Shami Kebab", "Phirni"],
        "photos_count": 11,
        "match_keywords": ["mughlai", "non-veg", "biryani", "kebab", "north indian",
                           "wedding", "eid", "family", "fremont"],
    },
]

INQUIRIES: List[Dict[str, Any]] = []  # In-memory store — replace with DB in prod

EVENT_TYPES = [
    {"label": "Wedding",        "icon": "💍"},
    {"label": "Engagement",     "icon": "💫"},
    {"label": "Birthday",       "icon": "🎂"},
    {"label": "House Party",    "icon": "🏠"},
    {"label": "Corporate",      "icon": "💼"},
    {"label": "Religious Event","icon": "🙏"},
]
