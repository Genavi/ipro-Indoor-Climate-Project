# Project Plan - Variant: Long

### Part One
```mermaid
gantt
    dateFormat YYYY-MM-DD
    excludes weekends
    Project Start : milestone, done, t0, 2026-01-12, 0d
    Working on project :done, t01, 2026-01-12, 5d
    Level 0 :done, t02, 2026-01-12, 1d
    Level 1 :done, t03, after t02, 4d
    Research available Sensors :done, t03, after t02, 4d
    Research available Microcontroller :done, t03, after t02, 4d
    Working on project : active, t2, 2026-01-19, 5d
    Level 3 :active, t04, 2026-01-19, 5d
    Learning Telegraf : done, t05, 2026-01-19, 2d
    Setup Cloud Solution : active, t06, after t05, 2d
    Setup Networking: active, t07, after t05, 2d
    Setup MQTT Broker : active, t08, after t05, 2d
    Setup Telegraf read/write from FeatherS3 : active, t07, after t05, 2d
    Ingestion from FeatherS3 to InfluxDB : active, t08, after t05, 2d
    Update Grafana Dashboard : active, t09, after t07, 1d
    Unit Testing and Documentation : active, t10, after t08, 1d
    Feedback-Markt : milestone, t3, 2026-01-26, 0d
    Working on project : t4, 2026-01-26, 5d
    Working on project : t4, 2026-02-02, 5d
    Working on project : t4, 2026-02-09, 5d
    Interim submission : milestone, t7, 2026-02-14, 0d
```

### Part Two
```mermaid
gantt
    dateFormat YYYY-MM-DD
    excludes weekends
    Unfreeze Project : milestone, t0, 2026-08-10, 0d
    Working on project : t01, 2026-08-10, 5d
    Working on project : t2, 2026-08-17, 5d
    Feedback-Markt : milestone, t3, 2026-08-17, 0d
    Working on project : t4, 2026-08-24, 5d
    Working on project : t4, 2026-08-31, 5d
    Working on project : t4, 2026-09-07, 1d
    Interim submission : milestone, t7, 2026-09-08, 0d
```

## Project Levels
- [Level 0](../../../templates/fhnw-ipro-indoor-climate-genavi/level-0/README.md#building-blocks)
- [Level 1](../../../templates/fhnw-ipro-indoor-climate-genavi/level-1/README.md#building-blocks)
- [Level 2](../../../templates/fhnw-ipro-indoor-climate-genavi/level-2/README.md#building-blocks)
- [Level 3](../../../templates/fhnw-ipro-indoor-climate-genavi/level-3/README.md#building-blocks)
- [Level 4](../../../templates/fhnw-ipro-indoor-climate-genavi/level-4/README.md#building-blocks)


## Research available Microcontroller and Sensors
- [Personal Hardware](../2-hardware/personal-hardware.md)
