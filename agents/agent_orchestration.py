from crewai import Agent, Crew, Task
import sqlite3

def fetch_for_agent(db_path="photos.db"):
    # Gather a summary for the agent
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT event_tag, COUNT(*) FROM events GROUP BY event_tag ORDER BY COUNT(*) DESC")
    events_summary = cursor.fetchall()
    cursor.execute("SELECT path FROM photos")
    paths = cursor.fetchall()
    conn.close()
    return events_summary, [p[0] for p in paths]

# Initialize your agent
llm_agent = Agent(
    name="Photo Organizer",
    role="Group photos by events and people using database info, and suggest organization schemes.",
    goal="Automate the intelligent organization of local photos by important milestones, people, or timeframes, providing actionable and user-friendly grouping suggestions.",
    backstory="This agent is designed to help users make sense of large, unsorted local photo collections using advanced AI and LLM reasoning. It leverages embeddings, event tags, and metadata for optimal grouping and organization.",
    llm="ollama/llama2",  # Or your actual Ollama model name
)

# Example task for the agent
def suggest_groups():
    events_summary, paths = fetch_for_agent("photos.db")
    event_str = "\n".join([f"{tag}: {count}" for tag, count in events_summary])
    task = Task(
    description=f"""You are a smart agent for a photo organizer system.
    Below is a summary of event tags and their frequencies:\n{event_str}\n
    Generate action recommendations for grouping the photos into folders or albums by their event type or important milestones.
    Also suggest ideas for grouping people if provided face clustering results.""",
    expected_output="A clear, structured list of recommended photo groups or albums by milestone/event and/or by individual, with short explanations for each suggestion. Optionally add instructions for further user actions.",
    agent=llm_agent
    )

    crew = Crew(tasks=[task])
    result = crew.kickoff()
    print("Agent Suggestions:")
    print(result)

if __name__ == "__main__":
    suggest_groups()
