// run this in console on notion.so

const makePagePublic = async (pageId, spaceId) => {
  const authToken = "<your_notion_auth_token>";

  const payload = {
    "requestId": "e294a9cf-cd6a-4db5-a422-a1bfa63c7660",
    "transactions": [
      {
        "id": "8713127b-35c0-4e6c-9324-5d717e4a7bc6",
        "spaceId": spaceId,
        "debug": {
          "userAction": "BlockPermissionsSettings.handlePermissionItemChange"
        },
        "operations": [
          {
            "pointer": {
              "table": "block",
              "id": pageId,
              "spaceId": spaceId
            },
            "command": "setPermissionItem",
            "path": [
              "permissions"
            ],
            "args": {
              "type": "public_permission",
              "role": "reader",
              "added_timestamp": Date.now()
            }
          },
          {
            "pointer": {
              "table": "block",
              "id": pageId,
              "spaceId": spaceId
            },
            "path": [],
            "command": "update",
            "args": {
              "last_edited_time": Date.now()
            }
          }
        ]
      }
    ]
  };

  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "cookie": `token_v2=${authToken}`,
    },
    body: JSON.stringify(payload)
  };

  const response = await fetch("https://www.notion.so/api/v3/saveTransactions", requestOptions);
  const data = await response.json();

  return data;
};

// Usage example
const pageIds = ["<your_copied_page_ids_from_maze_creator>"]
const spaceId = "<your_notion_space_id>";

pageIds.forEach(pageId => {
    makePagePublic(pageId, spaceId)
        .then(data => console.log(data))
        .catch(error => console.error(error));
});