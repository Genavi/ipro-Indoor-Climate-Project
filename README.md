<div align='center'>
 <h1>
  ipro: Indoor Climate Project
 </h1>

 <p>
  This repository contains the code and resources for the Indoor Climate Project (ipro).
 </p>

 <p>
  Check the <a href='#'>Demo</a> (planned).
 </p>

 <p>
  <a href="https://www.python.org/"><img alt="Python" src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" /></a>
  <a href="https://docs.docker.com/compose/"><img alt="Docker Compose" src="https://img.shields.io/badge/Docker%20Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" /></a>
  <a href="https://grafana.com/"><img alt="Grafana" src="https://img.shields.io/badge/Grafana-F2F4F9?style=for-the-badge&logo=grafana&logoColor=orange&labelColor=F2F4F9" /></a>
 </p>

 <p>
  <a href="https://www.postgresql.org/"><img alt="PostgreSQL" src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" /></a>
  <a href="https://www.sqlalchemy.org/"><img alt="SQLAlchemy" src="https://img.shields.io/badge/SQLAlchemy-39003E?style=for-the-badge&logo=sqlalchemy&logoColor=white" /></a>
  <a href="https://alembic.sqlalchemy.org/"><img alt="Alembic" src="https://img.shields.io/badge/Alembic-2D3E50?style=for-the-badge&logo=alembic&logoColor=white" /></a>
  <a href="https://microbit.org/"><img alt="micro:bit" src="https://img.shields.io/badge/micro:bit-00ED00?style=for-the-badge&logo=micro:bit&logoColor=white" /></a>
 </p>

<!-- Adding this later when using Raspberry Pi 3 B+ or Tuino 1
 <p>
  <a href="https://raspberrypi.org/"><img alt="Raspberry Pi" src="https://img.shields.io/badge/Raspberry%20Pi-C51A4A?style=for-the-badge&logo=raspberry-pi&logoColor=white" /></a>
  <a href="https://arduino.cc/"><img alt="Arduino" src="https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=arduino&logoColor=white" /></a>
 </p>
-->

 <kbd><img src="./project/docs/images/grafana-dashboard_v1.png" width="600" /></kbd>

</div>

<br />


## Repository Structure

The repository is organized into several key directories:
- `project/`: Contains the main project code and documentation.
    - `docs/`: Contains documentation related to the project.
- `templates/`: Contains template repositories 
    - `fhnw-ipro-indoor-climate-genavi/`: Template for the indoor climate project (GitHub).
    - `ipro_strat_hs25/`: Template for ipro project (FHNW GitLab).

Both projects `template-indoor-climate-genavi` and `ipro_strat_hs25` are set up as submodules within this repository. In order to work with them, you need to initialize and update the submodules after cloning the main repository.

```console
$ git clone <repository_url>
$ cd <repository_directory>
$ git submodule update --init --recursive
```

## Getting started

The [getting-started.md](project/docs/getting-started.md) file provides detailed instructions on setting up the development environment for the Indoor Climate Project.

## Roadmap
Check the [project-plan.md](project/docs/0-project-plan/project-plan.md) for an overview of the project timeline, milestones, and levels.

## Project Logs
Progress and updates are documented in the [project-log.md](project/docs/1-project-logs/project-log.md#project-log).

## License
TBD