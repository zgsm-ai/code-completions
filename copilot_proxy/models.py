from typing import Optional, Union

from pydantic import BaseModel

import time


class EditorHideScore(BaseModel):
    is_whitespace_after_cursor: Optional[bool] = False
    prefix: Optional[str] = ""
    document_length: Optional[int] = 0
    prompt_end_pos: Optional[int] = 0

    previous_label: Optional[float] = 0.0
    previous_label_timestamp: Optional[int] = int(time.time() * 1000)


class PromptOptions(BaseModel):
    prefix: Optional[str] = ""
    suffix: Optional[str] = ""
    cursor_line_prefix: Optional[str] = ""
    cursor_line_suffix: Optional[str] = ""
    code_context: Optional[str] = ""


class CompletionContextAndIntention(BaseModel):
    language: Optional[str] = "python"
    is_single_completion: Optional[bool] = True
    prefix: Optional[str] = ""
    suffix: Optional[str] = ""
    cursor_line_prefix: Optional[str] = ""
    cursor_line_suffix: Optional[str] = ""
    st: Optional[float] = 0.0


class CompletionPostprocessorContext(BaseModel):
    language: Optional[str] = "python"
    completion_code: Optional[str]
    prefix: Optional[str]
    suffix: Optional[str]


class OpenAIinput(BaseModel):
    model: Optional[str]
    prompt: Optional[str]
    max_tokens: Optional[int] = 16
    temperature: Optional[float] = 0.6
    top_p: Optional[float] = 1.0
    n: Optional[int] = 1
    logprobs: Optional[int] = None
    stop: Optional[Union[str, list]] = []
    presence_penalty: Optional[float] = 0
    frequency_penalty: Optional[float] = 1
    best_of: Optional[int] = 1
    language_id: Optional[str]
    trigger_mode: Optional[str]
    file_project_path: Optional[str]
    calculate_hide_score: Optional[EditorHideScore] = EditorHideScore()
    user_id: Optional[str]
    repo: Optional[str]
    git_path: Optional[str] = ""
    prompt_options: Optional[PromptOptions] = None
    code_context_strategy: Optional[str] = ""


class CompletionRequest(OpenAIinput):
    parent_id: Optional[str] = None
    complete_id: Optional[str] = None
    is_fauxpilot_request: Optional[bool] = False
    api_key: Optional[str] = None
    authorization: Optional[str] = None
    client_id: Optional[str] = None
    file_project_path: Optional[str] = None
    project_path: Optional[str] = None
    import_content: Optional[str] = None
