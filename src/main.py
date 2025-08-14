import argparse
import json
import sys
import modules
import asyncio
import modules.email_checker
import modules.social_media_checker
from target import Target
from rich.panel import Panel
from rich.console import Console
from rich.table import Table
from rich.text import Text


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


def present_email_info(t: Target):
    if not (t.email_breaches):
        console = Console()
        summary_text = Text(f"No email breaches found for: {t.email_address}", justify="center")
        console.print(
            Panel(summary_text, title="Scan Summary", style="bold green"))
    else:
        print()
        # print(t.email_breaches)
        with open("../data/email_info.json", "w") as f:
            json.dump(t.email_breaches, f)
        console = Console()
        summary_text = Text(f"Found {t.email_breaches.get('breaches_num')} breaches for: {t.email_address}\nRisk: {t.email_breaches.get('risk_label')} | Score: {t.email_breaches.get('risk_score')}", justify="center")

        table = Table(title="Breach Details")
        table.add_column("Breach Name", style="cyan")
        table.add_column("Domain", style="magenta")
        table.add_column("Breach Date", style="green")
        table.add_column("Description")

        for breach in t.email_breaches.get('breaches_in_detail'):
            table.add_row(
                breach['name'],
                breach['domain'],
                breach['xposed_date'],
                breach['details']
            )

        console.print(
            Panel(summary_text, title="Scan Summary", style="bold red"))
        console.print(table)


def present_info_gathered(t: Target):
    present_email_info(t)


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
        present_info_gathered(t)
        pass

    except Exception as e:
        # Print the error to the console
        print(f"[!] A critical error occurred: {e}", file=sys.stderr)


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
