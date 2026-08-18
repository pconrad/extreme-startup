# First we compile the node stuff
FROM node:19-alpine AS node-build
COPY ./frontend ./frontend
WORKDIR /frontend

# Clean install all packages from package-lock.json, then build
RUN npm ci
RUN npm run build

# Then we run the python stuff
FROM python:3.11-bookworm
COPY ./flaskr ./flaskr

# Copy pre-compiled node stuff
COPY --from=node-build ./frontend/dist ./flaskr/vite

# Install reqs
RUN pip install --upgrade pip
RUN pip install -r flaskr/requirements.txt

# Set env variables
ENV DB_USERNAME=xs-bot
ENV DB_ADDRESS=cluster0.dvvipyf.mongodb.net

EXPOSE 5000
EXPOSE 80

CMD ["python", "-m", "flask", "--app", "flaskr", "--debug", "run", "--host", "0.0.0.0", "--port", "80"]
