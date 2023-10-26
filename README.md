# Matching Algorithm Server for allocation-app

This server, built using FastAPI, is dedicated to processing allocation data and returning results using a specialized matching algorithm. It is designed exclusively to support the `allocation-app` project. A web platform for Student Project Allocation management.

### Why Separate Repo?
Due to specific package dependencies available only in Python, the matching algorithm couldn't be integrated directly into the NextJS app. Hence, this server acts as a bridge, ensuring seamless data processing without compromising on the tech stack's integrity.

### Tech Stack
- Python: The core language used for building the server and the matching algorithm.
- FastAPI: A modern, fast (high-performance), web framework for building APIs.
- Pydantic: Used for data validation and type annotations.
