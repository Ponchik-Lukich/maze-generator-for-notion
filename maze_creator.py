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


def create_page(icon, title, start_page_id=page_id):
    create_page_body = {
        "parent": {"page_id": start_page_id},
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


def create_pages(matrix, y, x, title):
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
    elif title == "Start":
        icon = "🚷"

    new_page_id = create_page(icon, title, start_page_id)
    if y == 1 and x == first_row_zero_index:
        finish_page_id = create_page("🏁", "Finish", new_page_id)
        print("Finish created:", finish_page_id)

    print("Created:", new_page_id, title)
    mark_matrix[y][x] = 1
    if y > 0 and matrix[y - 1][x] == 0:
        if mark_matrix[y - 2][x] == 0:
            print("Up", y, x)
            up_id = create_pages(matrix, y - 2, x, "Up")
            print("adding link up", new_page_id, up_id)
            add_link(new_page_id, up_id, "Up", title)
            # create_pages(matrix, y - 2, x, new_page_id, "Up")
    if y < len(matrix) - 1 and matrix[y + 1][x] == 0:
        if mark_matrix[y + 2][x] == 0:
            print("Down", y, x)
            down_id = create_pages(matrix, y + 2, x, "Down")
            print("adding link down", new_page_id, down_id)
            add_link(new_page_id, down_id, "Down", title)
    if x > 0 and matrix[y][x - 1] == 0:
        if mark_matrix[y][x - 2] == 0:
            print("Left", y, x)
            left_id = create_pages(matrix, y, x - 2, "Left")
            print("adding link left", new_page_id, left_id)
            add_link(new_page_id, left_id, "Left", title)
    if x < len(matrix[0]) - 1 and matrix[y][x + 1] == 0:
        if mark_matrix[y][x + 2] == 0:
            print("Right", y, x)
            right_id = create_pages(matrix, y, x + 2, "Right")
            print("adding link right", new_page_id, right_id)
            add_link(new_page_id, right_id, "Right", title)
    return new_page_id


def add_link(page_id, linked_page_id, direction, title):
    page_id = page_id.replace("-", "")
    linked_page_id = linked_page_id.replace("-", "")
    direction = direction.replace("-", "")

    update_block_body = {
        "operations": [
            {
                "id": page_id,
                "path": "properties.Links",
                "command": "update",
                "value": [
                    {
                        "type": "embed",
                        "embed": {
                            "url": f"https://www.notion.so/{linked_page_id}",
                            "caption": {
                                "text": [
                                    {
                                        "type": "text",
                                        "text": {
                                            "content": ""
                                        }
                                    }
                                ]
                            }
                        }
                    }
                ]
            }
        ]
    }
    update_response = requests.patch(
        "https://api.notion.com/v1/blocks",
        json=update_block_body, headers=headers)
    print("------ ", f"https://www.notion.so/{linked_page_id}")
    print("------ ", f"https://www.notion.so/{page_id}")
    print(update_response.json())


matrix = parse_maze("images/5x5Maze.png")

mark_matrix = [[0 for i in range(len(matrix[0]))] for j in range(len(matrix))]
last_row_zero_index = 0
first_row_zero_index = 0
# find index of zero in last row
for i in range(len(matrix[0])):
    if last_row_zero_index != 0 and first_row_zero_index != 0:
        break
    if matrix[len(matrix) - 1][i] == 0:
        last_row_zero_index = i
    if matrix[0][i] == 0:
        first_row_zero_index = i
matrix[0][first_row_zero_index] = 1
matrix[len(matrix) - 1][last_row_zero_index] = 1

start_page_id = create_page("🚷", "Start page", page_id)
print("New-Maze:", page_id)
print("Start page:", start_page_id)
create_pages(matrix, len(matrix) - 2, last_row_zero_index, "Start")
