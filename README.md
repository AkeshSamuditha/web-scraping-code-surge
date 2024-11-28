# Web Scraping Project

This project is designed to scrape documentation from AWS Lambda and React websites. The scraped data is then saved into a JSON file.

## Project Structure

```
.
├── aws.py
├── main.py
├── react.py
└── README.md
```

- `aws.py`: Contains functions to scrape AWS Lambda documentation.
- `react.py`: Contains functions to scrape React documentation.
- `main.py`: Main script to run the scraping and save the data to a JSON file.
- `README.md`: This file.

## Prerequisites

- Python 3.x
- `requests` library
- `beautifulsoup4` library

You can install the required libraries using pip:

```sh
pip install requests beautifulsoup4
```

## How to Run

1. Clone the repository or download the source code.
2. Navigate to the project directory.
3. Run the main script:

```sh
python main.py
```

If you want to save the output to a custom file, you can provide the output file name as an argument when running the script:

```sh
python main.py --output_file output.json
```

## Output Format

The scraped data is saved in a JSON file with the following structure:

```json
{
  "aws_lambda": [
    {
      "title": "Example Title",
      "url": "https://example.com",
      "source": "react | aws_lambda",
      "sections": {
        "summary": "Brief summary of the documentation page.",
        "subsection": [
          {
            "title": "Subsection Title",
            "content": "content of the subsection as a sections",
            "urls": ["https://example.com/subsection"],
            "code": [
              {
                "language": "python",
                "code": "print('Hello, World!')"
              }
            ]
          }
        ]
      }
    }
  ]
}
```

- `aws_lambda`: A list of dictionaries containing scraped data from AWS Lambda documentation.
- `react`: A list of dictionaries containing scraped data from React documentation.
- Each dictionary contains:
  - `title`: The title of the documentation page.
  - `url`: The URL of the documentation page.
  - `source` : The Source of the page ('react' | 'aws_lambda')
  - `content`: The main content extracted from the documentation page.
    - `summary`: A brief summary of the documentation page.
    - `subsection`: A list of subsections within the documentation page, each containing:
    - `title`: The title of the subsection.
    - `content`: The main content of the subsection, which may contain up to two levels of subsections.
    - `urls`: A list of URLs found within the subsection.
      - `code`: A list of dictionaries each containing:
        - `language`: The programming language of the code snippet.
        - `code`: The code snippet itself.
      - `urls`: A list of URLs found within the subsection.
