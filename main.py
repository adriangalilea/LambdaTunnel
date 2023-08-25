from lambdalabs import LambdaLabs
from termcolor import colored, cprint
import time
import os

lambda_labs = LambdaLabs('')
SSH_KEY_NAME = ""

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
        print(f"Instance ID: {instance_id}")
        print(f"Instance Type: {instance_details['instance_type']}")
        print(f"Price (cents per hour): {instance_details['price_cents_per_hour']}")
        print(f"IP: {instance_details['ip']}")
        print("SSH LOGIN")
        print(f"ssh ubuntu@{instance_details['ip']}")
        print("\n")
else:
    offered_instances = lambda_labs.list_offered_instances()
    cprint("\nInstances.\n", 'cyan', attrs=['bold'])
    valid_instances = {k: v for k, v in offered_instances.items() if v is not None}
    region_memory = {}
    for i, (instance, details) in enumerate(valid_instances.items()):
        price_per_hour = details['price_cents_per_hour'] / 100
        if details['available']:
            cprint(f"{i+1}. {instance} - ${price_per_hour:.2f}/hour", 'green')
            region_memory[instance] = details['regions'][0] if details['regions'] else None
        else:
            cprint(f"{i+1}. {instance} - ${price_per_hour:.2f}/hour", 'red')
    cprint("\nq. quit", 'blue', attrs=['bold'])
    while True:
        try:
            user_input = input("\nEnter the number of the instance to launch: ")
            if user_input.lower() == 'q':
                exit()
            selected_instance = int(user_input) - 1
            INSTANCE_NAME = list(valid_instances.keys())[selected_instance]
            SELECTED_REGION = region_memory.get(INSTANCE_NAME)
            if SELECTED_REGION and valid_instances[INSTANCE_NAME]['available']:
                lambda_labs.launch_instance(SELECTED_REGION, INSTANCE_NAME, [SSH_KEY_NAME])
                cprint("\nInstance launched successfully.\n", 'green', attrs=['bold'])
                break
            else:
                while True:
                    if valid_instances[INSTANCE_NAME]['available']:
                        cprint(f"{colored(time.strftime('%Y-%m-%d %H:%M:%S'), 'grey')} - {colored(INSTANCE_NAME, 'green')}", 'white')
                        os.system('afplay /System/Library/Sounds/Glass.aiff')
                        break
                    else:
                        cprint(f"{colored(time.strftime('%Y-%m-%d %H:%M:%S'), 'grey')} - {colored(INSTANCE_NAME, 'red')}", 'white')
                        time.sleep(15)
        except (ValueError, IndexError):
            cprint("\nInvalid selection. Please try again.\n", 'red', attrs=['bold'])