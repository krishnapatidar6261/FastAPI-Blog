from app.blogs.models import HashTags
from database.session import get_db
from sqlalchemy.orm import Session


tags = [
    'Python', 'Programming', 'Coding', 'Developer', 'SoftwareDevelopment', 'Tech', 'Technology', 'CodeNewbie', '100DaysOfCode', 
    'DeveloperLife', 'MachineLearning', 'AI', 'DataScience', 'JavaScript', 'WebDevelopment', 'CloudComputing', 'DevOps', 'CyberSecurity', 
    'BigData', 'Innovation', 'DigitalMarketing', 'SocialMediaMarketing', 'ContentMarketing', 'SEO', 'MarketingTips', 'Business', 'Startup',
    'Entrepreneur', 'SmallBusiness', 'Success', 'Motivation', 'Leadership', 'MarketingStrategy', 'GrowthHacking', 'Branding', 'Photography',
    'Art', 'PhotoOfTheDay', 'Artist', 'DigitalArt', 'Artwork', 'Illustration', 'Design', 'Creative', 'InstaArt', 'Photographer', 'Picoftheday',
    'Capture', 'VisualArt', 'artoftheday', 'Fitness', 'Health', 'Workout', 'Gym', 'HealthyLifestyle', 'FitnessMotivation', 'Wellness', 'FitFam',
    'Nutrition', 'Yoga', 'Running', 'Bodybuilding', 'HealthyEating', 'Mindfulness', 'SelfCare'
]


def add_hashtags(lst):
    # get_db is usually a generator dependency, so we need next()
    db: Session = next(get_db())

    for tag in lst:
        # check if tag already exists
        exists = db.query(HashTags).filter(HashTags.name == tag).first()
        if not exists:
            hashtag = HashTags(name=tag)
            db.add(hashtag)

            db.commit()
            db.close()
    print("✅ Hashtags added successfully!")


if __name__ == "__main__":
    add_hashtags(tags)
