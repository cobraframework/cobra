# using UNITTEST
from cobra.test import Test


class Greeter(Test):

    def test_greeter(self):
        # Get Greeter Contract Factory
        greeter = self.cobra.contract('Greeter')
        # Deploying Greeter
        greeter = greeter.deploy()

        self.assertEqual(greeter.greet(), "Hello", "Oops! Not Equal.")


# # using PYTEST
# def test_greeter(cobra):
#     # Get Greeter Contract Factory
#     greeter = cobra.contract('Greeter')
#     # Deploying Greeter
#     greeter = greeter.deploy()
#
#     assert greeter.greet() == "Hello" "Oops! Not Equal."
