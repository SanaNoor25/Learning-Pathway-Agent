from typing import Dict, Any


ROLE_CATALOG: Dict[str, Dict[str, Any]] = {
    "data_scientist": {
        "role_name": "Data Scientist",
        "description": "Builds ML models and extracts insights from data.",
        "required_skills": ["python", "statistics", "machine learning", "sql"],
        "priority_skills": ["machine learning", "python"],
        "prerequisites": ["basic python", "math fundamentals"],
        "interview_focus": ["ml concepts", "case studies", "sql queries"],
        "suggested_projects": [
            "Customer churn prediction model",
            "Sales forecasting system"
        ]
    },

    "data_analyst": {
        "role_name": "Data Analyst",
        "description": "Analyzes datasets to generate business insights.",
        "required_skills": ["excel", "sql", "power bi", "python"],
        "priority_skills": ["sql", "excel"],
        "prerequisites": ["basic statistics"],
        "interview_focus": ["sql queries", "data visualization"],
        "suggested_projects": [
            "Sales dashboard",
            "Business KPI tracker"
        ]
    },

    "machine_learning_engineer": {
        "role_name": "Machine Learning Engineer",
        "description": "Builds and deploys ML systems at scale.",
        "required_skills": ["python", "ml", "docker", "mlops"],
        "priority_skills": ["mlops", "deployment"],
        "prerequisites": ["python", "machine learning basics"],
        "interview_focus": ["system design", "ml pipelines"],
        "suggested_projects": [
            "ML API deployment system",
            "Recommendation engine"
        ]
    }
}


def get_role_catalog_entry(target_role: str) -> Dict[str, Any]:
    """
    Normalize and fetch role from catalog.
    """
    if not target_role:
        return {"error": "No role provided"}

    key = target_role.strip().lower().replace(" ", "_")

    return ROLE_CATALOG.get(key, {
        "error": f"Role '{target_role}' not found in catalog",
        "available_roles": list(ROLE_CATALOG.keys())
    })