import json
from react import scrape_react
from aws import scrape_lmbda
import argparse
def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def scrape_and_save(save_file = 'scraped_data.json'):
    react_docs = scrape_react()
    lambda_docs = scrape_lmbda()
   
    all_data = react_docs + lambda_docs
    # save_to_json(react_docs, 'react.json')
    # save_to_json(lambda_docs, 'lambda.json')
    save_to_json(all_data, save_file)
    print("Saved To", save_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape data and save to a JSON file.')
    parser.add_argument('output_file', nargs='?', default='scrape.json', help='The output file to save the scraped data')
    args = parser.parse_args()

    scrape_and_save(args.output_file)