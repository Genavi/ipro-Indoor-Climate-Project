# Features for Part Two of the Project
This document outlines the possible features and improvements for the second part of the Indoor Climate Project. These features can be build upon the existing functionality and enhance the overall user experience and capabilities of the application.

## Possible Features
1. **Additional Datasources for Grafana Dashboard**:
   - Integrate external weather data to provide context for indoor climate conditions. This can be done by using a weather API (e.g., OpenWeatherMap) to fetch outdoor weather data and display it on the Grafana dashboard alongside the indoor sensor data.
   - Add container metrics to monitor the performance and resource usage of the Docker containers running the application. This can be achieved by using Telegraf's Docker input plugin to collect metrics such as CPU usage, memory usage, and network I/O, and then visualizing this data in Grafana.
2. **Additional Sensor for Window State**:
   - Add a new sensor to monitor the state of the window (open/closed). This can be implemented using a simple magnetic reed switch sensor connected to the micro:bit. The sensor data can be sent to the MQTT broker and stored in the TimescaleDB database, allowing it to be visualized on the Grafana dashboard. This feature can provide insights into how the window state affects indoor climate conditions.
3. **Threshold Alerting in Grafana**:
   - Implement threshold alerting in Grafana to notify users when certain conditions are met (e.g., CO2 levels exceed 1000 ppm, humidity levels exceed 50%H). This can be set up using Grafana's alerting features, allowing users to receive notifications via email, Slack, or other channels when the defined thresholds are exceeded. This can help users take timely action to improve indoor air quality.
4. **Healthcheck Alerting for FeatherS3 Connection**:
   - Set up healthcheck alerting in Grafana to monitor the status of the FeatherS3 connection. This can be done by creating a healthcheck query in Grafana that checks the status of the connection to the FeatherS3 sensor. If the connection is lost or if there are issues with the sensor, an alert can be triggered to notify the user, allowing them to troubleshoot and resolve the issue promptly.
5. **Documentation Updates**:
   - Update the project documentation to include the new features and improvements added in part two of the project. This includes updating the README file, adding new sections to the documentation for the additional datasources, the window state sensor, and the alerting setup in Grafana. Clear and comprehensive documentation will help users understand how to use the new features and how to set up their own instances of the application with the added functionality.
6. **Additional Improvements**:
   - Based on user feedback and testing, additional improvements and features may be identified and implemented during the second part of the project. This can include performance optimizations, UI/UX enhancements for the Grafana dashboard, or additional integrations with other services or platforms.
7. **Security Enhancements**:
   - Implement security best practices for the application, such as securing the MQTT broker with TLS encryption, implementing authentication and authorization for accessing the Grafana dashboard, and ensuring that sensitive data (e.g., database credentials) is stored securely using environment variables or secret management tools.
8. **Backup and Recovery Solutions**:
   - Set up backup and recovery solutions for the TimescaleDB database to prevent data loss in case of hardware failure or other issues. This can include automated backups, offsite storage of backups, and testing of the recovery process to ensure that data can be restored successfully when needed.
9. **Performance Monitoring and Optimization**:
   - Implement performance monitoring for the application to identify any bottlenecks or issues that may arise as the application scales. This can include monitoring the performance of the database, the MQTT broker, and the Grafana dashboard, and optimizing queries, configurations, or resource allocations as needed to ensure smooth operation of the application.
10. **User Interface Enhancements**:
    - Enhance the user interface of the Grafana dashboard to improve usability and provide a better user experience. This can include customizing the dashboard layout, adding interactive elements, and improving the visual design to make it more intuitive and visually appealing for users.
11. **Mobile Accessibility**:
    - Ensure that the Grafana dashboard is accessible and usable on mobile devices, allowing users to monitor their indoor climate conditions on the go. This can involve optimizing the dashboard layout for smaller screens and ensuring that all features are functional on mobile browsers.
