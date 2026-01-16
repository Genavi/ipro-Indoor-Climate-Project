# ipro: Indoor Climate Project

This repository contains the code and resources for the Indoor Climate Project (ipro).

## Repository Structure

The repository is organized into several key directories:
- `project/`: Contains the main project code and documentation.
    - `docs/`: Contains documentation related to the project.
- `templates/`: Contains template repositories 
    - `fhnw-ipro-indoor-climate-genavi/`: Template for the indoor climate project (GitHub).
    - `ipro_strat_hs25/`: Template for ipro project (FHNW GitLab).

Both projects `template-indoor-climate-genavi` and `ipro_strat_hs25` are set up as submodules within this repository. In order to work with them, you need to initialize and update the submodules after cloning the main repository.

```bash
git clone <repository_url>
cd <repository_directory>
git submodule update --init --recursive
```

The [getting-started.md](project/docs/getting-started.md) file provides detailed instructions on setting up the development environment for the Indoor Climate Project.