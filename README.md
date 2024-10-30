# AmazonCookieGenerator

A Python utility for generating and managing Amazon session cookies with location-based settings. This tool addresses the challenge that Amazon sets the delivery location based on the user's IP address, making it difficult to scrape data for other geographic regions. By handling CSRF token management and location preferences, this project enables the use of geolocation proxies to access Amazon data across multiple locales.

## Features

- Generate valid Amazon session cookies with location-specific settings
- Handle CSRF token management automatically
- Support for multiple Amazon locales (DE, UK, US, etc.)
- Save and load cookie sessions for reuse
- TLS client implementation for secure connections

## Requirements

```
beautifulsoup4
tls-client
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/amazon-cookie-generator.git
cd amazon-cookie-generator
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage example:

```python
from amazon_cookie_generator import main

# Generate cookies for German Amazon store
cookie_path = 'data/cookies/cookies.pkl'
cookies = main(cookie_path, locale="DE")
```

Configuration options:
```python
config = CookieGeneratorConfig(
    locale='DE',          # Country locale (e.g., 'DE', 'UK', 'US')
    zip_code=10115,       # Default ZIP code for location
    country_code="DE"     # Country code for location settings
)
```

## Configuration

The tool supports various configuration options through the `CookieGeneratorConfig` class:

- `locale`: Set the Amazon store locale (default: 'DE')
- `client_identifier`: Set the browser client type
- `zip_code`: Set the default ZIP code
- `country_code`: Set the country code

## Error Handling

The tool includes custom exceptions for various error cases:
- `InvalidRequestMethodException`
- `RequestErrorException`
- `TokenElementNotFoundException`
- `DataModalNotFoundException`
- `AntiCsrfTokenNotFoundException`
- `CsrfTokenNotFoundException`

## License

[Choose an appropriate license]

## Disclaimer

This tool is for educational and research purposes only. Make sure to comply with Amazon's terms of service and robots.txt when using this tool. Avoid excessive or malicious scraping, as it may result in account restrictions or legal actions.
