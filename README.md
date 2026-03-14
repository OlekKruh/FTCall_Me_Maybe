# Call me maybe

*This project has been created as part of the 42 curriculum by ndemkiv, okruhlia.*

> [!WARNING]
> *The accuracy of the information or implementation may not correspond to reality.*
> ___USE AT YOUR OWN RISK!___


**Fabricated within the Data-Forges of:**

![Forge World Warsaw](https://img.shields.io/badge/Sector-42_Warsaw-b71c1c?style=for-the-badge&logo=42&logoColor=white)

**Sacred Tech-Stack (Lingua Technis):**

![Python](https://img.shields.io/badge/Lingua_Technis-Python_3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyCharm](https://img.shields.io/badge/Cogitator_Interface-PyCharm-000000?style=for-the-badge&logo=jetbrains&logoColor=white)

**Sustained by:**

![Recaf](https://img.shields.io/badge/Coffee_Stimulants-High_Grade-6F4E37?style=for-the-badge&logo=coffeescript&logoColor=white)
![&](https://img.shields.io/badge/-%26-gray?style=for-the-badge)
![Machine Spirit](https://img.shields.io/badge/Praise_the-Omnissiah-8B0000?style=for-the-badge&logo=warhammer&logoColor=white)

**Verification Rites:**

![Machine Spirit](https://img.shields.io/badge/Machine_Spirit-Appeased-success?style=for-the-badge&logo=robot-framework&logoColor=white)
> *"From the weakness of the mind, Omnissiah save us."*

### Description
**Call me maybe** is a specialized tool designed to explore **Function Calling** and **Constrained Decoding** in Large Language Models. The core of the project is a custom generation pipeline that forces the model to output strictly valid JSON, which is then parsed to execute local Python functions. It bridges the gap between natural language prompts and structured code execution.

### Instructions

**Prerequisites:** Python 3.12 or newer.

**Installation & Execution:**
We use a Makefile to automate the setup process. All dependencies and the virtual environment are kept local to the project folder.

1. Install dependencies and setup the virtual environment:
**make install**

2. Run the application:
**make run**
(Note: On the first run, the model weights will be downloaded to the local .model_cache directory).

**Other Commands:**
* **make lint** - Runs flake8 and mypy to check code quality and type annotations.
* **make clean** - Removes temporary files and clears the output directory.
* **make dell** - Total Purge: Removes the virtual environment and all downloaded LLM weights.

### Logic & Implementation

**Constrained Greedy Search:**
Instead of using standard generation methods, we implemented a manual token-by-token loop:
* **Greedy Selection:** The algorithm selects the token with the highest logit at each step.
* **JSON Integrity:** A bracket-counting mechanism monitors the output, ensuring the model stops exactly when the JSON object is structurally complete.
* **Singleton Manager:** The LLM is managed via a Singleton pattern to ensure it is loaded into memory only once.

**Function Execution:**
The system maps model outputs to a set of predefined tools:
* Math: fn_add_numbers, fn_get_square_root.
* Strings: fn_reverse_string, fn_substitute_string_with_regex.

### Project Structure
* main.py - Main entry point and orchestration.
* constrained_greedy.py - LLM interaction and custom decoding logic.
* parser.py - Input validation using Pydantic RootModels.
* func.py - Reusable tool library.
* llm_sdk/ - Local SDK for model interaction.

### Resources

**AI Usage:**
Generative AI was used as a pair-programming tool to:
* Optimize the Greedy Search loop and logit processing.
* Refactor type hints for strict mypy compliance.
* Configure Poetry for local package management.
All AI-generated logic was thoroughly reviewed and integrated into the project architecture.

**References:**
* 42 Project Subject: Call me maybe.
* Hugging Face: Tokenizer and Logits processing documentation.
* Pydantic V2: Official documentation.