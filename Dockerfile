# Python's base image
FROM python:3.12-slim 

# # Setting Working Directory inside my Container
WORKDIR /app

# # Copy Dependency List
COPY requirements.txt .

# # Install Python Packages
RUN pip install -r requirements.txt

# # Copying all the code into the image
COPY . .

# # Starting your app
# # CMD ["fastapi","dev","app.py"] this wont work because Fastapi itself is not a command-line tool
CMD ["uvicorn", "predictor.app:app", "--host", "0.0.0.0", "--port", "8000"]

