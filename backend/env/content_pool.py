"""
content_pool.py

Synthetic content dataset for SafeFeed simulation.
72 posts across healthy, neutral, and risk-cluster categories.
"""

CONTENT_POOL = [
    # --- STUDY (healthy) ---
    {"id": 1,  "title": "5 Quick Study Tips", "category": "study", "engagement_score": 7.2, "risk_score": 0.5, "tags": ["study", "education", "focus"]},
    {"id": 2,  "title": "How to Use the Pomodoro Technique", "category": "study", "engagement_score": 6.8, "risk_score": 0.4, "tags": ["study", "productivity", "focus"]},
    {"id": 3,  "title": "Best Note-Taking Methods for Students", "category": "study", "engagement_score": 6.5, "risk_score": 0.3, "tags": ["study", "notes", "learning"]},
    {"id": 4,  "title": "How to Ace Your Next Exam", "category": "study", "engagement_score": 7.0, "risk_score": 0.5, "tags": ["study", "exam", "education"]},
    {"id": 5,  "title": "Mindful Learning: Study With Intention", "category": "study", "engagement_score": 5.9, "risk_score": 0.3, "tags": ["study", "mindfulness", "learning"]},
    {"id": 6,  "title": "Top Apps for Students in 2024", "category": "study", "engagement_score": 7.5, "risk_score": 0.4, "tags": ["study", "apps", "tech"]},

    # --- PETS (healthy) ---
    {"id": 7,  "title": "Adorable Puppy Does Daily Tricks", "category": "pets", "engagement_score": 8.9, "risk_score": 0.2, "tags": ["pets", "dogs", "cute"]},
    {"id": 8,  "title": "Cat Knocks Over Everything (Compilation)", "category": "pets", "engagement_score": 9.1, "risk_score": 0.1, "tags": ["pets", "cats", "funny"]},
    {"id": 9,  "title": "Rabbit Learns to Jump Over Tiny Fence", "category": "pets", "engagement_score": 7.8, "risk_score": 0.2, "tags": ["pets", "rabbit", "cute"]},
    {"id": 10, "title": "What Your Dog's Body Language Means", "category": "pets", "engagement_score": 7.3, "risk_score": 0.3, "tags": ["pets", "dogs", "education"]},
    {"id": 11, "title": "Parrot Sings Happy Birthday Song", "category": "pets", "engagement_score": 8.6, "risk_score": 0.1, "tags": ["pets", "birds", "funny"]},
    {"id": 12, "title": "Kitten Meets Puppy for the First Time", "category": "pets", "engagement_score": 9.3, "risk_score": 0.1, "tags": ["pets", "cute", "heartwarming"]},

    # --- COMEDY (healthy) ---
    {"id": 13, "title": "Office Prank Goes Hilariously Wrong", "category": "comedy", "engagement_score": 8.8, "risk_score": 0.4, "tags": ["comedy", "funny", "prank"]},
    {"id": 14, "title": "Dad Jokes That Actually Made Us Laugh", "category": "comedy", "engagement_score": 7.9, "risk_score": 0.2, "tags": ["comedy", "jokes", "family"]},
    {"id": 15, "title": "Autocorrect Fail Compilation 2024", "category": "comedy", "engagement_score": 8.5, "risk_score": 0.3, "tags": ["comedy", "texting", "funny"]},
    {"id": 16, "title": "Comedian Does Perfect Impressions", "category": "comedy", "engagement_score": 8.2, "risk_score": 0.3, "tags": ["comedy", "impressions", "performance"]},
    {"id": 17, "title": "Grocery Store Mishap Goes Viral", "category": "comedy", "engagement_score": 7.7, "risk_score": 0.3, "tags": ["comedy", "viral", "funny"]},
    {"id": 18, "title": "Kid Says the Darndest Things", "category": "comedy", "engagement_score": 8.1, "risk_score": 0.1, "tags": ["comedy", "kids", "cute"]},

    # --- SPORTS (healthy) ---
    {"id": 19, "title": "Top 10 Basketball Dunks of the Year", "category": "sports", "engagement_score": 8.7, "risk_score": 0.3, "tags": ["sports", "basketball", "highlights"]},
    {"id": 20, "title": "How to Improve Your Tennis Serve", "category": "sports", "engagement_score": 6.9, "risk_score": 0.2, "tags": ["sports", "tennis", "tutorial"]},
    {"id": 21, "title": "Underdog Team Wins Championship", "category": "sports", "engagement_score": 8.4, "risk_score": 0.2, "tags": ["sports", "inspiration", "teamwork"]},
    {"id": 22, "title": "Morning Run Routines From Pro Athletes", "category": "sports", "engagement_score": 7.1, "risk_score": 0.2, "tags": ["sports", "running", "routine"]},
    {"id": 23, "title": "Swimming Tips for Beginners", "category": "sports", "engagement_score": 6.7, "risk_score": 0.3, "tags": ["sports", "swimming", "tutorial"]},
    {"id": 24, "title": "Yoga Stretches for Athletes", "category": "sports", "engagement_score": 7.0, "risk_score": 0.2, "tags": ["sports", "yoga", "recovery"]},

    # --- ART (healthy) ---
    {"id": 25, "title": "Speed Painting a Landscape in Watercolor", "category": "art", "engagement_score": 7.6, "risk_score": 0.2, "tags": ["art", "painting", "creative"]},
    {"id": 26, "title": "How to Draw Portraits for Beginners", "category": "art", "engagement_score": 7.2, "risk_score": 0.2, "tags": ["art", "drawing", "tutorial"]},
    {"id": 27, "title": "Street Art From Around the World", "category": "art", "engagement_score": 8.0, "risk_score": 0.2, "tags": ["art", "street art", "culture"]},
    {"id": 28, "title": "Satisfying Sand Art Compilation", "category": "art", "engagement_score": 8.3, "risk_score": 0.1, "tags": ["art", "sand", "satisfying"]},
    {"id": 29, "title": "Digital Art Timelapse: Fantasy Character", "category": "art", "engagement_score": 7.9, "risk_score": 0.2, "tags": ["art", "digital", "fantasy"]},
    {"id": 30, "title": "Pottery Making: From Clay to Cup", "category": "art", "engagement_score": 7.5, "risk_score": 0.1, "tags": ["art", "pottery", "satisfying"]},

    # --- PRODUCTIVITY (healthy) ---
    {"id": 31, "title": "Build a Morning Routine That Sticks", "category": "productivity", "engagement_score": 7.4, "risk_score": 0.3, "tags": ["productivity", "routine", "habits"]},
    {"id": 32, "title": "How to Stop Procrastinating for Good", "category": "productivity", "engagement_score": 7.8, "risk_score": 0.4, "tags": ["productivity", "procrastination", "focus"]},
    {"id": 33, "title": "Deep Work: The Secret to Peak Performance", "category": "productivity", "engagement_score": 7.1, "risk_score": 0.3, "tags": ["productivity", "focus", "work"]},
    {"id": 34, "title": "Best Free Tools for Staying Organized", "category": "productivity", "engagement_score": 7.3, "risk_score": 0.2, "tags": ["productivity", "tools", "organization"]},
    {"id": 35, "title": "Journal Prompts to Boost Clarity", "category": "productivity", "engagement_score": 6.8, "risk_score": 0.3, "tags": ["productivity", "journaling", "wellbeing"]},
    {"id": 36, "title": "How to Set Goals You'll Actually Keep", "category": "productivity", "engagement_score": 7.2, "risk_score": 0.3, "tags": ["productivity", "goals", "planning"]},

    # --- FASHION (high-engagement, okay) ---
    {"id": 37, "title": "outfit of the day inspo (casual)", "category": "fashion", "engagement_score": 8.6, "risk_score": 2.5, "tags": ["fashion", "ootd", "casual"]},
    {"id": 38, "title": "Spring Wardrobe Essentials 2024", "category": "fashion", "engagement_score": 8.2, "risk_score": 2.0, "tags": ["fashion", "spring", "style"]},
    {"id": 39, "title": "Thrift Flip: Transforming Old Clothes", "category": "fashion", "engagement_score": 8.4, "risk_score": 1.5, "tags": ["fashion", "thrift", "diy"]},
    {"id": 40, "title": "Color Matching 101: Dress Smarter", "category": "fashion", "engagement_score": 7.8, "risk_score": 1.8, "tags": ["fashion", "style", "color"]},
    {"id": 41, "title": "Styling Tips for Different Body Types", "category": "fashion", "engagement_score": 7.5, "risk_score": 3.0, "tags": ["fashion", "style", "body"]},
    {"id": 42, "title": "Affordable Fashion Haul This Week", "category": "fashion", "engagement_score": 8.0, "risk_score": 2.2, "tags": ["fashion", "haul", "affordable"]},

    # --- FITNESS (high-engagement, okay) ---
    {"id": 43, "title": "30-Minute Full Body Workout (No Gym)", "category": "fitness", "engagement_score": 8.8, "risk_score": 1.5, "tags": ["fitness", "workout", "home"]},
    {"id": 44, "title": "What I Eat in a Day (Balanced Diet)", "category": "fitness", "engagement_score": 8.3, "risk_score": 2.0, "tags": ["fitness", "diet", "health"]},
    {"id": 45, "title": "How to Build a Consistent Gym Habit", "category": "fitness", "engagement_score": 7.9, "risk_score": 1.2, "tags": ["fitness", "gym", "habits"]},
    {"id": 46, "title": "Best Pre-Workout Meals", "category": "fitness", "engagement_score": 7.5, "risk_score": 1.4, "tags": ["fitness", "nutrition", "performance"]},
    {"id": 47, "title": "Abs Workout for Beginners", "category": "fitness", "engagement_score": 8.5, "risk_score": 1.8, "tags": ["fitness", "abs", "beginner"]},
    {"id": 48, "title": "Stretching Routine for Flexibility", "category": "fitness", "engagement_score": 7.2, "risk_score": 1.0, "tags": ["fitness", "stretching", "flexibility"]},

    # --- TRENDS (high-engagement, okay) ---
    {"id": 49, "title": "Viral Dance Challenge Everyone Is Doing", "category": "trends", "engagement_score": 9.2, "risk_score": 1.8, "tags": ["trends", "dance", "viral"]},
    {"id": 50, "title": "This Week's Meme Roundup", "category": "trends", "engagement_score": 8.9, "risk_score": 1.2, "tags": ["trends", "memes", "humor"]},
    {"id": 51, "title": "New App Everyone Is Downloading", "category": "trends", "engagement_score": 8.7, "risk_score": 1.5, "tags": ["trends", "apps", "tech"]},
    {"id": 52, "title": "Trending Recipes: The Ultimate Smash Burger", "category": "trends", "engagement_score": 8.4, "risk_score": 0.8, "tags": ["trends", "food", "recipe"]},

    # --- CELEBRITY (high-engagement, okay) ---
    {"id": 53, "title": "Celebrity Interviews: Honest and Relatable", "category": "celebrity", "engagement_score": 8.6, "risk_score": 2.0, "tags": ["celebrity", "interview", "entertainment"]},
    {"id": 54, "title": "Behind the Scenes: Movie Premiere", "category": "celebrity", "engagement_score": 8.1, "risk_score": 1.5, "tags": ["celebrity", "movies", "entertainment"]},
    {"id": 55, "title": "Famous Athletes Talk Mental Health", "category": "celebrity", "engagement_score": 7.9, "risk_score": 1.0, "tags": ["celebrity", "sports", "mental health"]},
    {"id": 56, "title": "Top Songs This Week", "category": "celebrity", "engagement_score": 8.8, "risk_score": 1.2, "tags": ["celebrity", "music", "trending"]},

    # --- APPEARANCE COMPARISON (risk cluster) ---
    {"id": 57, "title": "Rating My Face Before and After Filter", "category": "appearance_comparison", "engagement_score": 8.9, "risk_score": 7.8, "tags": ["appearance", "filter", "comparison"]},
    {"id": 58, "title": "Would You Date Me? Rate My Look", "category": "appearance_comparison", "engagement_score": 9.1, "risk_score": 8.5, "tags": ["appearance", "rating", "self-image"]},
    {"id": 59, "title": "My Body Transformation: 6 Months", "category": "appearance_comparison", "engagement_score": 8.7, "risk_score": 7.0, "tags": ["appearance", "body", "transformation"]},
    {"id": 60, "title": "Comparing Myself to This Celebrity", "category": "appearance_comparison", "engagement_score": 8.4, "risk_score": 8.0, "tags": ["appearance", "celebrity", "comparison"]},

    # --- VALIDATION SEEKING (risk cluster) ---
    {"id": 61, "title": "Nobody Likes Me and I Don't Know Why", "category": "validation_seeking", "engagement_score": 8.6, "risk_score": 8.2, "tags": ["validation", "loneliness", "social"]},
    {"id": 62, "title": "Asking Strangers If I'm Interesting", "category": "validation_seeking", "engagement_score": 8.3, "risk_score": 7.5, "tags": ["validation", "social", "self-esteem"]},
    {"id": 63, "title": "Am I Too Much to Handle? Honest Poll", "category": "validation_seeking", "engagement_score": 8.8, "risk_score": 8.0, "tags": ["validation", "poll", "identity"]},

    # --- REPETITIVE EMOTIONAL (risk cluster) ---
    {"id": 64, "title": "Sad Songs Playlist That Hits Different", "category": "repetitive_emotional", "engagement_score": 8.5, "risk_score": 6.5, "tags": ["emotional", "music", "sad"]},
    {"id": 65, "title": "Why Do I Always Feel Left Out?", "category": "repetitive_emotional", "engagement_score": 8.7, "risk_score": 7.2, "tags": ["emotional", "loneliness", "relatable"]},
    {"id": 66, "title": "Late Night Feelings Thread", "category": "repetitive_emotional", "engagement_score": 8.4, "risk_score": 6.8, "tags": ["emotional", "night", "feelings"]},
    {"id": 67, "title": "Things That Make Me Cry Instantly", "category": "repetitive_emotional", "engagement_score": 8.2, "risk_score": 6.3, "tags": ["emotional", "sad", "relatable"]},

    # --- NEGATIVITY LOOP (risk cluster) ---
    {"id": 68, "title": "Everything Is Getting Worse (Thread)", "category": "negativity_loop", "engagement_score": 8.3, "risk_score": 7.9, "tags": ["negativity", "rant", "stress"]},
    {"id": 69, "title": "Why I Hate Mondays: A Rant", "category": "negativity_loop", "engagement_score": 7.9, "risk_score": 6.5, "tags": ["negativity", "rant", "monday"]},
    {"id": 70, "title": "Nothing Goes Right For Me Ever", "category": "negativity_loop", "engagement_score": 8.5, "risk_score": 8.3, "tags": ["negativity", "venting", "hopeless"]},

    # --- DOOMSCROLL (risk cluster) ---
    {"id": 71, "title": "15 Things That Prove the World Is Broken", "category": "doomscroll", "engagement_score": 8.8, "risk_score": 8.7, "tags": ["doomscroll", "news", "anxiety"]},
    {"id": 72, "title": "How Bad Could Things Actually Get? (Thread)", "category": "doomscroll", "engagement_score": 8.5, "risk_score": 8.5, "tags": ["doomscroll", "anxiety", "future"]},
]

RISK_CATEGORIES = {
    "appearance_comparison",
    "validation_seeking",
    "repetitive_emotional",
    "negativity_loop",
    "doomscroll",
}

SAFE_CATEGORIES = {
    "study", "pets", "comedy", "sports", "art", "productivity",
    "fashion", "fitness", "trends", "celebrity",
}


def get_all_posts():
    """Return the full content pool."""
    return CONTENT_POOL


def get_posts_by_category(category: str):
    """Return posts filtered by category."""
    return [p for p in CONTENT_POOL if p["category"] == category]


def get_posts_by_id(post_id: int):
    """Return a single post by ID."""
    for post in CONTENT_POOL:
        if post["id"] == post_id:
            return post
    return None


def get_high_risk_posts(threshold: float = 5.0):
    """Return posts whose risk_score exceeds the threshold."""
    return [p for p in CONTENT_POOL if p["risk_score"] >= threshold]


def get_safe_posts(threshold: float = 5.0):
    """Return posts whose risk_score is below the threshold."""
    return [p for p in CONTENT_POOL if p["risk_score"] < threshold]


def get_categories():
    """Return list of unique categories."""
    return list({p["category"] for p in CONTENT_POOL})
