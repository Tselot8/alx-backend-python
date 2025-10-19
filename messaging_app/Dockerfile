FROM python:3.10

# Set working directory
WORKDIR /app

# Copy only requirements first
COPY requirements.txt .

COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django project files into container
COPY manage.py .
COPY messaging_app/ ./messaging_app/
COPY chats/ ./chats/

# Expose port
EXPOSE 8000

# Run the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
