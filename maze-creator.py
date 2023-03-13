import requests
import os
from dotenv import load_dotenv

load_dotenv()

NOTION_KEY = os.environ.get("NOTION_KEY")
headers = {'Authorization': f"Bearer {NOTION_KEY}",
           'Content-Type': 'application/json',
           'Notion-Version': '2022-06-28'}

search_params = {"filter": {"value": "page", "property": "object"}}
search_response = requests.post(
    f'https://api.notion.com/v1/search',
    json=search_params, headers=headers)

search_results = search_response.json()["results"]
page_id = search_results[0]["id"]


# Define function to create a page with a given title and text
def create_page(icon, title, parent_id):
    create_page_body = {
        "parent": {"page_id": parent_id},
        "properties": {
            "title": {
                "title": [{
                    "type": "text",
                    "text": {"content": title}}]
            }
        },
        "icon": {
            "type": "emoji",
            "emoji": icon
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": ""
                        }
                    }]
                }
            }
        ]
    }
    create_response = requests.post(
        "https://api.notion.com/v1/pages",
        json=create_page_body, headers=headers)
    # print(create_response.json())
    return create_response.json()["id"]


# Define function to recursively create pages based on the matrix
def create_pages(matrix, x, y, parent_id, title):
    # page_title = f"Page {x},{y}"
    icon = ""
    if title == "Up":
        icon = "🔼"
    elif title == "Down":
        icon = "🔽"
    elif title == "Left":
        icon = "◀️"
    elif title == "Right":
        icon = "▶️"

    page_text = title
    new_page_id = create_page(icon, title, parent_id)
    mark_matrix[x][y] = 1
    # print(x, y, new_page_id)
    # for row in mark_matrix:
    #     print(row)
    # Add links to neighboring pages
    if x > 0 and matrix[x - 1][y] == 0 and mark_matrix[x - 1][y] == 0:
        print("Up", x, y)
        create_pages(matrix, x - 1, y, new_page_id, "Up")
        # add_link(new_page_id, left_id, "Left")
    if x < len(matrix) - 1 and matrix[x + 1][y] == 0 and mark_matrix[x + 1][y] == 0:
        print("Down", x, y)
        create_pages(matrix, x + 1, y, new_page_id, "Down")
        # add_link(new_page_id, right_id, "Right")
    if y > 0 and matrix[x][y - 1] == 0 and mark_matrix[x][y - 1] == 0:
        print("Left", x, y)
        create_pages(matrix, x, y - 1, new_page_id, "Left")
        # add_link(new_page_id, up_id, "Up")
    if y < len(matrix[0]) - 1 and matrix[x][y + 1] == 0 and mark_matrix[x][y + 1] == 0:
        print("Right", x, y)
        create_pages(matrix, x, y + 1, new_page_id, "Right")
        # add_link(new_page_id, down_id, "Down")

    # return new_page_id

matrix = [[1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
          [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
          [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
          [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
          [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1],
          [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
          [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1],
          [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
          [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
          [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
          [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1]
          ]

mark_matrix = [[0 for i in range(len(matrix[0]))] for j in range(len(matrix))]

create_pages(matrix, 10, 5, page_id, "Up")


