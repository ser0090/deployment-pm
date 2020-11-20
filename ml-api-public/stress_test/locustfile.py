import time
from locust import HttpUser
from locust import task

class QuickstartUser(HttpUser):

    POS_SENT = 'Esta es una oracion positiva y estoy contento por eso'

    @task(1)
    def index(self):
        self.client.get("/")

    @task(3)
    def predict(self):
        self.client.post("/predict", params={"text": self.POS_SENT})

    def on_start(self):
        pass
