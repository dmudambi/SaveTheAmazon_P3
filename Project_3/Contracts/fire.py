import requests
import json
from pathlib import Path
from web3.auto import w3
import sys

landfax_address = "0xA955Edf5D9C4D273B03975a8150Df81bf0022C4c"

def initContract():
    with open(Path("LandFax.json")) as json_file:
        abi = json.load(json_file)

    return w3.eth.contract(address=landfax_address, abi=abi)

landfax = initContract()

# function to enter fire information
def createFireReport():
    token_id = int(input("Token ID: "))

    return token_id

def reportFire(token_id):
    txn_hash = landfax.functions.reportFire(token_id).transact({"from": w3.eth.accounts[0]})
    txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)

    return txn_receipt

def getFireReports(token_id):
    fire_filter = landfax.events.fire.createFilter(
        fromBlock="0x0", argument_filters={"token_id": token_id}
    )
    return fire_filter.get_all_entries()


def main():
    if sys.argv[1] == "report":
        token_id = createFireReport()
        receipt = reportFire(token_id)

        print(receipt)
        print("Had a Fire:", token_id)

    elif sys.argv[1] == "get":
        token_id = int(sys.argv[1])
        land = landfax.functions.lands(token_id).call()
        reports = getFireReports(token_id)

        print(reports)
        print("Lat/Lon", land[0], "has had a fire.")


main()








