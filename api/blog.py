from logger.blog_logger import setup_logger
from fastapi import APIRouter, HTTPException, Header, Depends
from schemas.blog import BlogCreate, BlogUpdate, BlogResponse, BlogCreateResponse
from service.blog import BlogService
from typing import Tuple
from utils.cerbos_ops import check_permission

router = APIRouter()

logger = setup_logger(__name__)

async def get_user_details(
    x_user: str = Header(..., description="User identifier"),
    x_role: str = Header(..., description="User role")
) -> Tuple[str, str]:
    if not x_user or not x_role:
        logger.error(f"Missing user details in headers")
        raise HTTPException(status_code=401, detail="Missing user details in headers")
    logger.info(f"User authenticated: {x_user} with role: {x_role}")
    return x_user, x_role

@router.get("/blogs", response_model=list[BlogResponse])
async def list_blogs(
    user_details: Tuple[str, str] = Depends(get_user_details),
    skip: int = 0, 
    limit: int = 100
):
    user, role = user_details
    logger.info(f"Listing blogs request from user: {user}")
    if not check_permission("view", [role]):
        logger.warning(f"Permission denied for user: {user} to view blogs")
        raise HTTPException(status_code=403, detail="Permission denied")
    return BlogService.get_all_blogs(skip, limit)

@router.get("/blogs/{blog_id}", response_model=BlogResponse)
async def get_blog(
    blog_id: int,
    user_details: Tuple[str, str] = Depends(get_user_details)
):
    user, role = user_details
    blog = BlogService.get_blog_by_id(blog_id)
    if not blog:
        logger.error(f"Blog not found: {blog_id}")
        raise HTTPException(status_code=404, detail="Blog not found")
    
    if not check_permission("view", [role]):
        logger.warning(f"Permission denied for user: {user} to view blog: {blog_id}")
        raise HTTPException(status_code=403, detail="Permission denied")
    return blog

@router.put("/blogs/{blog_id}")
async def update_blog(
    blog_id: int, 
    data: BlogUpdate,
    user_details: Tuple[str, str] = Depends(get_user_details)
):
    user, role = user_details
    blog = BlogService.get_blog_by_id(blog_id)
    if not blog:
        logger.error(f"Blog not found: {blog_id}")
        raise HTTPException(status_code=404, detail="Blog not found")
    
    if blog.user != user:
        logger.warning(f"User: {user} attempted to update blog: {blog_id} owned by another user")
        raise HTTPException(status_code=403, detail="You can only update your own blogs")
    
    if not check_permission("update", [role]):
        logger.warning(f"Permission denied for user: {user} to update blog: {blog_id}")
        raise HTTPException(status_code=403, detail="Permission denied")
    
    blog = BlogService.update_blog(blog_id, data)
    logger.info(f"Blog updated successfully: {blog_id}")
    return {"message": "Blog updated successfully"}

@router.post("/blogs", response_model=BlogCreateResponse, status_code=201)
async def create_blog(
    data: BlogCreate,
    user_details: Tuple[str, str] = Depends(get_user_details)
):
    user, role = user_details
    if not check_permission("create", [role]):
        logger.warning(f"Permission denied for user: {user} to create blog")
        raise HTTPException(status_code=403, detail="Permission denied")
    
    new_blog = BlogService.create_blog(data, user=user)
    logger.info(f"Blog created successfully: {new_blog.id}")
    return BlogCreateResponse(
        id=new_blog.id,
        message="Blog created successfully"
    )

@router.delete("/blogs/{blog_id}")
async def delete_blog(
    blog_id: int,
    user_details: Tuple[str, str] = Depends(get_user_details)
):
    user, role = user_details
    blog = BlogService.get_blog_by_id(blog_id)
    if not blog:
        logger.error(f"Blog not found: {blog_id}")
        raise HTTPException(status_code=404, detail="Blog not found")
    
    if not check_permission("delete", [role]):
        logger.warning(f"Permission denied for user: {user} to delete blog: {blog_id}")
        raise HTTPException(status_code=403, detail="Permission denied")
    
    if not BlogService.delete_blog(blog_id):
        logger.error(f"Failed to delete blog: {blog_id}")
        raise HTTPException(status_code=404, detail="Blog not found")
    logger.info(f"Blog deleted successfully: {blog_id}")
    return {"message": "Blog deleted successfully"}
