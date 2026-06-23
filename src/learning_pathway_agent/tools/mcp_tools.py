from crewai.tools import tool
from src.learning_pathway_agent.data.role_catalog import get_role_catalog_entry


@tool("get_role_data")
def get_role_data(role: str):
    """Fetch role data from MCP Role Catalog"""
    return get_role_catalog_entry(role)


@tool("get_learning_resources")
def get_learning_resources(skill: str):
    """Fetch learning resources from MCP Resource Catalog"""
    return {
        "skill": skill,
        "resources": [
            {
                "name": f"Intro to {skill}",
                "type": "course",
                "difficulty": "beginner",
                "duration": "2-4 hours",
                "url": None,
            }
        ],
    }


@tool("web_search_ddgs")
def web_search(query: str):
    """Search internet using DDGS MCP"""
    return f"[WEB SEARCH PLACEHOLDER for {query}]"
