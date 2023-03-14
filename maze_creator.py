import requests
import os
from dotenv import load_dotenv
from maze_parser import parse_maze

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


def create_pages(matrix, y, x, parent_id, title):
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

    new_page_id = create_page(icon, title, parent_id)
    if y == 1 and x == first_row_zero_index:
        finish_page_id = create_page("🏁", "Finish", new_page_id)
        print("Finish created:", finish_page_id)

    print("Created:", new_page_id)
    mark_matrix[y][x] = 1
    if y > 0 and matrix[y - 1][x] == 0:
        if mark_matrix[y - 2][x] == 0:
            print("Up", y, x)
            create_pages(matrix, y - 2, x, new_page_id, "Up")
    if y < len(matrix) - 1 and matrix[y + 1][x] == 0:
        if mark_matrix[y + 2][x] == 0:
            print("Down", y, x)
            create_pages(matrix, y + 2, x, new_page_id, "Down")
    if x > 0 and matrix[y][x - 1] == 0:
        if mark_matrix[y][x - 2] == 0:
            print("Left", y, x)
            create_pages(matrix, y, x - 2, new_page_id, "Left")
    if x < len(matrix[0]) - 1 and matrix[y][x + 1] == 0:
        if mark_matrix[y][x + 2] == 0:
            print("Right", y, x)
            create_pages(matrix, y, x + 2, new_page_id, "Right")


matrix = parse_maze("images/5x5Maze.png")

mark_matrix = [[0 for i in range(len(matrix[0]))] for j in range(len(matrix))]
last_row_zero_index = 0
first_row_zero_index = 0
# find index of zero in last row
for i in range(len(matrix[0])):
    if last_row_zero_index != 0 and first_row_zero_index !=0:
        break
    if matrix[len(matrix) - 1][i] == 0:
        last_row_zero_index = i
    if matrix[0][i] == 0:
        first_row_zero_index = i
matrix[0][first_row_zero_index] = 1
matrix[len(matrix) - 1][last_row_zero_index] = 1

start_page_id = create_page("🚷", "Start page", page_id)
create_pages(matrix, len(matrix) - 2, last_row_zero_index, start_page_id, "Up")
