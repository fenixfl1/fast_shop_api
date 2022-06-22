# categories controller

class CategoriesController:
    def __init__(self, categories_service):
        self.categories_service = categories_service

    def get_categories(self):
        return self.categories_service.get_categories()

    def get_category(self, category_id):
        return self.categories_service.get_category(category_id)

    def create_category(self, category):
        return self.categories_service.create_category(category)

    def update_category(self, category_id, category):
        return self.categories_service.update_category(category_id, category)

    def delete_category(self, category_id):
        return self.categories_service.delete_category(category_id)
