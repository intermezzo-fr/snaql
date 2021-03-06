# coding: utf-8
import os
from snaql.factory import Snaql
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestUseCases(unittest.TestCase):

    def setUp(self):
        self.sql_root = os.path.abspath(os.path.dirname(__file__))
        self.snaql = Snaql(self.sql_root, 'queries')

    def test_usual_case(self):
        users_queries = self.snaql.load_queries('users.sql')
        self.assertEqual(
            users_queries.users_by_country(), (
                "SELECT count(*) AS count "
                "FROM user "
                "WHERE country_code = ?"
            )
        )
        self.assertEqual(
            users_queries.select_all(), (
                "SELECT * "
                "FROM user"
            )
        )

    def test_subrendering(self):
        users_queries = self.snaql.load_queries('users.sql')

        self.assertEqual(
            users_queries.users_count_cond(), (
                "SELECT count(*) AS count "
                "FROM user"
            )
        )
        context = {'by_country': True, 'country_code': 42}
        self.assertEqual(
            users_queries.users_count_cond(**context), (
                "SELECT count(*) AS count "
                "FROM user  "
                "WHERE country_code = 42 "
            )
        )

    def test_complex_subrendering(self):
        users_queries = self.snaql.load_queries('users.sql')

        context = {'users_ids': [1, 2, 3]}
        self.assertEqual(
            users_queries.users_select_cond(**context), (
                "SELECT * "
                "FROM user  "
                "WHERE user_id IN (1, 2, 3) "
            )
        )

    def test_escaping(self):
        users_queries = self.snaql.load_queries('users.sql')

        context = {'user_name': "'semirook';"}
        self.assertEqual(
                users_queries.users_escaping(**context), (
                "SELECT * FROM user  "
                "WHERE user_name = \\'semirook\\'; "
            )
        )

    def test_clean_env(self):
        users_queries = self.snaql.load_queries('users.sql')
        self.assertEqual(
            users_queries.select_all(), (
                "SELECT * "
                "FROM user"
            )
        )
        self.assertFalse(self.snaql.jinja_env.sql_params)

    def test_multiple_ns(self):
        users_queries = self.snaql.load_queries('users.sql')
        news_queries = self.snaql.load_queries('news.sql')
        self.assertEqual(
            users_queries.select_all(), (
                "SELECT * "
                "FROM user"
            )
        )
        self.assertEqual(
            news_queries.select_all(), (
                "SELECT * "
                "FROM news"
            )
        )
