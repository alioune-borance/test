import unittest
import os
from flask_testing import TestCase
from flask import abort,url_for
from app import create_app,db
from app.models import Employee,Department,Role


class TestBase(TestCase):

    def create_app(self):

        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI = "sqlite:///' + os.path('app.db')"
        )

        return app

    def setUp(self):

        db.create_all()

        admin = Employee(username="test_admin",password="admin",is_admin=True)

        employee = Employee(username="test_user",password="test")

        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()


    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()


class TestModels(TestBase):

    def test_employee_model(self):
        self.assertEqual(Employee.query.count(), 2)

    def test_department_model(self):
        """
        Test number of records in Department table
        """

        # create test department
        department = Department(name="IT", description="The IT Department")

        # save department to database
        db.session.add(department)
        db.session.commit()

        self.assertEqual(Department.query.count(), 1)


    def test_role_model(self):

        role = Role(name="r1",description="desc1")

        db.session.add(role)
        db.session.commit()

        self.assertEqual(Role.query.count(), 1)


class TestViews(TestBase):

    def test_homepage_view(self):
        """
        Test that homepage is accessible without login
        """
        response = self.client.get(url_for("home.homepage"))

        self.assertEqual(response.status_code,200)

    def test_login_view(self):
        """
        Test that login page is accessible without login
        """

        response = self.client.get(url_for("auth.login"))

        self.assertEqual(response.status_code, 200)


    def test_logout_view(self):
        """
        Test that logout link is inaccessible without login
        and redirects to login page then to logout
        """
        target_url = url_for('auth.logout')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_dashboard_view(self):
        """
        Test that dashboard is inaccessible without login
        and redirects to login page then to dashboard
        """
        target_url = url_for('home.dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_admin_dashboard_view(self):
        """
        Test that dashboard is inaccessible without login
        and redirects to login page then to dashboard
        """
        target_url = url_for('home.admin_dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_departments_view(self):
        """
        Test that departments page is inaccessible without login
        and redirects to login page then to departments page
        """
        target_url = url_for('admin.list_departments')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_roles_view(self):
        """
        Test that roles page is inaccessible without login
        and redirects to login page then to roles page
        """
        target_url = url_for('admin.list_roles')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_employees_view(self):
        """
        Test that employees page is inaccessible without login
        and redirects to login page then to employees page
        """
        target_url = url_for('admin.list_employees')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


if __name__ == '__main__':
    unittest.main()