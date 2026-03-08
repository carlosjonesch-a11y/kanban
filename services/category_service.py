from database.connection import get_supabase_client


class CategoryService:
    def __init__(self):
        self.client = get_supabase_client()

    # ---- Categorias ----

    def get_all_categories(self) -> list[dict]:
        response = self.client.table("categories").select("*").order("name").execute()
        return response.data

    def get_category_by_id(self, category_id: str) -> dict | None:
        response = (
            self.client.table("categories")
            .select("*")
            .eq("id", category_id)
            .single()
            .execute()
        )
        return response.data

    # ---- Subcategorias ----

    def get_subcategories(self, category_id: str | None = None) -> list[dict]:
        query = self.client.table("subcategories").select("*, categories(name, color)")
        if category_id:
            query = query.eq("category_id", category_id)
        response = query.order("name").execute()
        return response.data

    def create_subcategory(self, name: str, category_id: str) -> dict:
        response = (
            self.client.table("subcategories")
            .insert({"name": name, "category_id": category_id})
            .execute()
        )
        return response.data[0]

    def update_subcategory(self, subcategory_id: str, name: str) -> dict:
        response = (
            self.client.table("subcategories")
            .update({"name": name})
            .eq("id", subcategory_id)
            .execute()
        )
        return response.data[0]

    def delete_subcategory(self, subcategory_id: str) -> None:
        self.client.table("subcategories").delete().eq("id", subcategory_id).execute()
