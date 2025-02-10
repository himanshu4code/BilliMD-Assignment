import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.blog import Blog

def load_initial_data(session):
    # Read JSON file
    with open('database/blogs.json', 'r') as f:
        blogs_data = json.load(f)
    
    # Convert JSON data to Blog model instances
    blog_instances = [
        Blog(
            user=blog['user_id'],
            title=blog['title'],
            content=blog['content']
        ) for blog in blogs_data
    ]
    
    # Add all instances to session and commit
    session.add_all(blog_instances)
    session.commit()
    print("Initial blog posts loaded successfully!")

def init_database():
    engine = create_engine(os.getenv("BLOG_DB_URL"))
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Load initial data
    try:
        load_initial_data(session)
    except Exception as e:
        print(f"Error loading initial data: {e}")
        session.rollback()
    finally:
        session.close()
    
    print("Database initialization completed!")
