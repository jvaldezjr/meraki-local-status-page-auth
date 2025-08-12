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