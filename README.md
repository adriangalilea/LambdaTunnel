# Why?
_Performance for [stable-diffusion](https://github.com/AUTOMATIC1111/stable-diffusion-webui) on MacOS/iPadOS is not that great, many people are building dedicated Windows systems with high-end GPU's, and that's great but I think we can do better._

What about using locally a remote Nvidia H100 ($40,000 GPU) at $2,40 per hour?


# Prerequisites
- An account on Lambda Cloud.
- An SSH key pair that you can use to connect to your Lambda Cloud instance.

# Fast set-up
Open your terminal.
Run the following command:
```bash
bash <(curl -s https://raw.githubusercontent.com/adriangalilea/LambdaTunnel/main/fast_setup.sh)
```
Follow the prompts in the terminal. The script will ask for the IP address of your Lambda Cloud instance, create an SSH tunnel, and mount the instance's filesystem on your local machine.
Once the script has finished running, you can access the stable-diffusion UI at http://localhost:7860.

# Disclaimer
## Lamdalabs
I'm not affiliated in any way shape or form to Lambdalabs... yet 😜

## Security
Running scripts directly from the web is a potential security risk. Before running the command, you should inspect the script from this repository. By running the command, you are acknowledging that you trust the source and the contents of the script.

While every effort has been made to ensure the safety and effectiveness of this script, it is provided as-is without any warranties or assurances of any kind. The author of this script cannot be held responsible for any damages, data loss, or issues of any kind arising from the use of this script.

For better security, consider cloning this repository and running the script locally:
```bash
git clone https://github.com/adriangalilea/LambdaTunnel.git
cd LambdaGPU-Helper
bash connect_to_server.sh
```
Or even better read how to do it manually:

# Manual set-up

1. [SSH key pair setup](https://cloud.lambdalabs.com/ssh-keys)
2. Spin up the [lambdalabs instance](https://cloud.lambdalabs.com/instances)
3. Wait until it's done loading and copy the ssh command
4. Connect to the instance through SSH on a terminal
5. (Optional) use tmux to install [stable-diffusion](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
6. Once Stable diffusion is finishing installing and is running exit tmux with `ctrl+b -> d` for detaching from tmux and leave stable diffusion running.
7. Create an ssh tunnel for the port stable diffusion uses 7860
8. For convenience you could connect to the remote server through filezilla or duck

# To-do
- [x] Working fast_setup.sh
- [ ] Proper manual guide
- [ ] pre-selecting extensions
- [ ] pre-selecting models from civit.ai
- [ ] Having an auto-close instance timer so you don't burn money if you forget.
- [ ] Test connect trough iPad Manually
- [ ] Automate iPad connection(prolly not gonna happen)
- [ ] YouTube video tutorial
- [ ] Illustrate this readme with performance metrics.

# Contributing
I welcome contributions to this project! Please feel free to open an issue or submit a pull request.
