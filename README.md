# PhotoMind Agent

## Create a virtual environment

Create the virtual environment: Execute the python -m venv command followed by the desired name for your virtual environment. A common practice is to name it venv or env. 
Code

    python -m venv venv

## To activate virtual environment

This command will create a new directory (e.g., venv) within your project folder, containing a self-contained Python installation and its associated packages.
Activate the virtual environment:
On Windows:
Code

        .\venv\Scripts\activate
On macOS/Linux.
Code

        source venv/bin/activate

## Install the dependencies

Run the below command

Code

        pip install -r requirements.txt

## Create a environment file (.env) and the API keys

1. create .env file
2. Add the API Keys


### Flow

#### Module 1: Photo Ingestion (ingest/photo_ingest.py)
#### Module 2: Vision Analysis (vision/photo_vision.py)
##### A. Face Detection & Embedding Extraction
We’ll use InsightFace or Dlib for face detection and feature vector extraction.
##### B. Event/Milestone Extraction
For event grouping, use CLIP or similar model to generate captions or tags per photo.
#### Step 4: Metadata Database Module
We'll store all the extracted metadata (photo_meta.json, face_meta.json, event_tags.json) in a local database to make querying, grouping, and integration easier for agents.
#### Step 5: Agent Orchestration (Ollama + CrewAI)
Goal: Connect your local database with intelligent agents capable of reasoning (using Ollama and CrewAI).

agents/agent_orchestration.py: Use CrewAI to define agent roles, workflows, and interactions.
#### Step 5: Agent Orchestration, where you’ll connect Ollama with CrewAI to create intelligent agents that analyze your database

