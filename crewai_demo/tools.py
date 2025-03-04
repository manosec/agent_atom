from crewai.tools import BaseTool

def store_code_locally(code_snippet: str, language: str, file_name: str = None) -> str:
    """
    Saves the provided code snippet into a file with the correct file extension based on its programming language.
    
    Args:
        code_snippet (str): The code to be stored.
        language (str): The programming language of the code (e.g., 'python', 'bash', 'javascript').
        file_name (str, optional): The base name for the file (without extension). Defaults to 'artifact'.
    
    Returns:
        str: A confirmation message including the full file name.
        
    Raises:
        ValueError: If the language is not supported.
    """
    # Mapping of languages to their file extensions
    ext_mapping = {
        "python": ".py",
        "bash": ".sh",
        "javascript": ".js",
        "java": ".java",
        "c++": ".cpp",
        "c": ".c",
        "ruby": ".rb",
        "go": ".go",
        # Add more mappings as needed
    }
    
    # Normalize language input
    language_lower = language.lower()
    extension = ext_mapping.get(language_lower)
    
    if not extension:
        raise ValueError(f"Unsupported language: {language}")
    
    if not file_name:
        file_name = "artifact"
    
    # Construct the full file name
    file_path = file_name + extension
    
    # Write the code snippet to the file
    with open(file_path, "w") as file:
        file.write(code_snippet)
    
    return f"File {file_path} created successfully."


class StoreTool(BaseTool):
    name: str = "Testcase Store"
    description:str = "Used to store the generated testscript to a file"

    def _run(self, code_snippet, language, file_name):
        store_code_locally(code_snippet=code_snippet, language=language, file_name=file_name)


store_tool = StoreTool()