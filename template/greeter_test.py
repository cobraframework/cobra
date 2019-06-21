# by UNITTEST
from cobra.test import Test


class Greeter(Test):

    def test_greeter(self):
        # Get Greeter Contract Factory
        greeter = self.cobra.contract('Greeter')
        # Deploying Greeter
        greeter = greeter.deploy()

        self.assertEqual(greeter.greet(), "Hello", "Oops! Not Equal.")


# # by PYTEST
# def test_greeter(cobra):
#     # Get Contract Factory
#     greeter = cobra.contract('Greeter')
#     # Deploying MetaCoin
#     greeter = greeter.deploy()
#
#     assert greeter.greet() == "Hello" "Oops! Not Equal."
