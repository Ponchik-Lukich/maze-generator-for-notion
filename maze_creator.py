import requests
import os
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
default_children = [
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": "Dead end!"
                }
            }]
        }
    }
]


def make_children(page_children):
    json_children = []
    if len(page_children) == 0:
        json_children = default_children
    else:
        for child in page_children:
            json_children.append({
                "object": "block",
                "type": "link_to_page",
                "link_to_page": {
                    "page_id": child
                }
            })
    return json_children


def create_page(icon, title, children):
    create_page_body = {
        "parent": {"page_id": page_id},
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
        "children": children,
    }
    while True:
        try:
            create_response = requests.post(
                "https://api.notion.com/v1/pages",
                json=create_page_body, headers=headers)
            page_ids.append(create_response.json()["id"])
            # print(create_response.json())
            break
        except Exception as e:
            print(e)
            print(create_response.text)

    # time.sleep(1)
    return create_response.json()["id"]


def create_pages(y, x, title):
    mark_matrix[y][x] = 1
    page_children = []
    if y > 0 and matrix[y - 1][x] == 0:
        if mark_matrix[y - 2][x] == 0:
            up_id = create_pages(y - 2, x, "Up")
            page_children.append(up_id)
    if y < len(matrix) - 1 and matrix[y + 1][x] == 0:
        if mark_matrix[y + 2][x] == 0:
            down_id = create_pages(y + 2, x, "Down")
            page_children.append(down_id)
    if x > 0 and matrix[y][x - 1] == 0:
        if mark_matrix[y][x - 2] == 0:
            left_id = create_pages(y, x - 2, "Left")
            page_children.append(left_id)
    if x < len(matrix[0]) - 1 and matrix[y][x + 1] == 0:
        if mark_matrix[y][x + 2] == 0:
            right_id = create_pages(y, x + 2, "Right")
            page_children.append(right_id)
    if y == 1 and x == first_row_zero_index:
        finish_page_id = create_page("🏁", "Finish", default_children)
        page_children.append(finish_page_id)
        print("Finish created:", finish_page_id)
    icon = ""
    if len(page_children) == 0:
        icon = "💀"
        title = "Dead end"
    else:
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
    # print("Creating:", icon, title, make_children(page_children))
    new_page_id = create_page(icon, title, make_children(page_children))
    print("Created:", new_page_id, title)
    return new_page_id


matrix = parse_maze("images/5x5Maze.png")
page_ids = []

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

print("New-Maze:", page_id)
start_page_id = create_pages(len(matrix) - 2, last_row_zero_index, "Start")
print(page_ids)

