from unittest.mock import Mock
import unittest

from src.models.system_user_model import SystemUser
from src.views.user_repository import UserRepository
from src.viewmodels.user_view_model import get_profile_user_details, update_user_login_session


# from my_module import update_user_login_session, session, UserRepository, SystemUser


class TestGetProfileUserDetails(unittest.TestCase):

    def test_update_user_login_session(self):
        # Create a mock session object
        mock_session = {}

        # Create a mock user object
        mock_user = SystemUser(full_name='testuser', email='testuser@example.com', lock=0)

        # Create a mock repository object
        mock_repository = Mock()
        mock_repository.query_update_user.return_value = None

        # Replace the session and user_repository objects with the mock objects
        with unittest.mock.patch('flask.session', mock_session):
            with unittest.mock.patch('my_module.user_repository', mock_repository):
                # Call the method to be tested
                update_user_login_session(mock_user, 'testuser')

                # Assert that the session object has been updated with the username
                self.assertEqual(mock_session['username'], 'testuser')

                # Assert that the user object lock attribute has been updated
                self.assertEqual(mock_user.lock, 1)

                # Assert that the repository method has been called with the user object
                mock_repository.query_update_user.assert_called_once_with(mock_user)

    # def test_get_profile_user_details1(self):
    #     # Create a mock user object to be returned by the repository
    #     mock_user: SystemUser = Mock()
    #     mock_user.full_name = 'johndoe'
    #     mock_user.email = 'johndoe@example.com'
    #
    #     # Create a mock repository object
    #     mock_repository: UserRepository = Mock()
    #     mock_repository.query_system_user.return_value = mock_user
    #
    #     # Replace the user_repository with the mock_repository
    #     with unittest.mock.patch('src.views.user_repository', mock_repository):
    #         # Call the method to be tested
    #         user = get_profile_user_details()
    #
    #         # Assert that the method returns the expected user object
    #         self.assertEqual(user.full_name, 'johndoe')
    #         self.assertEqual(user.email, 'johndoe@example.com')

    def test_get_profile_user_details(self):
        # Define a mock user object to be returned by the repository
        mock_user = SystemUser(full_name='test_user', email='test_user@example.com')

        # Define a mock repository object that returns the mock user object
        class MockUserRepository:
            def query_system_user(self):
                return mock_user

        # Replace the global user_repository object with the mock repository object
        og_user_repository = unittest.mock.Mock(UserRepository())
        user_repository = MockUserRepository()

        # Call the method to be tested
        result = get_profile_user_details()

        # Assert that the result is the mock user object
        self.assertEqual(result, mock_user)

        # Restore the original user_repository object
        user_repository = og_user_repository
