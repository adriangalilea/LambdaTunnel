from lambdalabs import LambdaLabs
from termcolor import colored, cprint
import time
import os
import requests

lambda_labs = LambdaLabs('secret_lambda_b3e9dc2cdfe94bebaad2805b7d579ea0.jHMgOTrQKIfGaOABzkFNAgADX5a3YXg1')
SSH_KEY_NAME = "mac mini"

if not SSH_KEY_NAME:
    ssh_keys = lambda_labs.list_ssh_keys()
    print("Select an SSH key:")
    for i, key in enumerate(ssh_keys):
        print(f"{i+1}. {key}")
    selected_key = int(input("Enter the number of your selection: ")) - 1
    SSH_KEY_NAME = ssh_keys[selected_key]

running_instances = lambda_labs.list_running_instances()
if running_instances:
    for instance_id in running_instances:
        instance_details = lambda_labs.get_instance_details(instance_id)
        price_per_hour = instance_details['price_cents_per_hour'] / 100
        cprint(f"\n{instance_details['instance_type']}", 'green', end='')
        cprint(f" - ${price_per_hour:.2f}/hour", 'yellow')
        cprint(f"\nID: {instance_id}")
        cprint(f"IP Address: {instance_details['ip']}")
        while True:
            cprint("\n1. Create SSH tunnel", 'green')
            cprint("2. Connect via SSH", 'green')
            cprint("3. Kill instance", 'green')
            cprint("q. Quit", 'blue', attrs=['bold'])
            user_input = input("\nEnter your selection: ")
            if user_input.lower() == 'q':
                break
            elif user_input == '1':
                cprint(f"\nssh -L 7860:localhost:7860 ubuntu@{instance_details['ip']}", 'green')
            elif user_input == '2':
                cprint(f"\nssh ubuntu@{instance_details['ip']}", 'green')
            elif user_input == '3':
                try:
                    response = lambda_labs.terminate_instance(instance_id)
                    cprint("\nInstance terminated successfully.\n", 'green', attrs=['bold'])
                except requests.exceptions.JSONDecodeError:
                    cprint("\nFailed to terminate instance. Please try again.\n", 'red', attrs=['bold'])
                break
            else:
                cprint("\nInvalid selection. Please try again.\n", 'red', attrs=['bold'])
        cprint("\n")
else:
    cprint("\nInstances.\n", 'cyan', attrs=['bold'])
    offered_instances = {k: v for k, v in lambda_labs.list_offered_instances().items() if v is not None}
    for i, (instance, details) in enumerate(offered_instances.items()):
        price_per_hour = details['price_cents_per_hour'] / 100
        if details['regions']:
            cprint(f"{i+1}. {instance} - ${price_per_hour:.2f}/hour", 'green')
        else:
            cprint(f"{i+1}. {instance} - ${price_per_hour:.2f}/hour", 'red')
    cprint("\nq. quit", 'blue', attrs=['bold'])
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
