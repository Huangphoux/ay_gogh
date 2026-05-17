import time
from locust import HttpUser, task, between


class Learner(HttpUser):
    wait_time = between(0.5, 10)

    def on_start(self):
        self.client.post("/login", json={"username": "foo", "password": "bar"})

    def on_stop(self):
        pass

    @task
    def hello_world(self):
        self.client.get("/hello")
        self.client.get("/world")

    @task(3) # the number is weight when choosing task
    def view_items(self):
        for item_id in range(10):
            self.client.get(f"/item?id={item_id}", name="/item")
            time.sleep(1)
