import json
import pickle
import re

import tls_client
import traceback
from bs4 import BeautifulSoup

class CookieGeneratorConfig:
    def __init__(self, locale='DE'):
        self.locale = locale
        self.client_identifier = "chrome_112"
        self.zip_code = 10115
        self.country_code = "DE"
        self.update_urls()

    def update_urls(self):
        self.url_amazon = f"https://www.amazon.{self.locale}/"
        self.url_glow_rendered_address_selections = f"https://www.amazon.{self.locale}/portal-migration/hz/glow/get-rendered-address-selections"
        self.url_glow_address_change = f"https://www.amazon.{self.locale}/portal-migration/hz/glow/address-change"

    def set_locale(self, locale):
        self.locale = locale
        self.update_urls()


class InvalidRequestMethodException(Exception):
    "Raised when an invalid request method is used"
    pass


class RequestErrorException(Exception):
    "Raised when a request error occured"
    pass


class TokenElementNotFoundException(Exception):
    "Raised when a token element could not be found"
    pass


class DataModalNotFoundException(Exception):
    "Raised when a data modal could not be found"
    pass


class AntiCsrfTokenNotFoundException(Exception):
    "Raised when an anti csrf token could not be found"
    pass


class CsrfTokenNotFoundException(Exception):
    "Raised when a csrf token could not be found"
    pass


def send_request(url, session, method="GET", headers=None, params=None, json=None):
    if method == "GET":
        response = session.get(url, headers=headers, params=params, json=json)
    elif method == "POST":
        response = session.post(url, headers=headers, params=params, json=json)
    else:
        raise InvalidRequestMethodException

    if response.status_code == 200:
        return response, session
    else:
        print(f"Fehler beim Abrufen der Webseite: Statuscode {response.status_code}")
        raise RequestErrorException


def extract_anti_csrf_token(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    token_element = soup.find('span', {'id': 'nav-global-location-data-modal-action'})
    if token_element:
        data_modal = token_element.get('data-a-modal')
        if data_modal:
            data_modal_json = json.loads(data_modal.replace('&quot;', '"'))
            anti_csrf_token = data_modal_json.get('ajaxHeaders', {}).get('anti-csrftoken-a2z', '')
            if anti_csrf_token:
                return anti_csrf_token
            else:
                raise AntiCsrfTokenNotFoundException
        else:
            raise DataModalNotFoundException
    else:
        raise TokenElementNotFoundException


def extract_csrf_token(response_text):
    match = re.search(r'CSRF_TOKEN : "(.+?)"', response_text)
    if match:
        return match.group(1)
    else:
        raise CsrfTokenNotFoundException


def main(cookie_path, locale="DE"):

    config = CookieGeneratorConfig(locale=locale)

    url_amazon = config.url_amazon
    url_glow_rendered_address_selections = config.url_glow_rendered_address_selections
    url_glow_address_change = config.url_glow_address_change
    client_identifier = config.client_identifier
    zip_code = config.zip_code
    country_code = config.country_code

    session = tls_client.Session(client_identifier=client_identifier, random_tls_extension_order=True)
    amazon_base_response, session = send_request(url_amazon, session, "GET")
    html_content = amazon_base_response.text

    anti_csrf_token = extract_anti_csrf_token(html_content)

    print(f"Anti-CSRF-Token: {anti_csrf_token}")

    headers = {'anti-csrftoken-a2z': anti_csrf_token}

    params = {
        'deviceType': 'desktop',
        'pageType': 'Gateway',
        'storeContext': 'NoStoreName',
        'actionSource': 'desktop-modal',
    }

    rendered_address_selection_response, session = send_request(url_glow_rendered_address_selections, session,
                                                                "GET", params=params, headers=headers)

    csrf_token = extract_csrf_token(rendered_address_selection_response.text)
    print("CSRF-TOKEN: ", csrf_token)

    headers['anti-csrftoken-a2z'] = csrf_token

    params = {'actionSource': 'glow'}

    if locale == "DE":
        # Eigentlich unnötig, da es mit Country Code auch funktioniert.
        json_data = {
            'locationType': 'LOCATION_INPUT',
            'zipCode': zip_code,
            'deviceType': 'web',
            'storeContext': 'generic',
            'pageType': 'Gateway',
            'actionSource': 'glow',
        }

    else:

        json_data = {
            'locationType': 'COUNTRY',
            'district': country_code,
            'countryCode': country_code,
            'deviceType': 'web',
            'storeContext': 'generic',
            'pageType': 'Gateway',
            'actionSource': 'glow',
        }

    glow_address_change_response, session = send_request(url_glow_address_change, session, "POST", headers=headers,
                                                         params=params, json=json_data)

    print(glow_address_change_response.status_code)
    print(glow_address_change_response.text)


    # Speichern der HTML-Antwort für weitere Analysen
    with open("TEST.html", "w", encoding='UTF-8') as html_file:
        html_file.write(session.get(url_amazon).text)

    # Cookies speichern
    with open(cookie_path, 'wb') as file:
        pickle.dump(session.cookies, file)

    """
    # Neue Session erstellen
    session2 = tls_client.Session()

    session2.cookies.update(session.cookies)

    # Jetzt kannst du die Session mit den geladenen Cookies verwenden
    response = session2.get(url_amazon)
    """

    return session.cookies


if __name__ == "__main__":
    cookie_path = 'cookies.pkl'
    main(cookie_path, "DE")
