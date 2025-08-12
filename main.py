import meraki
import logging
import os

# Set up logging for debug messages
logging.basicConfig(level=logging.DEBUG)

# Get API key from environment variable
API_KEY = os.getenv('MERAKI_DASHBOARD_API_KEY')
if not API_KEY:
	raise EnvironmentError("MERAKI_DASHBOARD_API_KEY environment variable not set.")

dashboard = meraki.DashboardAPI(API_KEY)

# Get organizations the user has access to
organizations = dashboard.organizations.getOrganizations()

# Print organizations in a debug message
logging.debug(f"Organizations accessible to the user: {organizations}")


# Store networks by organization id
org_networks = {}
for org in organizations:
    org_id = org['id']
    networks = dashboard.organizations.getOrganizationNetworks(org_id)
    org_networks[org_id] = networks
    logging.debug(f"Networks for organization {org['name']}: {networks}")


# For each organization, create action batches for every 100 networks to update /networks/{networkId}/settings
for org_id, networks in org_networks.items():
    # Chunk networks into batches of 100
    for i in range(0, len(networks), 100):
        batch = networks[i:i+100]
        actions = []
        for net in batch:
            network_id = net['id']
            # Example action to update network settings (customize as needed)
            actions.append({
                "resource": f"/networks/{network_id}/settings",
                "operation": "update",
                "body": {
                    "localStatusPageEnabled": True,
                    "remoteStatusPageEnabled": True,
                    "localStatusPage": {
                        "authentication": {
                            "enabled": ,
                            "username": "admin",
                            "password": ""
                        }
                    }
                }
            })

        # Submit the action batch as unconfirmed
        response = dashboard.organizations.createOrganizationActionBatch(org_id, actions=actions, confirmed=False)
        logging.debug(f"Prepared UNCONFIRMED action batch for org {org_id} with {len(actions)} networks. Response: {response}")

        # Pause for user confirmation before deleting
        input(f"Press Enter to delete the unconfirmed action batch for org {org_id}...")

        # Cleanup: delete the unconfirmed action batch
        batch_id = response.get('id')
        if batch_id:
            del_response = dashboard.organizations.deleteOrganizationActionBatch(org_id, batch_id)
            logging.debug(f"Deleted unconfirmed action batch {batch_id} for org {org_id}. Response: {del_response}")

        # Debug: confirm action batches were deleted
        final_action_batches = dashboard.organizations.getOrganizationActionBatches(org_id)
        logging.debug(f"Final action batches for org {org_id} after cleanup: {final_action_batches}")
