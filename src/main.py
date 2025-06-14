import argparse
import json
import sys
import modules
import asyncio
import modules.email_checker
import modules.social_media_checker
from target import Target


def parse_arguements() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='OSINT-Tool',
        description='Gather info about a target based on what info is already provided'
    )

    parser.add_argument(
        '--target',
        required=True,
        help="who or what you are trying to gain info on"
    )

    parser.add_argument(
        '--fname',
        required=False,
        help="the first name of the target"
    )

    parser.add_argument(
        '--surname',
        required=False,
        help="the surname of the target"
    )

    parser.add_argument(
        '--email',
        required=False,
        help="the email of the target (e.g. tom@gmail.com)"
    )

    return parser.parse_args()


async def async_main():
    try:
        args = parse_arguements()

        t = Target(target_name=args.target, first_name=args.fname,
                   surname=args.surname, email_address=args.email)

        # Rest of logic
        print(f"Starting scan on {t.target_name}")

        print("INFO: Checking if email was breached")
        t.email_breaches = modules.email_checker.check_breaches(
            t.email_address)  # Getting email_breaches is done
        print("INFO: Finding social media accounts")
        t.social_media_profiles = await modules.social_media_checker.find_socials(t)
        pass

    except Exception as e:
        # Print the error to the console
        print(f"[!] A critical error occurred: {e}", file=sys.stderr)


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
