from pydantic import BaseModel


class CodeModel(BaseModel):
    testing_code: str
    testing_code_depedencies: list[str]
    tesintg_code_dependencies_installation_command: str
    testing_code_execution_command: str