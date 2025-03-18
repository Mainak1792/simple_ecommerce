# Use a lightweight Nginx image
FROM nginx:alpine

# Copy our static files to the default Nginx public folder
COPY . /usr/share/nginx/html

# Expose port 80 in the container
EXPOSE 5000

# Use the default Nginx startup command
