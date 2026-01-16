# Getting Started
This section provides instructions to set up the development environment for the Indoor Climate Project. Focus on Linux and macOS systems. Windows users may need to adapt some commands accordingly.

## Prerequisites

Ensure you have the following installed on your system:
- git
- Python 3.8 or higher
- pip/pip3 (package manager for Python)
- virtualenv (optional but recommended)
- Docker and Docker Compose (or Colima for macOS users)

## Setting Up the Development Environment
1. **Create a Virtual Environment** (optional but recommended):

    ```console
    $ python3 -m venv venv
    $ source venv/bin/activate
    ```

2. **Install Dependencies**:
    Install the required Python packages using pip.

    ```console
    $ pip3 install --upgrade pip3
    $ pip3 install -e .
    ```

3. **Initialize Submodules** (optional):
    If you are working with the template submodules, initialize and update them.

    ```console
    $ git submodule update --init --recursive
    ```

4. **Update Environment Variables**:
    Set any necessary environment variables as specified in the project documentation.

    You can use the provided `/project/.env.example` file as a template. 
    Create a `.env` file in the `project/` directory and add your database credentials.
    > If you are using Colima, use the Colima Gateway IP as `DATABASE_HOST`.

5. **Update Docker Configuration** (optional):

    Update the `docker-compose.override.yml` file in the `project/` directory if you need to customize the Postgres or Grafana settings. You can use the provided example file `/project/docker-compose.override.yml.example` as a template. Database credentials are set via environment variables.

6. **Initialize Database Schema**:
    Run the database migrations to set up the initial schema.

    ```console
    # Check if database is reachable
    $ alembic current

    # Run migrations to set up the database schema
    $ alembic upgrade head
    ```

## Running the Development Environment

1. Colima setup (only if you use Colima as Docker backend):
    ```console
    $ colima start --network-address
    $ colima status
    ```

2. Use Docker Compose to start the services:
    ```console
    $ cd project
    $ docker compose up -d

    # Make sure the services are running
    $ docker ps
    CONTAINER ID   IMAGE                               COMMAND                  CREATED          STATUS          PORTS                                         NAMES
    contains_id   grafana/grafana                     "/run.sh"                2 minutes ago   Up 2 minutes   0.0.0.0:3000->3000/tcp, [::]:3000->3000/tcp   grafana
    contains_id   timescale/timescaledb:latest-pg15   "docker-entrypoint.s…"   2 minutes ago   Up 2 minutes   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp   postgres

    # Execute database commands inside the Postgres container
    $ docker exec -it <container_name> psql -U <your_db_user> -d <your_db_name>
    $ docker exec -it <container_name> psql -U <your_db_user> -d <your_db_name> -c "SELECT * FROM your_table_name;"
    $ docker exec -it <container_name> psql -U <your_db_user> -d <your_db_name> -c "\d your_table_name"
    ```

    To stop the services, run:
    ```console
    $ docker compose down
    docker compose down -v  # remove volumes as well (don't do this if you want to keep your database data)
    ```

3. Run the Data Logger:
    ```console
    $ python3 src/main.py
    ```
    This will automatically:
    - Verify the database schema is up to date.
    - Connect to the serial port specified in the `.env` file.
    - Start reading data from the micro:bit and inserting it into the TimescaleDB database.
    


## Access Services:

- **Grafana**: Open your web browser and navigate to `http://localhost:3000`. Log in with the defaultcredentials (admin/admin) and change the password when prompted.
  - colima: `http://colima_gateway_ip:3000`
- **Postgres**: Connect using your preferred database client with the credentials you set in the `.env`file. Default port is `5432`.
- **TimescaleDB**: To verify the TimescaleDB Hypertable setup, you can run the following SQL command in your Postgres client:
    ```console
    $ docker exec -it postgres psql -U admin -d sensor_data -c "SELECT * from timescaledb_information.hypertables;"
    ```

If default ports don't work, check the port mappings in the `docker-compose.yml` file. Or use `docker ps` to see the actual port mappings.
    
