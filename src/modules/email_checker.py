import requests
import time

breach_info = {}


def check_no_breach(data, email):
    if 'Error' in data:
        if data['Error'] == 'Not found':
            print(
                f"No breaches associated with {email} on XposedOrNot database.")
            return True
    return False


def check_breaches(email: str) -> dict:
    # code to check whether there was a breach for an email
    # check Xposedornot

    api_url = f"https://api.xposedornot.com/v1/check-email/{email}"

    headers = {"User-Agent": "OSINT-Tool/1.0"}

    try:
        time.sleep(1)
        response = requests.get(api_url, headers=headers, timeout=30)

        if response.status_code == 200:

            data = response.json()

            if check_no_breach(data, email):
                return {}

            print("INFO: Breach detected!")
            breaches = data['breaches'][0]
            breach_info["breaches_num"] = len(breaches)  # useless currently
            # print(breaches)

            time.sleep(1)

            # move to a function?
            api_url = f"https://api.xposedornot.com/v1/breach-analytics?email={email}"
            # move to a function?
            response = requests.get(api_url, headers=headers, timeout=30)

            if response.status_code == 200:
                data = response.json()
                if check_no_breach(data, email):
                    return {}
                print("INFO: Getting more data on breaches")
                return data

            return {}

        elif response.status_code == 404:
            print(
                f"INFO: No breaches found for {email} on XposedOrNot (404 Not Found).")
            return {}

        elif response.status_code == 429:
            print(
                f"WARNING: Rate limit hit on initial check for {email}. Try again later.")
            return {}

        else:
            print(
                f"ERROR: Initial check API returned status {response.status_code} for {email}.")
            return {}

    except TimeoutError:
        print(
            f"ERROR: Request to XposedOrNot API timed out for {email} at {api_url}.")
    except requests.exceptions.RequestException as e:
        print(
            f"ERROR: An error occurred while querying XposedOrNot API for {email} at {api_url}: {e}")
    except ValueError:
        print(
            f"ERROR: Could not decode JSON response from XposedOrNot API for {email} at {api_url}.")
