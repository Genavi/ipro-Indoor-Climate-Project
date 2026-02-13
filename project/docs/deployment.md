# Deployment Guide

## Prerequisites
Before deploying the application, ensure you have the following prerequisites in place:
- A DigitalOcean Droplet configured as per the [DigitalOcean Setup](digitalocean-setup.md) guide.
- SSH access to your DigitalOcean Droplet.
- Docker and Docker Compose installed on the Droplet (if not using the Docker image from the marketplace).
- The project codebase available on the Droplet (either via git clone or file transfer).
- Raspberry Pi and FeatherS3 devices set up and configured to send data to the MQTT broker.

## Deployment Steps
1. **Clone the Repository**:
   SSH into your DigitalOcean Droplet and clone the project repository. Make sure to initialize and update the submodules if you are using them.

   ```console
   $ git clone <repository_url>
   $ cd <repository_directory>
   $ git submodule update --init --recursive
   ```
2. **Set Up Environment Variables**:
   Create a `.env` file in the project directory on the Droplet and add the necessary environment variables as specified in the [Getting Started Guide](getting-started.md). Use the provided `.env.example` file as a template.

3. **Configure Docker**:
   Ensure that the `docker-compose.yml` and `docker-compose.override.yml` files are correctly configured for the production environment. Update any necessary settings such as database credentials, MQTT broker address, and Grafana root URL. Make sure to set the `GF_SERVER_ROOT_URL` environment variable in the Grafana service to point to your Droplet's public IP or domain name.

4. **Build and Run the Application**:
    Use Docker Compose to build and run the application on the Droplet.
    
    ```console
    $ docker-compose up -d
    ```

5. **Verify the Deployment**:
    Check the status of the Docker containers to ensure they are running correctly.
    
    ```console
    $ docker-compose ps
    ```
    You can also check the logs for any errors or issues.
    
    ```console
    $ docker-compose logs -f
    ```

6. **Set Up Tailscale** (optional):
    If you are using Tailscale for secure access to your Droplet, ensure that the Tailscale service is running and properly configured. You can check the Tailscale status with:
    
    ```console
    $ docker-compose exec tailscale tailscale status
    ```

    Set up the Tailscale Proxy if you want to access Grafana securely via Tailscale.

    ```
    $ docker-compose exec tailscale tailscale serve --https=443 http://grafana:3000                              
    https://iot-gateway.tail7a645b.ts.net (tailnet only)
    |-- / proxy http://grafana:3000
    ```

    To later make sure the Tailscale Proxy is running, you can check the status again:

    ```console
    $ docker-compose exec tailscale tailscale serve status                              
    https://iot-gateway.tail7a645b.ts.net (tailnet only)
    |-- / proxy http://grafana:3000
    ```

7. **Access the Application**:
    Once the application is deployed, you can access Grafana via the Droplet's public IP address or domain name (e.g., `http://your-droplet-ip:3000` or `https://iot-gateway.tail7a645b.ts.net` if using Tailscale). Log in with the default Grafana credentials (admin/admin) and change the password upon first login.

8. **Configure Grafana**:
    After logging into Grafana, you can set up your dashboards and data sources to visualize the sensor data being collected by the application.

    You can import pre-configured dashboards from the `project/monitoring/` directory or create your own custom dashboards based on your needs.

