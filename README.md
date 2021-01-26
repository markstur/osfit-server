# Call and Crawl Python Server

This Python Flask server provides two REST endpoints.

1. POST a list of phone numbers to call with Twilio
2. POST a URL to crawl for Watson Discovery

## Steps

1. [Create the IBM Cloud services](#create-the-ibm-cloud-services)
2. [Deploy the server](#deploy-the-server)
3. [Use the REST services](#use-the-rest-services)

### Create the IBM Cloud services

Provision the following services:

* **Watson Discovery**
* **Watson Assistant**
* **Db2**

> TODO: Twilio setup

Create the service instances
If you do not have an IBM Cloud account, register for a free trial account <a href="https://cloud.ibm.com/registration">here</a>.

* Click <a href="https://cloud.ibm.com/catalog/services/watson-discovery">here</a> to create a <b>Watson Discovery</b> instance.</li>
* (optional) Click <a href="https://cloud.ibm.com/catalog/services/Db2">here</a> to create a <b>Db2</b> instance.</li>
* (optional) Click <a href="https://cloud.ibm.com/catalog/services/watson-assistant">here</a> to create a <b>Watson Assistant</b> instance.</li>

Gather credentials</h5>
  <ol>
    <li>From the main navigation menu (☰), select <b>Resource list</b> to find your services under <b>Services</b>.</li>
    <li>Click on each service to find the <b>Manage</b> view where you can collect the <b>API Key</b> and <b>URL</b> to use for each service when you configure credentials.
  </ol>

## Deploy the server

Click on one of the options below for instructions on deploying the Node.js server.

[![cf](https://raw.githubusercontent.com/IBM/pattern-utils/master/deploy-buttons/cf.png)](doc/source/cf.md) [![local](https://raw.githubusercontent.com/IBM/pattern-utils/master/deploy-buttons/local.png)](doc/source/local.md)

## License

This code pattern is licensed under the Apache License, Version 2. Separate third-party code objects invoked within this code pattern are licensed by their respective providers pursuant to their own separate licenses. Contributions are subject to the [Developer Certificate of Origin, Version 1.1](https://developercertificate.org/) and the [Apache License, Version 2](https://www.apache.org/licenses/LICENSE-2.0.txt).

[Apache License FAQ](https://www.apache.org/foundation/license-faq.html#WhatDoesItMEAN)
