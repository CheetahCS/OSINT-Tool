import target
import asyncio
import httpx
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def find_socials(t: target.Target):
    check_by_names()

    if t.email_address:
        await check_by_email(t.email_address)

    check_by_phone_number()
    pass


def check_by_names():
    pass


async def check_by_email(email: str):
    """
    Checks email registrations by making a request to each company registration page to
    determine whether an email is registered or not.
    """

    
    return 


async def run_site_check(email, client, site_function):
    """
    Helper function to run a single site check and safely handle its output.
    """

    # The holehe functions expect a list to append their result dictionary to
    site_name = getattr(site_function, '__name__', 'unknown')
    output_list = []

    try:
        # Call the specific site function (e.g., instagram(email, client, out))
        await site_function(email, client, output_list)
        if output_list:
            result_dict: dict = output_list[0]
            # Check if the 'exists' key is True in the result
            if result_dict.get("exists"):
                # Return the name of the site if found
                return result_dict.get("name")
            
    
    except asyncio.TimeoutError:
        logger.warning(f"Timeout checking {site_name}")
    except httpx.RequestError as e:
        logger.warning(f"Request error checking {site_name}: {e}")
    except Exception as e:
        logger.warning(f"Unexpected error checking {site_name}: {e}")
        pass

    logger.info(f"None on {site_name}")
    return None  # Return None if not found or if an error occurred
    

def check_by_phone_number():
    pass
