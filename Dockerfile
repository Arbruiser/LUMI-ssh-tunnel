# A lightweight, official Python image
FROM python:3.11-slim

# Create /app directory inside the container
WORKDIR /app

# Install basic system tools and remove remporary installation files
RUN apt-get update && apt-get install -y \
    git \
    curl \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*


# Create a Python virtual environment and add it to the system PATH
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install the OpenAI package
RUN pip install --no-cache-dir openai

# Install the OpenCode AI terminal agent
RUN curl -fsSL https://opencode.ai/install | bash

# Keep the container running in the background
CMD ["tail", "-f", "/dev/null"]
