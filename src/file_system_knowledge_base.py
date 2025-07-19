

import os
from typing import Iterator, List, Dict

from agno.knowledge.base import KnowledgeBase
from agno.llms.openai import OpenAI
from agno.schema import Document

class FileSystemKnowledgeBase(KnowledgeBase):
    """Knowledge base for reading and summarizing files from a local directory."""

    def __init__(self, path: str, **kwargs):
        super().__init__(**kwargs)
        if not os.path.isdir(path):
            raise ValueError(f"Path provided is not a valid directory: {path}")
        self.path = path
        self.llm = OpenAI(model="gpt-3.5-turbo")
        self.summarization_prompt = (
            "You are a highly skilled software engineer providing a concise summary of a file from a Salesforce project. "
            "Focus on the file's primary purpose, its key functions, and how it interacts with other parts of the system. "
            "The summary should be dense with information and no more than 3-4 sentences."
        )

    def _summarize_content(self, file_path: str, file_content: str) -> str:
        """Uses an LLM to summarize the content of a single file."""
        print(f"Summarizing: {file_path}")
        try:
            response = self.llm.get_chat_response(
                messages=[
                    {"role": "system", "content": self.summarization_prompt},
                    {
                        "role": "user",
                        "content": f"Summarize the file `{file_path}` with the following content:\n\n```\n{file_content}\n```"
                    }
                ]
            )
            return response.strip()
        except Exception as e:
            print(f"Error summarizing {file_path}: {e}")
            return ""

    def reader(self) -> Iterator[Document]:
        """Reads files from the directory and yields them as Documents for processing."""
        for root, _, files in os.walk(self.path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # The document content will be the summary, not the raw file.
                    summary = self._summarize_content(file_path, content)
                    if not summary:
                        continue

                    yield Document(
                        name=file_path,  # Use file path as the document name
                        content=summary, # The summary is what gets embedded
                        meta_data={
                            "file_path": file_path,
                            "original_content": content
                        }
                    )
                except Exception as e:
                    print(f"Could not read or process file {file_path}: {e}")

