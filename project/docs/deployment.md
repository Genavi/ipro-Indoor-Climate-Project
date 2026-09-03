# Deployment Guide

## Prerequisites
Before deploying the application, ensure you have the following prerequisites in place:
- A DigitalOcean Droplet configured as per the [DigitalOcean Setup](digitalocean-setup.md) guide.
- SSH access to your DigitalOcean Droplet.
- Docker and Docker Compose installed on the Droplet (if not using the Docker image from the marketplace).
- The project codebase available on the Droplet (either via git clone or file transfer).
- Raspberry Pi and FeatherS3 devices set up and configured to send data to the MQTT broker.
- Tailscale set up for secure access to the Droplet (optional but recommended).
- Tailscale Auth Keys created for the DigitalOcean Droplet, Raspberry Pi, and FeatherS3 devices to connect to the Tailscale network.

## Deployment Steps

### Droplet Setup

1. **Connect to the Droplet**:
   SSH into your DigitalOcean Droplet using the provided credentials.

   ```console
   $ ssh -i /Users/davidringgenberg/.ssh/id_ed25519_digitalocean_indoorclimate 'root@159.89.5.63'
   ```

2. **Clone the Repository**:
   SSH into your DigitalOcean Droplet and clone the project repository. Make sure to initialize and update the submodules if you are using them.

   ```console
   $ cd /opt
   $ git clone git@gitlab.fhnw.ch:david.ringgenberg/ipro-indoor-climate-project.git
   $ cd ipro-indoor-climate-project
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the project directory on the Droplet and add the necessary environment variables. Use the provided `.env.example` file as a template.

4. **Create the Secret Files**:
    Since your project is in /opt/ipro-indoor-climate-project, you should create a dedicated directory for these sensitive files that is ignored by Git to ensure you never accidentally push your credentials to a repository.

    ```console
    # Create a hidden secrets folder
    mkdir -p /opt/ipro-indoor-climate-project/secrets
    chmod 700 /opt/ipro-indoor-climate-project/secrets

    # Create the password files
    echo "your_super_secret_db_password" > /opt/ipro-indoor-climate-project/secrets/db_password.txt
    echo "tskey-auth-your-tailscale-key" > /opt/ipro-indoor-climate-project/secrets/ts_authkey.txt

    # Secure the files so only root/docker can read them
    chmod 600 /opt/ipro-indoor-climate-project/secrets/*.txt
    ```

    > **Note**: Replace `your_super_secret_db_password` and `tskey-auth-your-tailscale-key` with your actual database password and Tailscale auth key, respectively. Ensure that the `.env` file references these files correctly.

5. **Configure Docker**:
   Ensure that the `docker-compose.yml` and `docker-compose.override.yml` files are correctly configured for the production environment. Update any necessary settings such as database credentials, MQTT broker address, and Grafana root URL. Make sure to set the `GF_SERVER_ROOT_URL` environment variable in the Grafana service to point to your Droplet's public IP or domain name.

6. **Build and Run the Application**:
    Use Docker Compose to build and run the application on the Droplet.
    
    ```console
    $ docker-compose up -d
    ```

7. **Verify the Deployment**:
    Check the status of the Docker containers to ensure they are running correctly.
    
    ```console
    $ docker-compose ps
    ```
    You can also check the logs for any errors or issues.
    
    ```console
    $ docker-compose logs -f
    ```

8. **Set Up Tailscale** (optional):
    If you are using Tailscale for secure access to your Droplet, ensure that the Tailscale service is running and properly configured. You can check the Tailscale status with:
    
    ```console
    $ docker-compose exec tailscale tailscale status
    ```

    Set up the Tailscale Proxy if you want to access Grafana securely via Tailscale.

    ```console
    $ docker-compose exec tailscale tailscale serve --https=443 http://localhost:3000                              
    https://iot-gateway.tail7a645b.ts.net (tailnet only)
    |-- / proxy http://localhost:3000
    ```

    > **Note**: Use `localhost:3000` instead of `grafana:3000` because Tailscale runs on the host network and cannot resolve Docker service names.

    To later make sure the Tailscale Proxy is running, you can check the status again:

    ```console
    $ docker-compose exec tailscale tailscale serve status                              
    https://iot-gateway.tail7a645b.ts.net (tailnet only)
    |-- / proxy http://localhost:3000
    ```

9. **Access the Application**:
    Once the application is deployed, you can access Grafana via the Droplet's public IP address or domain name (e.g., `http://your-droplet-ip:3000` or `https://iot-gateway.tail7a645b.ts.net` if using Tailscale). Log in with the default Grafana credentials (admin/admin) and change the password upon first login.

10. **Configure Grafana**:
    After logging into Grafana, you can set up your dashboards and data sources to visualize the sensor data being collected by the application.

    You can import pre-configured dashboards from the `project/monitoring/` directory or create your own custom dashboards based on your needs.

### Raspberry Pi and FeatherS3 Setup

1. **Connect to the Raspberry Pi**:
   SSH into your Raspberry Pi and ensure it is connected to the same network as your DigitalOcean Droplet or has access to the Tailscale network.

   > You can also use the Raspberry Pi Connect service to manage your Raspberry Pi remotely. https://connect.raspberrypi.com/devices

2. **Clone the Repository**:

   ```console
   $ cd /home/genavi/playground/fhnw/s1-ipro/
   $ git clone git@gitlab.fhnw.ch:david.ringgenberg/ipro-indoor-climate-project.git
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the project directory on the Droplet and add the necessary environment variables. Use the provided `.env.example` file as a template.

4. **Configure the MQTT Client**:
   Ensure that the Raspberry Pi and FeatherS3 devices are configured to send data to the MQTT broker running on the DigitalOcean Droplet. Update the MQTT client configuration files with the correct broker address, port, and authentication credentials.

5. **Setup a systemd services**:
   1. **Tailscale Service**:
      To ensure that the Tailscale service runs automatically on boot, create a systemd service file for the Raspberry Pi. This will allow the Tailscale service to start automatically when the device is powered.

      ```console
      $ sudo nano /etc/systemd/system/tailscale-autoconnect.service
      ```

      Example systemd service file (`/etc/systemd/system/tailscale-autoconnect.service`):

      ```ini
      [Unit]
      Description=Tailscale Auto Connect
      After=network-online.target tailscaled.service
      Wants=network-online.target
      Requires=tailscaled.service

      [Service]
      Type=oneshot
      ExecStart=/bin/sh -c 'tailscale up --authkey=$(cat /etc/tailscale/authkey) --reset --accept-routes'
      RemainAfterExit=yes

      [Install]
      WantedBy=multi-user.target
      ```

      Create a file to store the Tailscale auth key and set the appropriate permissions:

      ```console
      $ sudo nano /etc/tailscale/authkey
      $ sudo chmod 600 /etc/tailscale/authkey
      ```

      Restart the systemd daemon to apply the changes and run the service:

      ```console
      $ sudo systemctl daemon-reload
      $ sudo systemctl enable tailscale-autoconnect.service
      $ sudo systemctl start tailscale-autoconnect.service
      ```

      Check the status of the service to ensure it is running correctly:

      ```console
      $ sudo systemctl status tailscale-autoconnect.service
      ```

      > Troubleshooting: If the service fails to start, check the logs for any errors:
      >
      > ```console
      > $ journalctl -u tailscale-autoconnect.service -f
      > ```

   2. **IOT MQTT Bridge**:
      To ensure that the application runs automatically on boot, create a systemd service file for the Raspberry Pi. This will allow the application to start automatically when the device is powered.

      ```console
      $ sudo nano /etc/systemd/system/iot_mqtt_bridge.service
      ```

      Example systemd service file (`/etc/systemd/system/iot_mqtt_bridge.service`):

      ```ini
      [Unit]
      Description=USB Serial to MQTT Bridge
      After=network-online.target
      Wants=network-online.target

      [Service]
      Type=simple
      User=genavi
      WorkingDirectory=/home/genavi/playground/fhnw/s1-ipro/ipro-indoor-climate-project/project/
      Environment=PYTHONUNBUFFERED=1
      ExecStart=/home/genavi/playground/fhnw/s1-ipro/ipro-indoor-climate-project/project/venv/bin/python3 -m src.main
      Restart=on-failure
      RestartSec=10
      StandardOutput=journal
      StandardError=journal

      [Install]
      WantedBy=multi-user.target
      ```

      Restart the systemd daemon to apply the changes and run the service:

      ```console
      $ sudo systemctl daemon-reload
      $ sudo systemctl enable iot_mqtt_bridge.service
      $ sudo systemctl start iot_mqtt_bridge.service
      ```

      Check the status of the service to ensure it is running correctly:

      ```console
      $ sudo systemctl status iot_mqtt_bridge.service
      ```

      > Troubleshooting: If the service fails to start, check the logs for any errors:
      > 
      > ```console
      > $ journalctl -u iot_mqtt_bridge.service -f
      > ```

   