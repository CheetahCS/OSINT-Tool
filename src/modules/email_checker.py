import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

    breach_info = {}

    try:
        time.sleep(1)
        response = requests.get(api_url, headers=headers, timeout=30)

        if response.status_code == 200:

            data = response.json()

            if check_no_breach(data, email):
                return {}

            logger.info(" Breach detected!")
            # print("INFO: Breach detected!")
            breaches = data['breaches'][0]
            breach_info["names"] = breaches
            breach_info["breaches_num"] = len(breaches)

            time.sleep(1)

            # move to a function?
            api_url = f"https://api.xposedornot.com/v1/breach-analytics?email={email}"
            # move to a function?
            response = requests.get(api_url, headers=headers, timeout=30)

            if response.status_code == 200:
                data = response.json()
                if check_no_breach(data, email):
                    return {}
                logger.info(" Getting more data on breaches")

                breach_info['risk_label'] = data['BreachMetrics']['risk'][0]['risk_label']
                breach_info['risk_score'] = data['BreachMetrics']['risk'][0]['risk_score']

                breaches_list = data["ExposedBreaches"]["breaches_details"]
                data_on_breaches = []
                for i in range(len(breaches_list)):
                    useful_info = {
                        'name': breaches_list[i]['breach'],
                        'details': breaches_list[i]['details'],
                        'domain': breaches_list[i]['domain'],
                        'password_risk': breaches_list[i]['password_risk'],
                        'xposed_data': breaches_list[i]['xposed_data'],
                        'xposed_date': breaches_list[i]['xposed_date'],
                        'xposed_records': breaches_list[i]['xposed_records']
                    }
                    data_on_breaches.append(useful_info)

                breach_info['breaches_in_detail'] = data_on_breaches

                return breach_info

            return {}

        elif response.status_code == 404:
            logger.info(
                f" No breaches found for {email} on XposedOrNot (404 Not Found).")
            # print(
            # f"INFO: No breaches found for {email} on XposedOrNot (404 Not Found).")
            return {}

        elif response.status_code == 429:
            logger.warning(
                f" Rate limit hit on initial check for {email}. Try again later.")
            # print(
            #     f"WARNING: Rate limit hit on initial check for {email}. Try again later.")
            return {}

        else:
            logger.error(
                f" Initial check API returned status {response.status_code} for {email}")
            # print(
            #     f"ERROR: Initial check API returned status {response.status_code} for {email}.")
            return {}

    except TimeoutError:
        logger.error(
            f" Request to XposedOrNot API timed out for {email} at {api_url}.")
        # print(
        #     f"ERROR: Request to XposedOrNot API timed out for {email} at {api_url}.")
    except requests.exceptions.RequestException as e:
        logger.error(
            f" An error occurred while querying XposedOrNot API for {email} at {api_url}: {e}")
        # print(
        #     f"ERROR: An error occurred while querying XposedOrNot API for {email} at {api_url}: {e}")
    except ValueError:
        logger.error(
            f" Could not decode JSON response from XposedOrNot API for {email} at {api_url}")
        # print(
        #     f"ERROR: Could not decode JSON response from XposedOrNot API for {email} at {api_url}.")
