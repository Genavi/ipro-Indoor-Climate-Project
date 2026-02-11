# DigitalOcean Setup

> GitHub Education students can get free $200 credit for DigitalOcean. Check [education.github.com](https://education.github.com/pack#digitalocean).
>
> Using the recommended Droplet configuration should be sufficient for hosting the Indoor Climate Project application for small to medium usage up to 9 months. Adjust the resources based on your expected load and performance requirements.
>
> Note: DigitalOcean charges for Droplet usage. Make sure to monitor your usage to avoid unexpected costs.

## Recommended Droplet Configuration
- **Image**: Marketplace > Docker on Ubuntu 22.04 LTS
- **Droplet Type**: Shared CPU - Basic
- **CPU**: Premium AMD > 2 vCPUs
- **Memory**: 2 GB
- **Storage**: 50GB NVMe SSDs
- **Transfer**: 3 TB
- **Authentication**: SSH Keys (add your public SSH key)

## Creating a Droplet
1. Log in to your DigitalOcean account.
2. Navigate to the "Droplets" section and click on "Create Droplet".
3. Choose an image:
   - Select "Marketplace"
   - Choose the latest Docker LTS version.
4. Choose a plan:
   - Select the plan that fits your needs (e.g., Basic, Standard).
5. Choose a datacenter region:
   - Select a region that is geographically close to your target users.
6. Authentication:
   - Choose SSH keys for secure access.
   - Add your public SSH key if you haven't done so already.
7. Finalize and create:
   - Review your settings and click on "Create Droplet".
