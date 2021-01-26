# Run locally

This document shows how to run the server on your local machine.

## Steps

1. [Clone the repo](#clone-the-repo)
1. [Configure credentials](#configure-credentials)
1. [Start the server](#start-the-server)

### Clone the repo

Clone the git repo locally. In a terminal, run:

```bash
git clone https://github.com/markstur/osfit-server
cd osfit-server
```

### Configure credentials

Copy the **env.sample** file to **.env**.

```bash
cp env.sample .env
```

Edit the **.env** file to configure credentials before starting the server.

```bash
#----------------------------------------------------------
# Copy this file to `.env`.
# Uncomment and configure each runtime setting.
# In general, missing configuration will result in skipping
# functionality (can be used for testing).
#----------------------------------------------------------

# Your Account SID from twilio.com/console
# Your Auth Token from twilio.com/console
# Your Twilio phone number to place calls from
TWILIO_ACCOUNT_SID=<add_twilio-account-sid>
TWILIO_AUTH_TOKEN=<add_twilio-auth-token>
TWILIO_PHONE_NUMBER=<add_twilio-phone-number>

# Configurable range for random delay between calls (seconds):
CALL_SLEEP_MIN=5
CALL_SLEEP_MAX=15

# Watson Discovery
# Crawl results are fed to discovery (skipped if not configured).
DISCOVERY_APIKEY=<add_watson-discovery-apikey>
DISCOVERY_URL=<add_watson-discovery-url>
DISCOVERY_COLLECTION_ID=<add_watson-discovery-collection-id>
DISCOVERY_ENVIRONMENT_ID=<add_watson-discovery-environment-id>

# Db2
# Call and crawl history is tracked in Db2 (skipped if not configured).
DB_USERNAME=<add_db2-username>
DB_PASSWORD=<add_db2-password>
DB_HOST=<add_db2-host>
DB_DATABASE=BLUDB
DB_PORT=50000

```

</p>
</details>

### Prerequisites

Your Python environment needs:

* Python 3.8 or later
* [pip](https://pip.pypa.io/en/stable/installing/)
* pipenv (`pip install --user pipenv`)

### Start the server

```bash
pipenv install
pipenv shell
python app.py
```

> Note: Use CTRL-C to kill it.

The server will be available in your browser at http://localhost:8080.  Return to the README.md for instructions on how to use the app.

[![return](https://raw.githubusercontent.com/IBM/pattern-utils/master/deploy-buttons/return.png)](https://github.com/markstur/osfit-server#use-the-rest-services)
