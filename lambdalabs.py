import requests
import base64


class LambdaLabs:
    def __init__(self, api_key, auth_type='basic'):
        self.api_key = api_key
        self.auth_type = auth_type
        self.base_url = 'https://cloud.lambdalabs.com/api/v1'

    def _get_auth_header(self):
        if self.auth_type == 'basic':
            return {'Authorization': 'Basic ' + base64.b64encode(self.api_key.encode()).decode()}
        elif self.auth_type == 'bearer':
            return {'Authorization': 'Bearer ' + self.api_key}
        else:
            raise ValueError('Invalid auth_type. Must be "basic" or "bearer".')

    def launch_instance(self, region_name, instance_type_name, ssh_key_names, file_system_names=None, quantity=1, name=None):
        url = self.base_url + '/instances'
        headers = self._get_auth_header()
        data = {
            'region_name': region_name,
            'instance_type_name': instance_type_name,
            'ssh_key_names': ssh_key_names,
            'file_system_names': file_system_names,
            'quantity': quantity,
            'name': name
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()

    def list_offered_instances(self):
        url = self.base_url + '/instance-types'
        headers = self._get_auth_header()
        response = requests.get(url, headers=headers)
        data = response.json().get('data', {})
        result = {}
        for key, value in data.items():
            result[key] = {
                'available': bool('regions_with_capacity_available' in value and value['regions_with_capacity_available']),
                'regions': [region['name'] for region in value.get('regions_with_capacity_available', [])],
                'price_cents_per_hour': value['instance_type']['price_cents_per_hour']
            }
        return result

    def list_running_instances(self):
        url = self.base_url + '/instances/running'
        headers = self._get_auth_header()
        response = requests.get(url, headers=headers)
        data = response.json().get('data', [])
        if not data:
            return []
        return [instance['id'] for instance in data]

    def get_instance_details(self, instance_id):
        url = self.base_url + '/instances/' + instance_id
        headers = self._get_auth_header()
        response = requests.get(url, headers=headers)
        data = response.json().get('data', {})
        if not data:
            return {}
        return {
            'instance_type': data['instance_type']['name'],
            'price_cents_per_hour': data['instance_type']['price_cents_per_hour'],
            'ip': data['ip']
        }

    def terminate_instance(self, instance_id):
        url = self.base_url + '/instances/' + instance_id
        headers = self._get_auth_header()
        response = requests.delete(url, headers=headers)
        return response.json()

    def restart_instance(self, instance_id):
        url = self.base_url + '/instances/' + instance_id + '/restart'
        headers = self._get_auth_header()
        response = requests.post(url, headers=headers)
        return response.json()

    def list_ssh_keys(self):
        url = self.base_url + '/ssh-keys'
        headers = self._get_auth_header()
        response = requests.get(url, headers=headers)
        data = response.json().get('data', [])
        if not data:
            return []
        return [key['name'] for key in data]
