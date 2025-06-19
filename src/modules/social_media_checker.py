
import target
import asyncio
import httpx
import logging
from holehe.modules.social_media.instagram import instagram
from holehe.modules.social_media.twitter import twitter
from holehe.modules.social_media.snapchat import snapchat
from holehe.modules.social_media.discord import discord
from holehe.modules.social_media.myspace import myspace
from holehe.modules.social_media.pinterest import pinterest
from holehe.modules.social_media.patreon import patreon
from holehe.modules.social_media.bitmoji import bitmoji
from holehe.modules.social_media.tumblr import tumblr
from holehe.modules.social_media.xing import xing

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SITES_TO_CHECK = [
    instagram,
    twitter,
    snapchat,
    discord,
    myspace,
    pinterest,
    patreon,
    bitmoji,
    tumblr,
    xing
    # Add other function names here...
]


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
    Checks email registrations by calling individual site modules from holehe
    concurrently, as shown in the official documentation.
    """
    logger.info(f"Checking email registrations for {email} on {len(SITES_TO_CHECK)} sites...")
    found_sites = []

    # Create an httpx.AsyncClient session, which holehe's modules need
    async with httpx.AsyncClient() as client:
        # Create a list of tasks to run concurrently for efficiency
        tasks = [run_site_check(email, client, site_func)
                 for site_func in SITES_TO_CHECK]

        # Run all tasks at the same time and wait for them to complete
        results = await asyncio.gather(*tasks)

        # Process the results, filtering out any 'None' values
        for result in results:
            if result is not None:
                found_sites.append(result)

    logger.info(f"Found email registrations on: {found_sites}") if found_sites else logger.info(f"No email registrations found.")
    return found_sites


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
