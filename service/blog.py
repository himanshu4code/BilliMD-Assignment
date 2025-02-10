from typing import List, Optional
from datetime import datetime
from models.blog import Blog
from database.db_ops import DatabaseOperations
from schemas.blog import BlogCreate, BlogUpdate, BlogResponse
from logger.blog_logger import setup_logger

logger = setup_logger(__name__)

class BlogService:
    @staticmethod
    def get_all_blogs(skip: int = 0, limit: int = 100) -> List[Blog]:
        logger.info(f"Fetching blogs with skip={skip}, limit={limit}")
        try:
            with DatabaseOperations() as db_ops:
                blogs = db_ops.get_all_records(Blog, skip, limit)
                logger.info(f"Successfully retrieved {len(blogs)} blogs")
                return blogs
        except Exception as e:
            logger.error(f"Error fetching blogs: {str(e)}")
            raise

    @staticmethod
    def get_blog_by_id(blog_id: int) -> Optional[Blog]:
        with DatabaseOperations() as db_ops:
            return db_ops.get_record(Blog, blog_id)

    @staticmethod
    def create_blog(data: BlogCreate, user: str) -> Blog:
        logger.info(f"Creating new blog for user: {user}")
        try:
            blog_data = data.model_dump()
            blog_data["created_at"] = datetime.utcnow()
            blog_data["user"] = user
            
            with DatabaseOperations() as db_ops:
                blog = db_ops.create_record(Blog, blog_data)
                logger.info(f"Successfully created blog with id: {blog.id}")
                return blog
        except Exception as e:
            logger.error(f"Error creating blog: {str(e)}")
            raise

    @staticmethod
    def update_blog(blog_id: int, data: BlogUpdate) -> Optional[Blog]:
        update_data = {k: v for k, v in data.model_dump().items() if v is not None}
        with DatabaseOperations() as db_ops:
            return db_ops.update_record(Blog, blog_id, update_data)

    @staticmethod
    def delete_blog(blog_id: int) -> bool:
        with DatabaseOperations() as db_ops:
            return db_ops.delete_record(Blog, blog_id)
