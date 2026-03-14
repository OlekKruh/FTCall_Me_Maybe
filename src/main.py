import os
import sys
import func
import time
import json
from typing import Any
from colors import GREEN, BOLD, RESET, YELLOW, RED
from constrained_greedy import constrained_search
from parser import pars_function_def, parse_query_file


def show_total_proces_time(start_time: float) -> None:
    """Calculates and prints the total execution time.

    Args:
        start_time: The time.perf_counter() value when processing started.
    """
    total_seconds = time.perf_counter() - start_time
    minutes, seconds = divmod(int(total_seconds), 60)
    time_str = f"{minutes:02d}:{seconds:02d}"
    print(f"{YELLOW}Total time: {BOLD}{time_str}{RESET}")


def func_test_run(result_json: list[dict[str, Any]],
                  tools_map: dict[str, Any]) -> None:
    """Executes functions based on the model's predictions.

    Iterates through the list of function calls, validates their existence
    in the tools map, and executes them with the provided parameters.
    Results are stored directly in the result_json list.

    Args:
        result_json: A list of dictionaries containing predicted
        function names and their parameters.
        tools_map: A dictionary mapping function name strings to actual
            callable Python functions.
    """
    print(f"\n{GREEN}Executing functions...{RESET}")
    for item in result_json:
        # prompt = item.get("prompt")
        fn_name = item.get("name")
        fn_params = item.get("parameters")

        if (isinstance(fn_name, str) and
                fn_name in tools_map and
                isinstance(fn_params, dict)):
            try:
                result = tools_map[fn_name](**fn_params)
                item["execution_resalt"] = result
                print(f"{GREEN}✓{RESET} {fn_name}\n"
                      f"-> {GREEN}{result}{RESET}\n")

            except Exception as e:
                item["execution_resalt"] = f"Error: {e}"
                print(f"{RED}❌ {fn_name}: {e}{RESET}")
        else:
            item["execution_result"] = ("Skip: "
                                        "Function not found or invalid params")


def main() -> None:
    """Main entry point of the LLM Function Calling pipeline.

    Initializes data paths, loads function definitions and user queries,
    manages the constrained generation loop, and saves final results to JSON.
    """
    query_path = "data/input/function_calling_tests.json"
    def_path = "data/input/functions_definition.json"
    output_dir = "data/output"
    output_file = os.path.join(output_dir, "result.json")

    tools_map: dict[str, Any] = {
        "fn_add_numbers":
            func.fn_add_numbers,
        "fn_greet":
            func.fn_greet,
        "fn_reverse_string":
            func.fn_reverse_string,
        "fn_get_square_root":
            func.fn_get_square_root,
        "fn_substitute_string_with_regex":
            func.fn_substitute_string_with_regex
    }

    query_list = parse_query_file(query_path)
    f_def = pars_function_def(def_path)

    if f_def is None or query_list is None:
        print("Abort program cycle. Check yours file.")
        sys.exit(1)

    system_prompt = f"""
    Available tools: {f_def}.
    JSON Schema to follow:
    {{
    "prompt": "User input",
    "name": "function_name",
    "parameters": {{ "key": "value" }}
    }}
    """

    start_time = time.perf_counter()
    result_json: list[dict[str, Any]] = []
    for item in query_list:
        user_query = item["prompt"]

        sys_prompt = (f"{system_prompt}\n"
                      f"User query: {user_query}\n"
                      f"Output:")

        raw_response = constrained_search(sys_prompt, user_query)

        try:
            model_data = json.loads(raw_response)

            result_entry = {
                "prompt": model_data.get("prompt"),
                "name": model_data.get("name"),
                "parameters": model_data.get("parameters")
            }
            result_json.append(result_entry)

        except json.JSONDecodeError:
            print(f"Error parsing JSON for query: {user_query}")

    func_test_run(result_json, tools_map)

    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result_json, f, indent=4, ensure_ascii=False)
    print(f"\n{GREEN}Results saved to {output_file}{RESET}")
    show_total_proces_time(start_time)


if __name__ == "__main__":
    main()
