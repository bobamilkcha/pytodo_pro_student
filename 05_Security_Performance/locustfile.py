import uuid
from locust import HttpUser, task, between


class PyTodoUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        """Register and log in a unique user for each simulated Locust client."""
        self.username = f"perf_{uuid.uuid4().hex[:8]}"
        self.password = "Password123"

        self.client.post(
            "/api/register",
            json={"username": self.username, "password": self.password},
            name="/api/register",
        )
        self.client.post(
            "/api/login",
            json={"username": self.username, "password": self.password},
            name="/api/login",
        )

    @task(4)
    def get_tasks(self):
        self.client.get("/api/tasks", name="/api/tasks [GET]")

    @task(3)
    def get_dashboard(self):
        self.client.get("/api/dashboard", name="/api/dashboard [GET]")

    @task(2)
    def get_categories(self):
        self.client.get("/api/categories", name="/api/categories [GET]")

    @task(1)
    def create_and_delete_task(self):
        res = self.client.post(
            "/api/tasks",
            json={"title": f"Load test task {uuid.uuid4().hex[:6]}"},
            name="/api/tasks [POST]",
        )
        if res.status_code in (200, 201):
            task_id = res.json().get("id")
            if task_id:
                self.client.delete(
                    f"/api/tasks/{task_id}",
                    name="/api/tasks/<id> [DELETE]",
                )