from cobra.test import Test


class MetaCoin(Test):

    def test_metacoin(self):
        # Get Contract Factory
        metacoin = self.cobra.contract('MetaCoin')
        # Deploying MetaCoin
        metacoin = metacoin.deploy()

        self.assertEqual(metacoin.getBalance(self.cobra.accounts[0]), 10000, "No it's not Equal!")


# def test_metacoin(cobra):
#     # Get Contract Factory
#     metacoin = cobra.contract('MetaCoin')
#     # Deploying MetaCoin
#     metacoin = metacoin.deploy()
#
#     assert metacoin.getBalance(cobra.accounts[0]) == 10000
