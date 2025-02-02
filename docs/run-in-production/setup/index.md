---
# description: >-
icon: display
---

# qyver Server

The qyver server is designed to be used by end users who want to leverage the power of qyver in deployable projects. With a simple command, you can run a qyver-powered app instance that creates REST endpoints and connects to external Vector Databases. This makes it an ideal solution for those seeking an easy-to-deploy environment for their qyver projects.

## Prerequisites

Before you can use this environment, you need to have:

1. Python 3.11 or higher installed with pip and venv modules. You can download Python from [here](https://www.python.org/downloads/).
2. A Python virtual environment created and activated in a dedicated project folder of your choice.
3. Install the qyver-server library: `pip install qyver-server`

*Note: The following documentation uses Unix-based terminal commands. Compatibility with other operating systems has not been verified.*

## How to start the application

To start the application follow the steps below:

1. **Create the qyver app folder**: Create a directory to store your qyver configuration files by running `mkdir qyver_app`. For a minimal working example, copy the [app.py](https://github.com/qyver/qyver/blob/main/docs/run-in-production/example/app.py) into your newly created `qyver_app` directory. For more advanced use cases, please read the next section below.

2. **Start the qyver server**: To start the server run the `python -m qyver.server` command.

By default, this will start the server on port 8080 (configurable via the `SERVER_PORT` environment variable) and expose the API endpoints for use. You can verify the server is running by visiting http://localhost:8080/docs in your browser.

## Configuring and Customizing Your Application

Once your server is running, you'll need to configure and integrate your application. There are two main aspects to focus on:
- [Application Configuration Guide](configuring-your-app.md) - Learn how to structure and customize your application
- [API Integration Guide](interacting-with-app-via-api.md) - Understand how to interact with your application through the REST API

Click on either link above for detailed documentation on each aspect.

## Support

If you encounter any issues while using this environment, please open an issue in this repository and we will do our best to help you.
