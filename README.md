<div align='center'>
 <h1>
  ipro: Indoor Climate Project
 </h1>
 
 <!--<p>
  <a href="https://github.com/badges/shields/actions/workflows/daily-tests.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/badges/shields/daily-tests.yml?label=daily%20tests" alt="Daily Tests Status">
  </a>
  <a href="https://coveralls.io/github/badges/shields">
    <img src="https://img.shields.io/coveralls/github/badges/shields"alt="Code Coverage"></a>
 </p>-->

 <kbd><img src="./project/docs/images/grafana-dashboard_v1.png" width="600" /></kbd>

 <p>
  This repository contains the code and resources for the Indoor Climate Project (ipro).
 </p>

 <p>
  Check the <a href='#'>Demo</a> (planned).
 </p>

 <h2>Technologies Used</h2>

 <h4>Programming Languages & Frameworks</h4>

 <p>
  <a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" /></a>
  <a href="https://micropython.org/"><img alt="MicroPython" src="https://img.shields.io/badge/MicroPython-2D2D2D?style=for-the-badge&logo=micropython&logoColor=white" /></a>
  <a href="https://docs.docker.com/compose/"><img alt="Docker Compose" src="https://img.shields.io/badge/Docker%20Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" /></a>
 </p>

 <h4>Visualisation</h4>

 <p>
  <a href="https://grafana.com/"><img alt="Grafana" src="https://img.shields.io/badge/Grafana-F2F4F9?style=for-the-badge&logo=grafana&logoColor=orange&labelColor=F2F4F9" /></a>
 </p>

 <h4>Database & ORM</h4>

 <p>
  <a href="https://www.tigerdata.com/timescaledb"><img alt="TimescaleDB" src="https://img.shields.io/badge/TimescaleDB-FF6F00?style=for-the-badge&logo=timescale&logoColor=white" /></a>
  <a href="https://www.postgresql.org/"><img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" /></a>
  <a href="https://alembic.sqlalchemy.org/en/latest/"><img alt="Alembic - SQLAlchemy" src="https://img.shields.io/badge/Alembic-39003E?style=for-the-badge&logo=sqlalchemy&logoColor=white" /></a>
 </p>

 <h4>Networking & Data Handling</h4>
 
 <p>
  <a href="https://tailscale.com"><img alt="Tailscale" src="https://img.shields.io/badge/Tailscale-100000?style=for-the-badge&logo=tailscale&logoColor=white" /></a>
  <a href="https://mosquitto.org/"><img alt="Eclipse Mosquitto" src="https://img.shields.io/badge/Mosquitto-008000?style=for-the-badge&logo=eclipse-mosquitto&logoColor=white" /></a>
  <a href="https://www.influxdata.com/time-series-platform/telegraf/"><img alt="InfluxData" src="https://img.shields.io/badge/Telegraf-22ADF1?style=for-the-badge&logo=influxdb&logoColor=white" /></a>
 </p>

 <h4>Hardware Platforms</h4>

 <p>
  <a href="https://adafru.it"><img alt="adafruit" src="https://img.shields.io/badge/Adafruit-00BFFF?style=for-the-badge&logo=adafruit&logoColor=white" /></a>
  <a href="https://raspberrypi.org/"><img alt="Raspberry Pi" src="https://img.shields.io/badge/Raspberry%20Pi-C51A4A?style=for-the-badge&logo=raspberry-pi&logoColor=white" /></a>
  <a href="https://microbit.org/"><img alt="micro:bit" src="https://img.shields.io/badge/micro:bit-00ED00?style=for-the-badge&logo=micro:bit&logoColor=white" /></a>
 </p>

<!-- Adding this later when using Raspberry Pi 3 B+ or Tuino 1
 <p>
  <a href="https://raspberrypi.org/"><img alt="Raspberry Pi" src="https://img.shields.io/badge/Raspberry%20Pi-C51A4A?style=for-the-badge&logo=raspberry-pi&logoColor=white" /></a>
  <a href="https://arduino.cc/"><img alt="Arduino" src="https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=arduino&logoColor=white" /></a>
 </p>
-->

</div>

<br />


# Repository Structure

The repository is organized into several key directories:
- `project/`: Contains the main project code and documentation.
    - `docs/`: Contains documentation related to the project.
    - `firmware/`: Contains the micro:bit firmware code.
    - `migrations/`: Contains Alembic database migration scripts.
    - `src/`: Contains the source code for the data logger and database interactions.
        - `database/`: Contains database connection and model definitions.
        - `monitoring/`: Contains grafana dasboard configurations.
        - `utils/`: Contains utility functions such as the serial reader.
- `templates/`: Contains template repositories 
    - `fhnw-ipro-indoor-climate-genavi/`: Template for the indoor climate project (GitHub).
    - `ipro_strat_hs25/`: Template for ipro project (FHNW GitLab).

Both projects `template-indoor-climate-genavi` and `ipro_strat_hs25` are set up as submodules within this repository. In order to work with them, you need to initialize and update the submodules after cloning the main repository. (Not needed to run the Indoor Climate Project itself)

```console
$ git clone <repository_url>
$ cd <repository_directory>
$ git submodule update --init --recursive
```

# Getting started

The [getting-started.md](project/docs/getting-started.md) file provides detailed instructions on setting up the development environment for the Indoor Climate Project.

# Roadmap and Project Log
Check the [project.md | Project Plan](project/docs/0-project/project.md#project-plan) for an overview of the project timeline, milestones, and levels.

Progress and updates are documented in the [project.md | Project Log](project/docs/0-project/project.md#project-log).

# License
TBD