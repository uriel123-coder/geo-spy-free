"""
Base de datos global de lugares del mundo.
Incluye ciudades, monumentos, paisajes y regiones con sus coordenadas GPS.
"""

GLOBAL_PLACES = [
    # Europa
    {"name": "Paris, France - Eiffel Tower", "lat": 48.8584, "lon": 2.2945, "keywords": ["eiffel tower", "paris", "france", "iron lattice tower"]},
    {"name": "London, United Kingdom - Big Ben", "lat": 51.5007, "lon": -0.1246, "keywords": ["big ben", "london", "clock tower", "parliament"]},
    {"name": "Rome, Italy - Colosseum", "lat": 41.8902, "lon": 12.4922, "keywords": ["colosseum", "rome", "amphitheater", "ancient ruins"]},
    {"name": "Barcelona, Spain - Sagrada Familia", "lat": 41.4036, "lon": 2.1744, "keywords": ["sagrada familia", "barcelona", "gaudi", "cathedral"]},
    {"name": "Athens, Greece - Parthenon", "lat": 37.9715, "lon": 23.7267, "keywords": ["parthenon", "athens", "acropolis", "ancient greece"]},
    {"name": "Venice, Italy - Grand Canal", "lat": 45.4408, "lon": 12.3155, "keywords": ["venice", "canals", "gondolas", "bridges"]},
    {"name": "Amsterdam, Netherlands - Canals", "lat": 52.3676, "lon": 4.9041, "keywords": ["amsterdam", "canals", "bicycles", "dutch"]},
    {"name": "Prague, Czech Republic - Old Town", "lat": 50.0755, "lon": 14.4378, "keywords": ["prague", "old town", "castle", "gothic"]},
    {"name": "Berlin, Germany - Brandenburg Gate", "lat": 52.5163, "lon": 13.3777, "keywords": ["brandenburg gate", "berlin", "neoclassical"]},
    {"name": "Moscow, Russia - Red Square", "lat": 55.7539, "lon": 37.6208, "keywords": ["red square", "moscow", "kremlin", "st basil"]},
    
    # América del Norte
    {"name": "New York, USA - Statue of Liberty", "lat": 40.6892, "lon": -74.0445, "keywords": ["statue of liberty", "new york", "manhattan", "liberty island"]},
    {"name": "New York, USA - Times Square", "lat": 40.7580, "lon": -73.9855, "keywords": ["times square", "broadway", "neon lights", "advertisements"]},
    {"name": "San Francisco, USA - Golden Gate Bridge", "lat": 37.8199, "lon": -122.4783, "keywords": ["golden gate", "san francisco", "bridge", "orange suspension"]},
    {"name": "Los Angeles, USA - Hollywood Sign", "lat": 34.1341, "lon": -118.3215, "keywords": ["hollywood sign", "los angeles", "hills"]},
    {"name": "Las Vegas, USA - The Strip", "lat": 36.1147, "lon": -115.1728, "keywords": ["las vegas", "casinos", "desert", "neon"]},
    {"name": "Chicago, USA - Willis Tower", "lat": 41.8789, "lon": -87.6359, "keywords": ["chicago", "sears tower", "skyscraper"]},
    {"name": "Washington DC, USA - White House", "lat": 38.8977, "lon": -77.0365, "keywords": ["white house", "washington", "capitol"]},
    {"name": "Miami, USA - South Beach", "lat": 25.7907, "lon": -80.1300, "keywords": ["miami beach", "art deco", "ocean", "palm trees"]},
    {"name": "Seattle, USA - Space Needle", "lat": 47.6205, "lon": -122.3493, "keywords": ["space needle", "seattle", "observation tower"]},
    {"name": "Toronto, Canada - CN Tower", "lat": 43.6426, "lon": -79.3871, "keywords": ["cn tower", "toronto", "canada"]},
    {"name": "Vancouver, Canada - Stanley Park", "lat": 49.3017, "lon": -123.1443, "keywords": ["vancouver", "mountains", "ocean", "rainforest"]},
    {"name": "Mexico City, Mexico - Zócalo", "lat": 19.4326, "lon": -99.1332, "keywords": ["zocalo", "mexico city", "cathedral", "plaza"]},
    
    # América del Sur
    {"name": "Rio de Janeiro, Brazil - Christ the Redeemer", "lat": -22.9519, "lon": -43.2105, "keywords": ["christ redeemer", "rio", "corcovado", "statue"]},
    {"name": "Buenos Aires, Argentina - Obelisco", "lat": -34.6037, "lon": -58.3816, "keywords": ["obelisk", "buenos aires", "avenue"]},
    {"name": "Lima, Peru - Plaza de Armas", "lat": -12.0464, "lon": -77.0428, "keywords": ["lima", "colonial", "plaza"]},
    {"name": "Machu Picchu, Peru", "lat": -13.1631, "lon": -72.5450, "keywords": ["machu picchu", "inca", "ruins", "mountains"]},
    {"name": "Bogota, Colombia - Monserrate", "lat": 4.6055, "lon": -74.0565, "keywords": ["bogota", "mountains", "andes"]},
    
    # Asia
    {"name": "Tokyo, Japan - Shibuya Crossing", "lat": 35.6595, "lon": 139.7004, "keywords": ["shibuya", "tokyo", "crossing", "neon signs"]},
    {"name": "Tokyo, Japan - Mount Fuji", "lat": 35.3606, "lon": 138.7274, "keywords": ["mount fuji", "volcano", "snow peak"]},
    {"name": "Beijing, China - Forbidden City", "lat": 39.9163, "lon": 116.3972, "keywords": ["forbidden city", "beijing", "palace", "imperial"]},
    {"name": "Shanghai, China - Bund", "lat": 31.2397, "lon": 121.4912, "keywords": ["shanghai", "bund", "skyscrapers", "waterfront"]},
    {"name": "Hong Kong - Victoria Harbor", "lat": 22.2793, "lon": 114.1628, "keywords": ["hong kong", "victoria harbor", "skyline", "skyscrapers"]},
    {"name": "Bangkok, Thailand - Grand Palace", "lat": 13.7500, "lon": 100.4915, "keywords": ["bangkok", "grand palace", "temple", "golden"]},
    {"name": "Singapore - Marina Bay Sands", "lat": 1.2834, "lon": 103.8607, "keywords": ["singapore", "marina bay", "modern", "skyline"]},
    {"name": "Dubai, UAE - Burj Khalifa", "lat": 25.1972, "lon": 55.2744, "keywords": ["burj khalifa", "dubai", "tallest building", "desert"]},
    {"name": "Istanbul, Turkey - Hagia Sophia", "lat": 41.0082, "lon": 28.9784, "keywords": ["hagia sophia", "istanbul", "mosque", "dome"]},
    {"name": "Jerusalem, Israel - Western Wall", "lat": 31.7767, "lon": 35.2345, "keywords": ["western wall", "jerusalem", "ancient", "religious"]},
    {"name": "Mumbai, India - Gateway of India", "lat": 18.9220, "lon": 72.8347, "keywords": ["mumbai", "gateway", "arch", "harbor"]},
    {"name": "Agra, India - Taj Mahal", "lat": 27.1751, "lon": 78.0421, "keywords": ["taj mahal", "agra", "white marble", "mausoleum"]},
    {"name": "Seoul, South Korea - N Seoul Tower", "lat": 37.5512, "lon": 126.9882, "keywords": ["seoul tower", "korea", "namsan"]},
    
    # África
    {"name": "Cairo, Egypt - Pyramids of Giza", "lat": 29.9792, "lon": 31.1342, "keywords": ["pyramids", "giza", "egypt", "desert", "sphinx"]},
    {"name": "Cape Town, South Africa - Table Mountain", "lat": -33.9628, "lon": 18.4098, "keywords": ["table mountain", "cape town", "flat top"]},
    {"name": "Marrakech, Morocco - Medina", "lat": 31.6295, "lon": -7.9811, "keywords": ["marrakech", "medina", "market", "desert"]},
    
    # Oceanía
    {"name": "Sydney, Australia - Opera House", "lat": -33.8568, "lon": 151.2153, "keywords": ["sydney opera house", "harbor", "shells"]},
    {"name": "Melbourne, Australia - Federation Square", "lat": -37.8179, "lon": 144.9691, "keywords": ["melbourne", "modern", "australia"]},
    {"name": "Auckland, New Zealand - Sky Tower", "lat": -36.8485, "lon": 174.7633, "keywords": ["auckland", "sky tower", "new zealand"]},
    
    # Paisajes y Regiones Generales
    {"name": "Beach with palm trees - Tropical", "lat": 0.0, "lon": 0.0, "keywords": ["beach", "palm trees", "tropical", "sand", "ocean"]},
    {"name": "Mountain landscape - Alps", "lat": 46.8182, "lon": 8.2275, "keywords": ["mountains", "alps", "snow", "peaks"]},
    {"name": "Desert landscape - Sahara", "lat": 25.0, "lon": 10.0, "keywords": ["desert", "sand dunes", "arid"]},
    {"name": "Forest - Amazon Rainforest", "lat": -3.4653, "lon": -62.2159, "keywords": ["rainforest", "jungle", "dense vegetation"]},
    {"name": "Suburban neighborhood - North America", "lat": 40.0, "lon": -100.0, "keywords": ["suburban", "houses", "lawns", "residential"]},
    {"name": "Urban cityscape - Generic", "lat": 0.0, "lon": 0.0, "keywords": ["city", "skyscrapers", "urban", "buildings", "downtown"]},
]

def get_text_prompts():
    """Genera prompts textuales para CLIP."""
    prompts = []
    for place in GLOBAL_PLACES:
        # Crear descripción rica combinando nombre y keywords
        desc = f"A photo of {place['name']}, showing {', '.join(place['keywords'][:3])}"
        prompts.append({
            "text": desc,
            "location": place['name'],
            "lat": place['lat'],
            "lon": place['lon']
        })
    return prompts
