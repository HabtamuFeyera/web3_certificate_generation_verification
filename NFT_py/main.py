import json
import hashlib
import os
from algosdk import mnemonic
from algosdk.v2client import algod
from algosdk.v2client import algod
from algosdk import mnemonic
from create_account import create_account
from closeout_account import closeout_account
from tkinter.messagebox import YES


def create_non_fungible_token():
    # Create an account for NFT creation
    print("Creating account...")
    accounts = {}
    m = create_account()
    accounts[1] = {
        'pk': mnemonic.to_public_key(m),
        'sk': mnemonic.to_private_key(m)
    }

    # Configure Algorand node connection
    algod_token = "YOUR_ALGOD_TOKEN"
    algod_address = "YOUR_ALGOD_ADDRESS"
    algod_client = algod.AlgodClient(algod_token, algod_address)

    # Load metadata from JSON file
    print("Reading metadata...")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 'NFT', 'metadata.json'), 'r') as f:
        metadataJSON = json.loads(f.read())
        metadataStr = json.dumps(metadataJSON)

    # Generate metadata hash
    print("Generating metadata hash...")
    hash = hashlib.new("sha512_256")
    hash.update(b"arc0003/amj")
    hash.update(metadataStr.encode("utf-8"))
    json_metadata_hash = hash.digest()

    # Create an Algorand asset
    print("Creating Asset...")
    params = algod_client.suggested_params()
    txn = AssetConfigTxn(
        sender=accounts[1]['pk'],
        sp=params,
        total=1,
        default_frozen=False,
        unit_name="ALICE001",
        asset_name="Alice's Artwork 001",
        manager=accounts[1]['pk'],
        strict_empty_address_check=False,
        url="https://path/to/my/asset/details",
        metadata_hash=json_metadata_hash,
        decimals=0
    )

    # Sign the transaction with the creator's private key
    stxn = txn.sign(accounts[1]['sk'])

    # Send the transaction to the network and retrieve the transaction ID
    txid = algod_client.send_transaction(stxn)
    print("Asset Creation Transaction ID:", txid)

    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("Transaction confirmed in round:", confirmed_txn['confirmed-round'])

    try:
        # Get asset information from the creator's account
        ptx = algod_client.pending_transaction_info(txid)
        asset_id = ptx["asset-index"]
        print_created_asset(algod_client, accounts[1]['pk'], asset_id)
        print_asset_holding(algod_client, accounts[1]['pk'], asset_id)
    except Exception as e:
        print(e)

    # Destroy the created asset
    print("Deleting Asset...")
    txn = AssetConfigTxn(
        sender=accounts[1]['pk'],
        sp=params,
        index=asset_id,
        strict_empty_address_check=False
    )

    # Sign the transaction with the creator's private key
    stxn = txn.sign(accounts[1]['sk'])

    # Send the transaction to the network and retrieve the transaction ID
    txid = algod_client.send_transaction(stxn)
    print("Asset Destroy Transaction ID:", txid)

    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("Transaction confirmed in round:", confirmed_txn['confirmed-round'])

    try:
        print_asset_holding(algod_client, accounts[1]['pk'], asset_id)
        print_created_asset(algod_client, accounts[1]['pk'], asset_id)
        print("Asset is deleted.")
    except Exception as e:
        print(e)

    # Closeout the account
    print("Sending closeout transaction back to the testnet dispenser...")
    closeout_account(algod_client, accounts[1])

# Utility function used to print created asset for account and assetid
def print_created_asset(algodclient, account, assetid):
    account_info = algodclient.account_info(account)
    for my_account_info in account_info['created-assets']:
        if my_account_info['index'] == assetid:
            print("Asset ID:", my_account_info['index'])
            print(json.dumps(my_account_info['params'], indent=4))
            break

# Utility function used to print asset holding for account and assetid
def print_asset_holding(algodclient, account, assetid):
    account_info = algodclient.account_info(account)
    for my_account_info in account_info['assets']:
        if my_account_info['asset-id'] == assetid:
            print("Asset ID:", my_account_info['asset-id'])
            print(json.dumps(my_account_info, indent=4))
            break

# Run the NFT creation script
create_non_fungible_token()
