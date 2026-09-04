# Exoplanet Explorer

Explore thousands of worlds beyond our solar system through data and AI.

Exoplanet Explorer is a full stack data and AI platform for exploring more than 5,600 NASA exoplanets. It combines a custom ELT pipeline, cloud data warehouse, semantic retrieval, and locally hosted language models to make complex astronomical data easier to explore through natural language.

🌐 https://exoplanetexplorer.space/


## What is Exoplanet Explorer?

NASA has collected an incredible amount of information about planets outside our solar system, but exploring that data usually means working through large datasets and understanding dozens of scientific attributes.

I wanted to make that experience a little more intuitive.

Exoplanet Explorer lets users ask questions about exoplanets in natural language and receive answers grounded in real astronomical data.

Questions can range from:

"What are some Earth sized planets?"

to

"Which discovered planets are most similar to Earth in temperature and size?"

Behind the interface is a complete data pipeline that collects, transforms, stores, retrieves, and analyzes exoplanet data before passing relevant context to the language model.


## Architecture

NASA Exoplanet Data
        ↓
      Airbyte
        ↓
    Snowflake
        ↓
       dbt
        ↓
Cleaned Exoplanet Dataset
        ↓
      FAISS
        ↓
Semantic Context Retrieval
        ↓
 Ollama + Gemma
        ↓
     FastAPI
        ↓
 React Interface


## Data Pipeline

The project uses a custom ELT pipeline to turn raw astronomical observations into data that can be queried and analyzed.

**Airbyte**

Handles ingestion of source exoplanet data into the analytical environment.

**Snowflake**

Acts as the central data warehouse for storing and querying thousands of exoplanet observations.

**dbt**

Transforms and structures raw records into clean analytical datasets used by the application.

**FAISS**

Creates a semantic retrieval layer over the processed data so relevant planets and attributes can be identified from natural language questions.


## AI Retrieval

Rather than asking a language model to answer questions from memory, Exoplanet Explorer retrieves relevant information from the underlying exoplanet dataset first.

The retrieved context is then passed to a locally hosted Gemma model through Ollama.

This gives the application a simple RAG workflow:

User Question  
↓  
Semantic Search  
↓  
Relevant Exoplanet Data  
↓  
Language Model  
↓  
Grounded Response


## Local AI Inference

One of my favorite parts of the project was experimenting with running the model locally instead of relying entirely on external model APIs.

The language model is served using **Ollama**, with inference running on separate hardware and connected to the application through **Tailscale**.

This architecture reduced model latency by approximately **83%**, bringing responses to **under 500 ms** while keeping inference under my control.


## Tech Stack

**Data**

Airbyte  
Snowflake  
dbt  
FAISS  
MySQL

**Backend**

Python  
FastAPI  
Ollama  
Gemma  
Tailscale

**Frontend**

React  
Tailwind CSS

**Infrastructure**

Docker  
Local model inference


## Features

* Explore data for more than **5,600 NASA exoplanets**
* Ask questions about exoplanets using natural language
* Retrieve answers grounded in real astronomical data
* Search across planetary and stellar characteristics
* Semantic retrieval using FAISS
* Locally hosted language model inference
* Interactive web interface for exploring discoveries
* End to end ELT pipeline for preparing analytical data


## API

The FastAPI backend exposes the retrieval and inference pipeline through the `/ask` endpoint.

A request is passed through semantic retrieval before relevant exoplanet context is supplied to the language model.

This keeps the frontend separated from the underlying retrieval and inference infrastructure.


## Why I Built It

I have always liked projects where data engineering, machine learning, and product development meet.

Exoplanet Explorer started as a way to experiment with astronomical data and gradually turned into a much larger question:

**What would it look like if exploring scientific datasets felt more like having a conversation?**

Building it gave me the chance to work across the entire stack, from ingestion and transformation to vector search, model inference, APIs, and the final interface.


## Project Highlights

**5,600+**
NASA exoplanets processed

**Custom ELT Pipeline**
Airbyte + Snowflake + dbt

**RAG**
FAISS powered semantic retrieval

**Local AI**
Ollama + Gemma

**83%**
reduction in inference latency

**<500 ms**
response latency with local inference


## Built By

**Jeet Mehta**

Interested in data, machine learning, and building systems that make complicated information easier to understand.
