# AmazonLocationCookiesGenerator

Python utility for generating customized Amazon session cookies with specified location settings. This tool addresses the challenge that Amazon sets the delivery location based on the user's IP address, making it difficult to access other geographic regions. Supports multiple Amazon domains and delivery countries, enabling seamless configuration of location-specific preferences.

**Caution**: This tool is intended solely to help developers and testers simulate location-specific Amazon settings and is for internal use in development and testing only. It is strictly prohibited to use this tool for illegal activities or for fraudulent purposes, including but not limited to circumventing geo-blocks or abusing Amazon policies. Use of this tool is at your own risk and the developer disclaims any liability for misuse.

## Features

- Generate valid Amazon session cookies with location-specific settings
- Handle CSRF token management automatically
- Support for multiple Amazon locales (e.g.,DE, CO.UK, IT, ES, PL, SE, etc.)
- Support for multiple delivery countries (e.g., 'DE', 'GB', 'IT', 'ES', 'PL', 'SE')
- Save and load cookie sessions for reuse

## Requirements

```
beautifulsoup4
tls-client
typing_extensions
```

## Installation

1. Create a new virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

2. Clone the repository:
```bash
git clone https://github.com/yourusername/amazon-cookie-generator.git
cd amazon-cookie-generator
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage example:

```python
from amazon_cookie_generator import main

# Generate cookies for Italian Amazon store with German delivery location
cookie_path = 'cookies.pkl'
cookies = main(cookie_path, locale="IT", country_code="DE")
```

Alternatively, you can deserialize the saved cookies from the `cookies.pkl` file:

```python
import pickle
import tls_client

cookie_path = "cookies.pkl"

with open(cookie_path, 'rb') as file:
    cookies = pickle.load(file)

session = tls_client.Session()

session.cookies.update(cookies)

# Now you can use the cookies in other requests
```

## Configuration

- `locale`: Set the Amazon top-level domain (default: 'DE')
  - The 'locale' parameter should be the Amazon top-level domain (e.g., 'DE', 'CO.UK', 'IT', 'ES', 'PL', 'SE')

- `country_code`: Set the country code for delivery location
  - The 'country_code' parameter should be the delivery location country code (e.g., 'DE', 'GB', 'IT', 'ES', 'PL', 'SE')


- Note: These two parameters may not always match, as the top-level domains and country codes can be different


- For a full list of valid country codes, please refer to the [Country Code reference](https://countrycode.org/).


## License

This project is licensed under the [MIT License](LICENSE).

# Disclaimer

**Educational Use Only**  
This project is intended solely for educational purposes to demonstrate the technical aspects of handling cookies and geolocation settings on the web. It is not intended to be used for unauthorized scraping, bypassing of security measures, or any actions that violate the Terms of Service of any website, including but not limited to Amazon.com.

**Terms of Service Compliance**  
Users are responsible for ensuring compliance with the Terms of Service, policies, and legal restrictions of any platform they interact with. Unauthorized data extraction, scraping, or bypassing security mechanisms may violate such terms and could lead to account suspension, IP blocking, or legal action from affected platforms.

**Liability**  
The creator of this project is not responsible for any misuse of this code or any damages resulting from its use. By using or referencing this code, you agree to take full responsibility for your actions and to respect the legal restrictions of any websites you interact with.

If you need data from Amazon or similar platforms, please consider using official APIs provided by these platforms, such as the Amazon Product Advertising API, to ensure compliance with their policies.
