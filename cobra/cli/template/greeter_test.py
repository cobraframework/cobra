from cobra.test import Test


class Greeter(Test):

    def test_greeter(self):
        # Get Greeter Contract Factory
        greeter = self.cobra.contract('Greeter')
        # Deploying Greeter
        greeter = greeter.deploy()

        self.assertEqual(greeter.greet(), "Hello", "No it's not Equal!")

# def test_metacoin(cobra):
#     # Get Contract Factory
#     greeter = cobra.contract('MetaCoin')
#     # Deploying MetaCoin
#     greeter = greeter.deploy()
#
#     assert greeter.greet() == "Hello"
