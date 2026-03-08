from database.connection import get_supabase_client


class TaskService:
    def __init__(self):
        self.client = get_supabase_client()

    def get_tasks(
        self,
        status: str | None = None,
        category_id: str | None = None,
        priority: str | None = None,
        search: str | None = None,
    ) -> list[dict]:
        query = self.client.table("tasks").select(
            "*, categories(name, color), subcategories(name)"
        )
        if status:
            query = query.eq("status", status)
        if category_id:
            query = query.eq("category_id", category_id)
        if priority:
            query = query.eq("priority", priority)
        if search:
            query = query.or_(
                f"title.ilike.%{search}%,description.ilike.%{search}%"
            )
        response = query.order("position").order("created_at", desc=True).execute()
        return response.data

    def create_task(self, data: dict) -> dict:
        max_pos = self._max_position(data.get("status", "todo"))
        data["position"] = max_pos + 1
        response = self.client.table("tasks").insert(data).execute()
        return response.data[0]

    def update_task(self, task_id: str, data: dict) -> dict:
        data["updated_at"] = "now()"
        response = (
            self.client.table("tasks")
            .update(data)
            .eq("id", task_id)
            .execute()
        )
        return response.data[0]

    def delete_task(self, task_id: str) -> None:
        self.client.table("tasks").delete().eq("id", task_id).execute()

    def move_task(self, task_id: str, new_status: str) -> dict:
        max_pos = self._max_position(new_status)
        response = (
            self.client.table("tasks")
            .update({"status": new_status, "position": max_pos + 1, "updated_at": "now()"})
            .eq("id", task_id)
            .execute()
        )
        return response.data[0]

    def _max_position(self, status: str) -> int:
        response = (
            self.client.table("tasks")
            .select("position")
            .eq("status", status)
            .order("position", desc=True)
            .limit(1)
            .execute()
        )
        if response.data:
            return response.data[0]["position"]
        return 0
