# Why?
_Performance for [stable-diffusion](https://github.com/AUTOMATIC1111/stable-diffusion-webui) on MacOS/iPadOS is not that great, many people are building dedicated Windows systems with high-end GPU's, and that's great but I think we can do better._

What about using locally a remote Nvidia H100 ($40,000 GPU) at $1,90 per hour?

# Prerequisites
- An account on Lambda Cloud.

# Steps
1. CLone the repo
2. install requirements.txt
3. Run main.py

# Features
<img width="330" alt="image" src="https://github.com/adriangalilea/LambdaTunnel/assets/90320947/4c0f00d4-dcb8-42bf-8dc9-04c128a1cd2d">
See what is available and directly launch an instance.

<img width="333" alt="image" src="https://github.com/adriangalilea/LambdaTunnel/assets/90320947/7d93326e-a15b-49ba-9928-a49a07023e63">
Create an alarm for a specific type of instance.

<img width="336" alt="image" src="https://github.com/adriangalilea/LambdaTunnel/assets/90320947/7767a49c-87e2-483d-be3b-4c879b41dbcd">


<img width="273" alt="image" src="https://github.com/adriangalilea/LambdaTunnel/assets/90320947/282db9b6-739f-4133-b15a-c1869d265ab1">


<img width="266" alt="image" src="https://github.com/adriangalilea/LambdaTunnel/assets/90320947/119214b5-f129-4b37-9e79-6f01e76bf25a">
You can launch a payload that will run everything for you, including the ssh tunnel. I will add more than Fooocus, but currently is the one I'm using, feel free to add others.

It'll atuomatically open a tab on your browser when it's done installing everything and doing the tunnel



## Lamdalabs
I'm not affiliated in any way shape or form to Lambdalabs.

### WARNING $$$
BE SURE TO CLOSE THE INSTANCE WHEN YOU ARE DONE I WOULD LIKE TO BE ABLE TO CLOSE THE SESSION BY SHUTTING DOWN THE SERVER BUT LAMBDALABS DON'T ALLOW THIS, I'M SHOUTING IN HOPES YOU SAVE SOME HARD EARNED CASH, IF YOU ARE READING THIS AFTER HAVING SPENT A BUNCH OF MONEY BECAUSE YOU WENT TO SLEEP AND FORGOT, I'M SORRY BUT THAT'S YOUR FAULT <3, THANKS FOR LISTENING TO MY TED-TALK.

Notice you'll pay for the setup time too, this is meant for serious work or enthusiasts.

# Security disclaimer and agreement
Running scripts directly from the web is a potential security risk. Before running the command, you should inspect the script from this repository. By running the command, you are acknowledging that you trust the source and the contents of the script.

While every effort has been made to ensure the safety and effectiveness of this script, it is provided as-is without any warranties or assurances of any kind. The author of this script cannot be held responsible for any damages, data loss, or issues of any kind arising from the use of this script.


# To-do
- [x] Working fast_setup.sh
- [x] update to python interactive program
- [ ] create a payload for automatic1111
- [ ] upgrade into a textual GUI
- [ ] [#1](https://github.com/adriangalilea/LambdaTunnel/issues/1)
- [ ] Having an auto-close instance timer so you don't burn money if you forget.
- [ ] YouTube video tutorial
- [ ] Illustrate this readme with performance metrics.

# Contributing
I welcome contributions to this project! Please feel free to open an issue or submit a pull request.

Author: Adrian Galilea
Co-author: ChatGPT & copilot
🫀x🤖
