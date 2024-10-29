import requests


class Log:

    def __init__(self, message):
        self.message = message

    def insert_log(self):
        # Copilot sugiere esto, para mi es mas efectivo en la base de datos
        # chatgpt lo reduce a gusto ambos tienen ventajas y desventajas
        url = "http://localhost:5000/log"
        data = {"message": self.message}
        response = requests.post(url, json=data)
        print(response.json())
