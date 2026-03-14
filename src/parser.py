from pydantic import BaseModel, ValidationError, RootModel
from typing import Dict, List, Optional, Any, cast


class TestItem(BaseModel):
    """Schema for a single test prompt."""
    prompt: str


class TestList(RootModel):
    """List of test items for root validation."""
    root: List[TestItem]


class TypeInfo(BaseModel):
    """Schema for parameter or return type information."""
    type: str


class FunctionModel(BaseModel):
    """Detailed schema for a function definition."""
    name: str
    description: str
    parameters: Dict[str, TypeInfo]
    returns: TypeInfo


class FunctionsList(RootModel):
    """List of function definitions for root validation."""
    root: List[FunctionModel]


def parse_query_file(file_path: str) -> Optional[List[Dict[str, Any]]]:
    """Parses and validates a JSON file containing user queries.

    Args:
        file_path: Path to the JSON file with test prompts.

    Returns:
        A list of dictionaries containing validated prompts,
        or None if parsing/validation fails.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_data = f.read()
            validated_data = TestList.model_validate_json(raw_data)

            return cast(List[Dict[str, Any]], validated_data.model_dump())
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except ValidationError as e:
        print(f"File Validation Error {file_path}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None


def pars_function_def(file_path: str) -> Optional[List[Dict[str, Any]]]:
    """Parses and validates a JSON file containing function definitions.

    Args:
        file_path: Path to the JSON file with tool definitions.

    Returns:
        A list of dictionaries representing function schemas,
        or None if parsing/validation fails.
    """
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
            raw_data = f.read()

        validated_data = FunctionsList.model_validate_json(raw_data)
        return cast(List[Dict[str, Any]], validated_data.model_dump())

    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except ValidationError as e:
        print(f"Validation Error in {e}")
        print(e.json(indent=2))
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None
