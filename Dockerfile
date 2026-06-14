# Step 1: Use an official lightweight Python image as the base
FROM python:3.11-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Install FastAPI and Pydantic directly inside the container
RUN pip install --no-cache-dir "fastapi[standard]" pydantic

# Step 4: Copy our main.py file from your Chromebook into the container
COPY main.py .

# Step 5: Tell the container to run our FastAPI server when it starts up
CMD ["fastapi", "run", "main.py", "--port", "8000"]