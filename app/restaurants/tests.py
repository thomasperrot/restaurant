from django.test import TestCase
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, APIClient

from . import models


class RestaurantViewSetTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_restaurant(self) -> None:
        """Assert that users can create restaurants."""

        # when
        response: Response = self.client.post("/restaurants", data={"name": "restaurant_1"}, format="json")

        # then
        assert response.status_code == 201
        restaurant = models.Restaurant.objects.get(pk="restaurant_1")
        assert restaurant.name == "restaurant_1"

    def test_create_already_existing_restaurant(self) -> None:
        """Assert that creating an already existing restaurant returns a 400 error."""

        # given
        models.Restaurant.objects.create(name="restaurant_1")

        # when
        response: Response = self.client.post("/restaurants", data={"name": "restaurant_1"}, format="json")

        # then
        assert response.status_code == 400
        assert response.data == {"name": ["restaurant with this name already exists."]}
        assert models.Restaurant.objects.count() == 1

    def test_create_restaurant_named_random(self) -> None:
        """Assert that users cannot create a restaurant named random."""

        # when
        response: Response = self.client.post("/restaurants", data={"name": "random"}, format="json")

        # then
        assert response.status_code == 400
        assert response.data == {"name": ["restaurant name can not be 'random'."]}
        assert models.Restaurant.objects.count() == 0

    def test_list_restaurants_first_page(self) -> None:
        """Assert that users can list restaurants first."""

        # given
        for i in range(25):
            models.Restaurant.objects.create(name=f"restaurant_{i}")

        # when
        response: Response = self.client.get("/restaurants", format="json")

        # then
        assert response.status_code == 200
        assert response.data == {
            "count": 25,
            "previous": None,
            "next": "http://testserver/restaurants?limit=10&offset=10",
            "results": [{"name": f"restaurant_{i}"} for i in range(10)],
        }

    def test_list_restaurants_any_page(self) -> None:
        """Assert that users can list any restaurant page."""

        # given
        for i in range(25):
            models.Restaurant.objects.create(name=f"restaurant_{i}")

        # when
        response: Response = self.client.get("/restaurants", data={"limit": 10, "offset": 10}, format="json")

        # then
        assert response.status_code == 200
        assert response.data == {
            "count": 25,
            "previous": "http://testserver/restaurants?limit=10",
            "next": "http://testserver/restaurants?limit=10&offset=20",
            "results": [{"name": f"restaurant_{i}"} for i in range(10, 20)],
        }

    def test_delete_restaurants(self) -> None:
        """Assert that users can delete restaurants by name."""

        # given
        models.Restaurant.objects.create(name=f"restaurant_1")

        # when
        response: Response = self.client.delete("/restaurants/restaurant_1", format="json")

        # then
        assert response.status_code == 204
        assert response.data == None

    def test_delete_non_existing_restaurants(self) -> None:
        """Assert that deleting a non existing restaurant returns a 404."""

        # when
        response: Response = self.client.delete(f"/restaurants/restaurant_1", format="json")

        # then
        assert response.status_code == 404
        assert response.data == {"detail": "Not found."}

    def test_get_random_restaurant(self) -> None:
        """Assert that user can retrieve a random restaurant."""

        # given
        names = [f"restaurant_{i}" for i in range(25)]
        for name in names:
            models.Restaurant.objects.create(name=name)

        # when
        response: Response = self.client.get(f"/restaurants/random")

        # then
        assert response.status_code == 200
        assert response.data["name"] in names

    def test_get_random_restaurant_empty_table(self) -> None:
        """Assert that a 404 is returned when asking for random restaurant and table is empty."""

        # when
        response: Response = self.client.get(f"/restaurants/random")

        # then
        assert response.status_code == 404
        assert response.data == {"detail": "No restaurant inserted yet."}

    def test_search_restaurant(self) -> None:
        """Assert that restaurants can be searched by name."""

        # given
        models.Restaurant.objects.create(name=f"Le Petit Chateau")
        models.Restaurant.objects.create(name=f"Le Grand Chateau")

        # when
        response: Response = self.client.get(f"/restaurants", data={"search": "petit"})

        # then
        assert response.status_code == 200
        assert response.data == {"count": 1, "next": None, "previous": None, "results": [{"name": "Le Petit Chateau"}]}
