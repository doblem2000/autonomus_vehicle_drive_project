import carla

client = carla.Client('172.19.192.1', 6015)
print(client.get_available_maps())