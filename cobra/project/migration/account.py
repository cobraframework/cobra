# from cobra.project.migration import *
#
# ACCOUNT_TEXT = """Balance: %d
# Address: %s"""
# HDWALLET_TEXT = """Balance: %d
# Address: %s
# Public Key: %s
# Private Key: %s"""
#
#
# # Display account information
# def display_account(web3: Web3,
#                     account=None,
#                     hdwallet=None):
#     if account is not None:
#         console_log(ACCOUNT_TEXT % (web3.eth.getBalance(account['address']),
#                                     web3.toChecksumAddress(account['address'])))
#     elif hdwallet is not None:
#         console_log(HDWALLET_TEXT % (web3.eth.getBalance(hdwallet['address']),
#                                      web3.toChecksumAddress(hdwallet['address']),
#                                      hdwallet['public_key'],
#                                      hdwallet['private_key']))
#     else:
#         console_log(ACCOUNT_TEXT % web3.eth.accounts[0])
