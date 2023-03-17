# Notion Maze Creator

Notion Maze Creator is a Python-based project that generates a maze within Notion using Notion API. Given an image of a maze, the script creates a series of interconnected pages representing the maze structure.

## Prerequisites

Before running this project, make sure you have the following:

- Python 3.6 or higher
- A Notion account with API access
- An image of a maze in PNG format from websites such as [Maze Generator](https://mazegenerator.net/)

## Installation

1. Clone this repository.
2. Install the required Python packages:

pip install -r requirements.txt

3. Set up your Notion API key:

Create a `.env` file in the project's root directory with the following content:

Replace `NOTION_KEY` with your actual Notion API key.

## Usage

1. Run the `maze-creator.py` script with the maze image as an argument:

The script will create a maze within your Notion account and print the page IDs of the created pages.

2. Make the created pages public:

Run the provided JavaScript code in the developer console of your Notion page. Replace `<your_notion_auth_token>`, `<your_copied_page_ids_from_maze_creator>`, and `<your_notion_space_id>` with the appropriate values.
Аfter that, all pages of the maze should be public when their parent page should be open.

3. Explore the maze:

Navigate to the created maze pages within your Notion account and start exploring!
