from mcp.server import FastMCP
import requests
import json

app = FastMCP('my_todos')

@app.tool()
async def get_todos(id: str = "") -> str:
    """
    Get todos from JSONPlaceholder API

    Args:
        id: Optional todo item ID. If not provided, returns all todos.

    Returns:
        JSON string with todo details
    """
    try:
        if id is not None:
            url = f"https://jsonplaceholder.typicode.com/todos/{id}"
        else:
            url = "https://jsonplaceholder.typicode.com/todos"
        
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        return json.dumps(response.json(), indent=2)
    
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"Request failed: {str(e)}"})
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"JSON decode failed: {str(e)}"})

if __name__ == '__main__':
    app.run(transport='stdio')
 