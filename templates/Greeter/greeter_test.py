# using UNITTEST
from cobra.test import Test


class Greeter(Test):

    def test_greeter(self):
        # Getting contract factory by name(Greeter)
        greeter = self.cobra.contract('Greeter')
        # Getting contract instance of Greeter
        greeter = greeter.deploy()

        self.assertEqual(greeter.greet(), "Hello", "Oops! Not Equal.")


# # using PYTEST
# def test_greeter(cobra):
#     # Getting contract factory by name(Greeter)
#     greeter = cobra.contract('Greeter')
#     # Getting contract instance of Greeter
#     greeter = greeter.deploy()
#
#     assert greeter.greet() == "Hello" "Oops! Not Equal."
