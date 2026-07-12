import json

from django.test import Client, RequestFactory, TestCase

from core.api.views import ApiCrud
from core.models import CustomUser, TreeCategory, WorkSelect
from core.views import Slide


class TreeApiTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.work = WorkSelect.objects.create(name='Engineer')
        self.root = TreeCategory.add_root(name='Root')
        self.child = self.root.add_child(name='Child')
        self.hidden_child = self.root.add_child(name='Hidden child', is_active=False)
        self.hidden_root = TreeCategory.add_root(name='Hidden root', is_active=False)
        self.user = self.create_user('alice', 'Alice', work=self.work)
        self.inactive_user = self.create_user('inactive', 'Inactive', is_active=False)
        self.root.users.add(self.user, self.inactive_user)

    def create_user(self, username, full_name, is_active=True, work=None):
        return CustomUser.objects.create_user(
            username=username,
            password='test-password',
            email=f'{username}@example.com',
            phone='1234567890',
            name_user_full=full_name,
            work=work,
            is_active=is_active,
        )

    def request_json(self, method, path, payload):
        return getattr(self.client, method)(
            path,
            data=json.dumps(payload),
            content_type='application/json',
        )

    def test_tree_endpoint_serializes_active_nodes_and_users(self):
        response = self.client.get('/api/v1/tree')

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]['pk'], f's:{self.root.pk}')
        self.assertEqual(payload[0]['fields'], {'name': 'Root'})
        self.assertEqual(payload[0]['children'][0]['pk'], f'u:{self.user.pk}')
        self.assertEqual(payload[0]['children'][0]['fields']['fullname'], 'Alice')
        self.assertNotIn(f'u:{self.inactive_user.pk}', json.dumps(payload))
        self.assertNotIn(f's:{self.hidden_child.pk}', json.dumps(payload))
        self.assertNotIn(f's:{self.hidden_root.pk}', json.dumps(payload))
        self.assertEqual(payload[0]['tree_children'][0]['fields'], {'name': 'Child'})

    def test_select_endpoint_lists_non_empty_work_names(self):
        WorkSelect.objects.create(name='')

        response = self.client.get('/api/v1/select')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), ['Engineer'])

    def test_post_moves_user_between_categories(self):
        response = self.request_json(
            'post',
            '/api/v1/tree',
            {'tomove': f's:{self.child.pk}', 'target': f'u:{self.user.pk}'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), '301')
        self.assertFalse(self.root.users.filter(pk=self.user.pk).exists())
        self.assertTrue(self.child.users.filter(pk=self.user.pk).exists())

    def test_post_moves_and_deletes_structures(self):
        new_root = TreeCategory.add_root(name='New root')

        move_response = self.request_json(
            'post',
            '/api/v1/tree',
            {'tomove': f's:{self.root.pk}', 'target': f's:{new_root.pk}'},
        )
        delete_struct_response = self.request_json(
            'post',
            '/api/v1/tree',
            {'dalete': True, 'target': f's:{self.child.pk}'},
        )
        delete_user_response = self.request_json(
            'post',
            '/api/v1/tree',
            {'dalete': True, 'target': f'u:{self.user.pk}'},
        )

        self.assertEqual(move_response.json(), '301')
        new_root.refresh_from_db()
        self.assertEqual(new_root.parent, self.root)
        self.assertEqual(delete_struct_response.json(), '301')
        self.child.refresh_from_db()
        self.assertFalse(self.child.is_active)
        self.assertEqual(delete_user_response.json(), '301')
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_post_returns_404_for_missing_object(self):
        response = self.request_json(
            'post',
            '/api/v1/tree',
            {'tomove': 's:9999', 'target': f'u:{self.user.pk}'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), '404')

    def test_put_creates_root_child_and_user_rows(self):
        root_response = self.request_json(
            'put',
            '/api/v1/tree',
            {'type': 's', 'name': 'Created root'},
        )
        child_response = self.request_json(
            'put',
            '/api/v1/tree',
            {'type': 's', 'name': 'Created child', 'parent': f's:{self.root.pk}'},
        )
        user_response = self.request_json(
            'put',
            '/api/v1/tree',
            {'type': 'u', 'username': 'new-user', 'parent': f's:{self.root.pk}'},
        )

        self.assertEqual(root_response.json(), '201')
        created_root = TreeCategory.objects.get(name='Created root')
        self.assertTrue(created_root.users.filter(username=f's{created_root.pk}').exists())
        self.assertEqual(child_response.json(), '201')
        self.assertTrue(self.root.get_children().filter(name='Created child').exists())
        self.assertEqual(user_response.json(), '201')
        self.assertTrue(self.root.users.filter(username='new-user', is_active=True).exists())

    def test_put_rejects_invalid_rows(self):
        root_user_response = self.request_json(
            'put',
            '/api/v1/tree',
            {'type': 'u', 'username': 'orphan-user'},
        )
        missing_parent_response = self.request_json(
            'put',
            '/api/v1/tree',
            {'type': 's', 'name': 'Orphan child', 'parent': 's:9999'},
        )

        self.assertEqual(root_user_response.json(), '400')
        self.assertEqual(missing_parent_response.json(), '400')

    def test_patch_updates_struct_and_user_rows(self):
        struct_response = self.request_json(
            'patch',
            '/api/v1/tree',
            {'pk': f's:{self.root.pk}', 'fields': {'name': 'Renamed root'}},
        )
        user_response = self.request_json(
            'patch',
            '/api/v1/tree',
            {
                'pk': f'u:{self.user.pk}',
                'fields': {
                    'fullname': 'Alice Updated',
                    'email': 'updated@example.com',
                    'phone': '0987654321',
                    'work': 'QA',
                },
            },
        )

        self.assertEqual(struct_response.json(), '201')
        self.root.refresh_from_db()
        self.assertEqual(self.root.name, 'Renamed root')
        self.assertEqual(user_response.json(), '201')
        self.user.refresh_from_db()
        self.assertEqual(self.user.name_user_full, 'Alice Updated')
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(self.user.phone, '0987654321')
        self.assertEqual(self.user.work.name, 'QA')

    def test_patch_rejects_missing_object(self):
        response = self.request_json(
            'patch',
            '/api/v1/tree',
            {'pk': 's:9999', 'fields': {'name': 'Missing'}},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), '400')

    def test_model_helpers_filter_and_serialize_tree(self):
        user_without_work = self.create_user('bob', 'Bob', work=None)
        self.root.users.add(user_without_work)

        self.assertEqual(self.user.get_full_name(), 'Alice')
        self.assertEqual(self.user.get_work(), 'Engineer')
        self.assertEqual(user_without_work.get_work(), '')
        self.assertEqual(self.root.get_json()['pk'], self.root.pk)
        self.assertEqual(
            self.root.get_json_parent([{'pk': self.child.pk}])['category_children'],
            [{'pk': self.child.pk}],
        )
        self.assertNotIn(self.hidden_child, list(self.root.get_children()))
        self.assertEqual(TreeCategory.get_tree(), [self.root])
        self.assertEqual(str(self.root), f'{self.root.pk}:Root')

    def test_vue_app_and_slide_render_template(self):
        response = self.client.get('/')
        slide_response = Slide.as_view(template_name='index.html')(self.factory.get('/slide'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(slide_response.status_code, 200)

    def test_api_view_accepts_request_arguments(self):
        response = ApiCrud.as_view()(self.factory.get('/api/v1/tree'))

        self.assertEqual(response.status_code, 200)
