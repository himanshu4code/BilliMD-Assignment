from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource
from .common_constant import CERBOS_URL, CERBOS_PORT
from logger.blog_logger import setup_logger

client = CerbosClient(
    host=f"{CERBOS_URL}:{CERBOS_PORT}"
)

logger = setup_logger(__name__)

def check_permission(action: str, roles: list) -> bool:
    """
    Checks permission based solely on the user's roles.
    The resource is defined only by its kind.
    """
    logger.info(f"Checking permission for action: {action} with roles: {roles}")
    try:
        principal = Principal(id="default", roles=roles)
        resource = Resource(
            "default",           
            "blog",              
            policy_version="default",  
            attr={}
        )
        
        allowed = client.is_allowed(action=action, principal=principal, resource=resource)
        logger.info(f"Permission check result: {allowed}")
        return allowed
    except Exception as e:
        logger.error(f"Error checking permissions: {str(e)}")
        raise