import requests
import json
import os
from dotenv import load_dotenv
# Load the .env file
load_dotenv()

# TODO: Make sure that you have a NOTION_SECRET environment variable set
NOTION_TOKEN = os.getenv('NOTION_SECRET', '')


def query_filter(notion_id: str):

    # You can have a single filter
    # More information about filter: https://developers.notion.com/reference/post-database-query#post-database-query-filter
    payload = {
        'filter':
            {
                'property': 'Name',  # Column name
                'text': {
                    'contains': 'a'  # filter and value to filter for
                }
            }
    }
# {'property': 'Name', 'text': {'contains': 'a'}}
    # Or you can have multiple filter:
    """
    payload = {
        'filter':
        {
            'and': [
                {
                    'property': 'Seen',
                    'checkbox': {
                        'equals': False
                    }
                },
                {
                    'property': 'Yearly visitor count',
                    'number': {
                        'greater_than': 1000000
                    }
                }
            ]
        }
    }
    """
    # The actual API request
    response = requests.post('https://api.notion.com/v1/databases/{}/query'.format(notion_id), json=payload, headers={
        'Authorization': 'Bearer '+NOTION_TOKEN, 'Notion-Version': '2021-08-16'})

    # If the request was not successful, we print the error and return
    if not response.ok:
        print('Error:', response.status_code)
        print('Error:', response.content)
        return

    # Parse the response as JSON
    data = response.json()

    # If you want to see the complete response, uncomment the following line
    print(json.dumps(data, indent=4))

    return data['results']


if __name__ == "__main__":

    # ID of the notion row/page
    # You can get the ID by listing all databases first (list_databases.py)
    # You can not copy the id from the app!
    # I suggest using the same database as in the recurring_tasks project
    database_id = "23d29aa90e024458b947282d7d16ec27" #Dbase

    # Call function to query the database
    rows = query_filter(database_id)

    # Something failed:(
    if rows is None:
        exit(1)

    for row in rows:
        # Find the title row
        title = 'Untitled'
        # Iterate over all columns and find the title column
        for property_key in row['properties']:
            property = row['properties'][property_key]
            if property['type'] == 'title':  # If we find the title column
                # Join all title parts together and ignore the formatting
                title = ''.join([t['plain_text'] for t in property['title']])

        # Print id and title
        print(row['id'], title)

        # If you want to see the complete row, uncomment the following line
        print(json.dumps(row, indent=4))
