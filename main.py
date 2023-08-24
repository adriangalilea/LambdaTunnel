from textual.app import App
from textual import events
from lambdalabs import LambdaLabs
from textual.widgets import Button, Checkbox, Static
from textual.reactive import Reactive

class LambdaLabsApp(App):
    CSS_PATH = "lambda.css"
    BINDINGS = [("s", "action_start_instance", "Start Instance"), 
                ("a", "action_set_alarm", "Set Alarm"), 
                ("j", "action_auto_join", "Auto Join")]

    def __init__(self, api_key):
        super().__init__()
        self.lambdalabs = LambdaLabs(api_key)
        self.region_name = self.lambdalabs.get_region()  # dynamically retrieve region
        self.instance_type_name = self.lambdalabs.get_instance_type()  # dynamically retrieve instance type
        self.ssh_key_name = None  # Will be set in choose_ssh_key
        self.offered_instances = Reactive([])
        self.alarms = []
        self.static_widget = Static("Press a number key to check instance status")

    async def choose_ssh_key(self):
        ssh_keys = self.lambdalabs.list_ssh_keys()
        menu_items = [(str(i), key) for i, key in enumerate(ssh_keys)]
        # The Menu class is not available in the textual.widgets module
        # Instead, we will print the keys and ask the user to select one
        print("Available SSH keys:")
        for item in menu_items:
            print(item)
        selected_key = input("Please enter the number of the SSH key you want to use: ")
        self.ssh_key_name = menu_items[int(selected_key)][1]
        
    async def on_mount(self) -> None:
        await self.choose_ssh_key()
        self.offered_instances = self.lambdalabs.list_offered_instances()
        self.screen.background = "darkblue"
        await self.view.dock(self.static_widget, edge="top")
        await self.view.dock(self.start_button, edge="left")
        await self.view.dock(self.set_alarm_button, edge="left")
        await self.view.dock(self.auto_join_checkbox, edge="left")

    def on_key(self, event: events.Key) -> None:
        if event.key.isdecimal():
            instance_index = int(event.key)
            if instance_index < len(self.offered_instances):
                instance = self.offered_instances[instance_index]
                if instance['status'] == 'offline':
                    self.alarms.append(instance['id'])
                    self.screen.background = "bg:green"
                    self.static_widget.update("Instance is offline")
                else:
                    self.screen.background = "bg:red"
                    self.static_widget.update("Instance is online")

    def action_start_instance(self) -> None:
        self.lambdalabs.launch_instance(self.region_name, self.instance_type_name, [self.ssh_key_name])

    def action_set_alarm(self, instance_id: str) -> None:
        self.lambdalabs.restart_instance(instance_id)

    def action_auto_join(self, instance_id: str) -> None:
        self.lambdalabs.terminate_instance(instance_id)

if __name__ == "__main__":
    api_key = 'secret_lambda_b3e9dc2cdfe94bebaad2805b7d579ea0.jHMgOTrQKIfGaOABzkFNAgADX5a3YXg1'  # replace with your actual API key
    app = LambdaLabsApp(api_key)
    app.run()