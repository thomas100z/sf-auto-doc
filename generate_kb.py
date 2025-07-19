import typer
from rich.prompt import Prompt
from typing_extensions import Annotated

from agno.agent import Agent
from agno.vectordb.chroma import ChromaDb
from src.file_system_knowledge_base import FileSystemKnowledgeBase

app = typer.Typer()

@app.command()
def fill(
    sf_project_path: Annotated[str, typer.Option(help="Path to the Salesforce project to read files from.")] = "./",
    db_path: Annotated[str, typer.Option(help="Path to store the ChromaDB database.")] = "chroma_db",
    collection: Annotated[str, typer.Option(help="Name of the collection in ChromaDB.")] = "salesforce_kb"
):
    """Create and fill the knowledge base with summaries of the project files."""
    print(f"Creating knowledge base from: {sf_project_path}")
    knowledge_base = FileSystemKnowledgeBase(
        path=sf_project_path,
        vector_db=ChromaDb(collection=collection, path=db_path)
    )
    # The load method will read, summarize, embed, and store the files.
    knowledge_base.load(recreate=True)
    print("\nKnowledge base created successfully.")

@app.command()
def chat(
    db_path: Annotated[str, typer.Option(help="Path to the ChromaDB database.")] = "chroma_db",
    collection: Annotated[str, typer.Option(help="Name of the collection in ChromaDB.")] = "salesforce_kb"
):
    """Start an interactive chat session with the Salesforce agent."""
    print("Initializing Salesforce Chat Agent...")
    
    # The knowledge base is not loaded here, just configured for the agent to use.
    knowledge_base = FileSystemKnowledgeBase(
        path=".", # Path is not used for querying, but required by constructor
        vector_db=ChromaDb(collection=collection, path=db_path)
    )

    agent = Agent(
        knowledge_base=knowledge_base,
        show_tool_calls=True,
        debug_mode=True,
    )

    print("Agent initialized. Type 'exit' or 'quit' to end the chat.")
    while True:
        message = Prompt.ask("[bold]You[/bold]")
        if message.lower() in ['exit', 'quit']:
            print("Exiting chat. Goodbye!")
            break
        agent.print_response(message)

if __name__ == "__main__":
    app()