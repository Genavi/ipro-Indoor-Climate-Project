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

## Running the Development Environment

1. **Colima setup** (only if you use Colima as Docker backend):
    ```console
    $ colima start --network-address
    $ colima status
    ```

2. **Start the services**:
    ```console
    $ cd project
    $ docker compose up -d

    # Make sure the services are running
    $ docker ps
    CONTAINER ID   IMAGE                               COMMAND                  CREATED          STATUS          PORTS                                         NAMES
    contains_id   grafana/grafana                     "/run.sh"                2 minutes ago   Up 2 minutes   0.0.0.0:3000->3000/tcp, [::]:3000->3000/tcp   grafana
    contains_id   timescale/timescaledb:latest-pg15   "docker-entrypoint.s…"   2 minutes ago   Up 2 minutes   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp   postgres
    ```
    Some useful commands to check logs and access the database (not needed for initial setup):
    ```console
    # Check logs for Postgres and Grafana
    $ docker compose logs -f postgres
    $ docker compose logs -f grafana
    
    # Execute database commands inside the Postgres container
    $ docker exec -it <container_name> psql -U <your_db_user> -d <your_db_name>
    $ docker exec -it <container_name> psql -U <your_db_user> -d <your_db_name> -c "SELECT * FROM your_table_name;"
    $ docker exec -it <container_name> psql -U <your_db_user> -d <your_db_name> -c "\d your_table_name"

    # Stop the services
    $ docker compose down
    $ docker compose down -v  # removes all volumes as well (don't do this if you want to keep your database data)
    ```

3. **Initialize Database Schema**:
    Run the database migrations to set up the initial schema.

    ```console
    # Check if database is reachable
    $ alembic current
    INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
    INFO  [alembic.runtime.migration] Will assume transactional DDL.

    # Run migrations to set up the database schema
    $ alembic upgrade head
    INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
    INFO  [alembic.runtime.migration] Will assume transactional DDL.
    INFO  [alembic.runtime.migration] Running upgrade  -> 63b5248db74e, initial migration
    ```

4. Run the Data Logger:
    ```console
    $ python3 src/main.py
    ```
    This will automatically:
    - Verify the database schema is up to date.
    - Connect to the serial port specified in the `.env` file.
    - Start reading data from the micro:bit and inserting it into the TimescaleDB database.

## Setup Grafana Dashboard
1. Open Grafana in your web browser at `http://localhost:3000` (or `http://colima_gateway_ip:3000` if using Colima).
2. Log in with the default credentials (admin/admin) and change the password when prompted.
3. Add a new data source:
   - Go to Configuration > Data Sources > Add data source.
   - Select "PostgreSQL" as the data source type.
   - Configure the data source with the following settings:
     - Host: `host.docker.internal:5432` (or `colima_gateway_ip:5432` if using Colima)
     - Database: `sensor_data`
     - User: your database user (from `.env` file)
     - Password: your database password (from `.env` file)
     - SSL Mode: Disabled
     - TimescaleDB: Enabled
   - Click "Save & Test" to verify the connection.
4. Import the provided Grafana dashboard JSON file:
   - Go to Create > Import.
   - Upload the `src/monitoring/grafana-indoor-climate-dashboard.json` file from the project repository.
   - Select the PostgreSQL data source you just created.
   - Click "Import" to add the dashboard.

## Access Services:

- **Grafana**: Open your web browser and navigate to `http://localhost:3000`. Log in with the defaultcredentials (admin/admin) and change the password when prompted.
  - colima: `http://colima_gateway_ip:3000`
- **Postgres**: Connect using your preferred database client with the credentials you set in the `.env`file. Default port is `5432`.
- **TimescaleDB**: To verify the TimescaleDB Hypertable setup, you can run the following SQL command in your Postgres client:
    ```console
    $ docker exec -it postgres psql -U admin -d sensor_data -c "SELECT * from timescaledb_information.hypertables;"
    ```

If default ports don't work, check the port mappings in the `docker-compose.yml` file. Or use `docker ps` to see the actual port mappings.
    
