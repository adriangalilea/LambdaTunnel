from lambdalabs import LambdaLabs
from termcolor import colored, cprint
import time
import os
import requests

from dotenv import load_dotenv
import os

if not os.path.isfile('.env'):
    with open('.env', 'w') as f:
        f.write('')

load_dotenv()

LAMBDA_LABS_KEY = os.getenv('LAMBDA_LABS_KEY')
if not LAMBDA_LABS_KEY:
    cprint("No Lambda Labs Key found in .env file.", 'red')
    os.system('open https://cloud.lambdalabs.com/api-keys')
    LAMBDA_LABS_KEY = input("Enter your Lambda Labs Key: ")
    with open('.env', 'a') as f:
        f.write(f'LAMBDA_LABS_KEY={LAMBDA_LABS_KEY}\n')
    os.environ['LAMBDA_LABS_KEY'] = LAMBDA_LABS_KEY
    os.system('clear')

lambda_labs = LambdaLabs(LAMBDA_LABS_KEY)
SSH_KEY_NAME = os.getenv('SSH_KEY_NAME')

if not SSH_KEY_NAME:
    ssh_keys = lambda_labs.list_ssh_keys()
    if ssh_keys:
        cprint("Select an SSH key:", 'green')
        for i, key in enumerate(ssh_keys):
            cprint(f"{i+1}. {key}", 'green')
        cprint(f"{len(ssh_keys)+1}. Create a new SSH key", 'green')
        selected_key = int(input("Enter the number of your selection: ")) - 1
        if selected_key < len(ssh_keys):
            SSH_KEY_NAME = ssh_keys[selected_key]
        else:
            key_name = input("Enter a name for your new SSH key: ")
            os.system(f"ssh-keygen -t rsa -b 4096 -C '{key_name}'")
            public_key = open(f"{os.getenv('HOME')}/.ssh/{key_name}.pub").read()
            lambda_labs.create_ssh_key(key_name, public_key)
            SSH_KEY_NAME = key_name
    else:
        cprint("No SSH keys found. Creating a new one.", 'yellow')
        key_name = input("Enter a name for your new SSH key: ")
        os.system(f"ssh-keygen -t rsa -b 4096 -C '{key_name}'")
        public_key = open(f"{os.getenv('HOME')}/.ssh/{key_name}.pub").read()
        lambda_labs.create_ssh_key(key_name, public_key)
        SSH_KEY_NAME = key_name

    with open('.env', 'a') as f:
        f.write(f'SSH_KEY_NAME={SSH_KEY_NAME}\n')
    os.environ['SSH_KEY_NAME'] = SSH_KEY_NAME
os.system('clear')

def display_running_instances():
    running_instances = lambda_labs.list_running_instances()
    if running_instances:
        for instance_id in running_instances:
            instance_details = lambda_labs.get_instance_details(instance_id)
            price_per_hour = instance_details['price_cents_per_hour'] / 100
            cprint(f"\n{instance_details['instance_type']}", 'green', end='')
            cprint(f" - ${price_per_hour:.2f}/hour", 'yellow')
            cprint(f"\nID: {instance_id}")
            cprint(f"IP Address: {instance_details['ip']}")
            instance_menu(instance_details, instance_id)
def instance_menu(instance_details, instance_id):
    while True:
        cprint("\n1. Connect via SSH", 'green')
        cprint("2. Kill instance", 'red')
        cprint("3. Install and run payload", 'green')
        cprint("\nq. Quit", 'blue', attrs=['bold'])
        user_input = input("\nEnter your selection: ")
        if user_input.lower() == 'q':
            break
        elif user_input == '1':
            os.system(f"ssh ubuntu@{instance_details['ip']}")
        elif user_input == '2':
            try:
                response = lambda_labs.terminate_instance(instance_id)
                cprint("\nInstance terminated successfully.\n", 'green', attrs=['bold'])
            except requests.exceptions.JSONDecodeError:
                cprint("\nFailed to terminate instance. Please try again.\n", 'red', attrs=['bold'])
            break
        elif user_input == '3':
            execute_payload(instance_details['ip'])
        else:
            cprint("\nInvalid selection. Please try again.\n", 'red', attrs=['bold'])
    cprint("\n")

def execute_payload(ip):
    payloads = {
        'fooocus': [
            '[ -d "$HOME/miniconda" ] || (wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda)',
            'git clone https://github.com/lllyasviel/Fooocus.git || echo "Fooocus already exists, skipping clone"',
            'source $HOME/miniconda/bin/activate && cd Fooocus && conda env create -f environment.yaml || echo "Environment already exists, skipping creation" && conda activate fooocus && pip install -r requirements_versions.txt',
            'cd Fooocus && tmux new-session -d -s fooocus "source $HOME/miniconda/bin/activate && conda activate fooocus && python launch.py" || echo "Session already exists, skipping creation"',
            'while ! nc -z localhost 7860; do sleep 1; done'
        ],
        # Add more payloads here
    }
    cprint("\nSelect a payload:", 'green')
    for i, key in enumerate(payloads.keys()):
        cprint(f"{i+1}. {key}", 'green')
    selected_key = int(input("\nEnter the number of your selection: ")) - 1
    payload = payloads[list(payloads.keys())[selected_key]]
    for command in payload:
        cprint(f"\nExecuting command: {command}\n", 'green')
        result = os.system(f"ssh ubuntu@{ip} '{command}'")
        if result != 0:
            cprint("\nAn error occurred while executing the payload. Please check the commands and try again.\n", 'red', attrs=['bold'])
            return
    os.system(f"ssh -N -L 7860:localhost:7860 ubuntu@{ip} &")
    while True:
        tunnel_check = os.system(f"nc -z localhost 7860")
        if tunnel_check == 0:
            cprint("\nPayload is running on 127.0.0.1:7860\n", 'green', attrs=['bold'])
            os.system("open http://127.0.0.1:7860/")
            break
        else:
            cprint("\nWaiting for payload to start...\n", 'yellow')
            time.sleep(5)
def display_offered_instances():
    cprint("\nInstances.\n", 'cyan', attrs=['bold'])
    offered_instances = {k: v for k, v in lambda_labs.list_offered_instances().items() if v is not None}
    for i, (instance, details) in enumerate(offered_instances.items()):
        price_per_hour = details['price_cents_per_hour'] / 100
        if details['regions']:
            cprint(f"{i+1}. {instance} - ${price_per_hour:.2f}/hour", 'green')
        else:
            cprint(f"{i+1}. {instance} - ${price_per_hour:.2f}/hour", 'red')
    cprint("\nq. Quit", 'blue', attrs=['bold'])
    launch_instance_menu(offered_instances)

def launch_instance_menu(offered_instances):
    while True:
        try:
            user_input = input("\nEnter the number of the instance to launch: ")
            if user_input.lower() == 'q':
                exit()
            selected_instance = int(user_input) - 1
            INSTANCE_NAME = list(offered_instances.keys())[selected_instance]
            if offered_instances[INSTANCE_NAME]['regions']:
                regions = offered_instances[INSTANCE_NAME]['regions']
                selected_region = regions[0]
                instance_id = lambda_labs.launch_instance(selected_region, INSTANCE_NAME, SSH_KEY_NAME)
                if instance_id:
                    cprint("\nInstance launched successfully.\n", 'green', attrs=['bold'])
                    display_running_instances()
                    break
                else:
                    cprint("\nFailed to launch instance. Please try again.\n", 'red', attrs=['bold'])
            else:
                while True:
                    if offered_instances[INSTANCE_NAME]['regions']:
                        cprint(f"{colored(time.strftime('%Y-%m-%d %H:%M:%S'), 'grey')} - {colored(INSTANCE_NAME, 'green')}", 'white')
                        os.system('afplay /System/Library/Sounds/Glass.aiff')
                        break
                    else:
                        cprint(f"{colored(time.strftime('%Y-%m-%d %H:%M:%S'), 'grey')} - {colored(INSTANCE_NAME, 'red')}", 'white')
                        time.sleep(15)
        except (ValueError, IndexError):
            cprint("\nInvalid selection. Please try again.\n", 'red', attrs=['bold'])

display_running_instances()
display_offered_instances()
