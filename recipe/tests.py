from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Recipe, Category
from datetime import timedelta

class RecipeViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        # Creating test objects for categories and recipes
        self.category1 = Category.objects.create(name='Test Category 1')
        self.category2 = Category.objects.create(name='Test Category 2')

        self.recipe1 = Recipe.objects.create(
            title='Recipe 1',
            description='Description for Recipe 1',
            instructions='Instructions for Recipe 1',
            ingredients='Ingredients for Recipe 1',
            created_at=timezone.now() - timedelta(days=1),
            category=self.category1
        )

        self.recipe2 = Recipe.objects.create(
            title='Recipe 2',
            description='Description for Recipe 2',
            instructions='Instructions for Recipe 2',
            ingredients='Ingredients for Recipe 2',
            created_at=timezone.now(),
            category=self.category2
        )

    def test_main_view(self):
        url = reverse('main')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
        # Checking that the page contains a list of recipes
        self.assertTrue('recipes' in response.context)
        # Checking that no more than 10 recipes are displayed
        self.assertLessEqual(len(response.context['recipes']), 10)

    def test_category_detail_view(self):
        url = reverse('category_detail', args=[self.category1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category_detail.html')
        # Checking that the page contains a category and a list of recipes from that category
        self.assertTrue('category' in response.context)
        self.assertTrue('recipes' in response.context)
        self.assertEqual(response.context['category'], self.category1)
        self.assertEqual(list(response.context['recipes']), [self.recipe1])

    def test_recipe_detail_view(self):
        url = reverse('recipe_detail', args=[self.recipe1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe_detail.html')
        # Checking that the page contains details of one recipe
        self.assertTrue('recipe' in response.context)
        self.assertEqual(response.context['recipe'], self.recipe1)
