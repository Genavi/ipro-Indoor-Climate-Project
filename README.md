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

  <kbd><img src="./project/docs/images/grafana-dashboard_v3.png" width="800" /></kbd>

  <p>A real-time indoor climate monitoring system that tracks CO₂ levels, temperature, humidity, and ambient light. Data is collected from ESP32-S3 sensors and visualized through modern Grafana dashboards optimized for Desktop and iPad displays.</p>

  <p><strong>Live Monitoring:</strong> Auto-refreshing dashboards with air quality scoring, threshold alerts, and dual-axis sensor visualization.</p>
  <p><strong>Local Weather Station Data:</strong> MeteoSwiss API integration for fetching data from local weather stations.</p>
  <p><strong>AI Integration:</strong> Utilizes the Gemini AI agent for predictive analytics and recommendations based on historical and real-time data.</p>

  <h2>Technologies Used</h2>

  <h4>Programming Languages & Frameworks</h4>
  <a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" /></a>
  <a href="https://micropython.org/"><img alt="MicroPython" src="https://img.shields.io/badge/MicroPython-2D2D2D?style=for-the-badge&logo=micropython&logoColor=white" /></a>
  <a href="https://docs.docker.com/compose/"><img alt="Docker Compose" src="https://img.shields.io/badge/Docker%20Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" /></a>

  <h4>Visualisation</h4>
  <a href="https://grafana.com/"><img alt="Grafana" src="https://img.shields.io/badge/Grafana-F2F4F9?style=for-the-badge&logo=grafana&logoColor=orange&labelColor=F2F4F9" /></a>

  <h4>AI Integration</h4>
  <a href="https://gemini.com/"><img alt="Gemini" src="https://img.shields.io/badge/Gemini-8E44AD?style=for-the-badge&logo=googlegemini&logoColor=white" /></a>

  <h4>Database & ORM</h4>
  <a href="https://www.tigerdata.com/timescaledb"><img alt="TimescaleDB" src="https://img.shields.io/badge/TimescaleDB-FF6F00?style=for-the-badge&logo=timescale&logoColor=white" /></a>
  <a href="https://www.postgresql.org/"><img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" /></a>
  <a href="https://alembic.sqlalchemy.org/en/latest/"><img alt="Alembic - SQLAlchemy" src="https://img.shields.io/badge/Alembic-39003E?style=for-the-badge&logo=sqlalchemy&logoColor=white" /></a>

  <h4>Networking & Data Handling</h4>
  <a href="https://tailscale.com"><img alt="Tailscale" src="https://img.shields.io/badge/Tailscale-100000?style=for-the-badge&logo=tailscale&logoColor=white" /></a>
  <a href="https://mosquitto.org/"><img alt="Eclipse Mosquitto" src="https://img.shields.io/badge/Mosquitto-008000?style=for-the-badge&logo=eclipse-mosquitto&logoColor=white" /></a>
  <a href="https://www.influxdata.com/time-series-platform/telegraf/"><img alt="InfluxData" src="https://img.shields.io/badge/Telegraf-22ADF1?style=for-the-badge&logo=influxdb&logoColor=white" /></a>

  <h4>Hardware Platforms</h4>
  <a href="https://adafru.it"><img alt="adafruit" src="https://img.shields.io/badge/Adafruit-00BFFF?style=for-the-badge&logo=adafruit&logoColor=white" /></a>
  <a href="https://raspberrypi.org/"><img alt="Raspberry Pi" src="https://img.shields.io/badge/Raspberry%20Pi-C51A4A?style=for-the-badge&logo=raspberry-pi&logoColor=white" /></a>
  <a href="https://microbit.org/"><img alt="micro:bit" src="https://img.shields.io/badge/micro:bit-00ED00?style=for-the-badge&logo=micro:bit&logoColor=white" /></a>

</div>

<hr />

# Repository Structure

The repository is organized into several key directories:

```
project/
├── database/                               # Contains database connection and model definitions.
├── docs/                                   # Contains documentation related to the project.
├── firmware/                               # Contains the micro:bit firmware code.
├── migrations/                             # Contains Alembic database migration scripts.
├── monitoring/                             # Contains grafana dasboard configurations.
├── mosquitto/                              # Contains mosquitto configuration files.
└── src/                                    # Contains the source code for the data logger and database interactions.
    ├── climate_advisor/                    # Contains the climate advisor code.
    ├── fetch_meteoswiss_data/              # Contains code to fetch data from MeteoSwiss.
    └── raspberry_py_script/                # Contains the Raspberry Pi code to fetch data from ESP32.
templates/ 
    ├── fhnw-ipro-indoor-climate-genavi/    # Template for the indoor climate project (GitHub).
    └── ipro_strat_hs25/                    # Template for ipro project (FHNW GitLab).
```

Both projects `template-indoor-climate-genavi` and `ipro_strat_hs25` are set up as submodules within this repository. In order to work with them, you need to initialize and update the submodules after cloning the main repository. (Not needed to run the Indoor Climate Project itself)

```console
$ git clone <repository_url>
$ cd <repository_directory>
$ git submodule update --init --recursive
```

# Getting started

The [getting-started.md](project/docs/getting-started.md) file provides detailed instructions on setting up the development environment for the Indoor Climate Project.

# Roadmap and Project Log
Check the [project.md | Project Plan](project/docs/0-project/project.md#part-one) for an overview of the project timeline and milestones.

Progress and updates are documented in the [project.md | Project Log](project/docs/0-project/project.md#project-log).

# License
TBD