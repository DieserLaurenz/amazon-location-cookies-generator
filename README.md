# AmazonLocationCookiesGenerator

A Python utility for generating Amazon session cookies with desired location settings. This tool addresses the challenge that Amazon sets the delivery location based on the user's IP address, making it difficult to scrape data for other geographic regions. The generated cookies may be used to access Amazon data across multiple locales.

## Features

- Generate valid Amazon session cookies with location-specific settings
- Handle CSRF token management automatically
- Support for multiple Amazon locales (DE, CO.UK, IT, ES, PL, SE, etc.)
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

## Disclaimer

This tool is for educational and research purposes only. Make sure to comply with Amazon's terms of service and robots.txt when using this tool. Avoid excessive or malicious scraping, as it may result in account restrictions or legal actions.
