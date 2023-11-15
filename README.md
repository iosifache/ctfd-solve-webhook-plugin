# `ctfd-solve-webhook-plugin`

## Description

`ctfd-solve-webhook-plugin` is a CTFd plugin for calling a webhook when a challenge is solved. HTTP GET requests are used.

In addition, the repository provides [predefined webhooks](#predefined-webhooks) which can be set up separately and called from the CTFd plugin.

## Predefined webhooks

| Identifier   | Purpose                                           |
| ------------ | ------------------------------------------------- |
| `mattermost` | Sends Mattermost messages to a specified channel. |

## Configuration

### Changing the configuration

They can be changed either by setting up some environment variables or using the plugin webpage which is available after installing the plugin. The latter can be accessed by clicking the "Plugins" button in the admin panel and selecting "Solve Webhook" from the dropdown list.

![Plugin configuration webpage](/others/screenshot.png)

### Available aspects

The configuration is composed of the following aspects:

| Description                                                                                                                 | Environment variable            | Type                           | Scope              | Mandatory        | UI editable |
| --------------------------------------------------------------------------------------------------------------------------- | ------------------------------- | ------------------------------ | ------------------ | ---------------- | ----------- |
| URL of the webhook                                                                                                          | `SOLVE_WEBHOOK_URL`             | String representing a URL      | CTFd plugin        | Yes              | Yes         |
| Maximum number of players for which the webhook is called                                                                   | `SOLVE_WEBHOOK_LIMIT`           | String representing an integer | CTFd plugin        | No               | Yes         |
| Boolean indicating if the Mattermost sender is a user (with incoming webhooks) or a bot                                     | `MATTERMOST_WEBHOOK_IS_BOT`     | `0` (false) or `1` (true)      | Mattermost webhook | Yes              | No          |
| [Mtttermost bot token](https://developers.mattermost.com/integrate/reference/bot-accounts/)                                 | `MATTERMOST_WEKHOOK_BOT_TOKEN`  | String                         | Mattermost webhook | If a bot is used | No          |
| Mattermost API Posts URL (if bot) or [incoming webhook URL](https://developers.mattermost.com/integrate/webhooks/incoming/) | `MATTERMOST_WEBHOOK_URL`        | String representing a URL      | Mattermost webhook | Yes              | No          |
| Mattermost channel ID in which the messages will be sent                                                                    | `MATTERMOST_WEBHOOK_CHANNEL`    | String                         | Mattermost webhook | Yes              | No          |
| Mattermost username from which the messages will be sent                                                                    | `MATTERMOST_WEBHOOK_USERNAME`   | String                         | Mattermost webhook | No               | No          |
| Icon accompanying each Mattermost message                                                                                   | `MATTERMOST_WEBHOOK_ICON_EMOJI` | String                         | Mattermost webhook | No               | No          |
| Custom authentication token for the Mattermost webhook                                                                      | `MATTERMOST_WEBHOOK_AUTH_TOKEN` | String                         | Mattermost webhook | Yes              | No          |

## Setup

All approaches described below require the repository to be cloned locally.

### Testing the plugin with Docker Compose

1. Change [the configuration aspects](#available-aspects) in `docker-compose.yaml`. At least `SOLVE_WEBHOOK_URL` should be populated with a URL, as it is empty by default.
2. Run `docker-compose --profile ctfd up --build --detach` from the root of this repository.
3. Optionally, you can see the logs of all services by using `docker-compose logs --follow`.

### Installing the plugin in an already-existent CTFd instance

1. Copy the entire `solve-webhook-plugin` folder in `<ctfd_installation_path>/CTFd/plugins/`, where `<ctfd_installation_path>` is the path in which you have installed CTFd.
2. If you have privileges on the system in which the CTFd instance is installed, set up [the environment variables ](#available-aspects). Otherwise, access the 

### Setting up a predefined webhook with Docker Compose

1. Change [the configuration aspects](#available-aspects) specific to the webhook in `docker-compose.yaml`.
2. Run `docker-compose --profile <webhook_id> up --build --detach` from the root of this repository, where `<webhook_id>` is the identifier of the plugin as mentioned in [the above table](#predefined-webhooks).

### Setting up a predefined webhook with Docker

1. Enter the `webhooks/<webhook_id>` folder, where `<webhook_id>` is the identifier of the plugin, as mentioned in [the above table](#predefined-webhooks).
2. Change the value of each `ENV`. Use [the above table with configuration aspects](#available-aspects) to understand what values should be set.
3. Use the `Dockerfile` and accompanying file from the folder in your usual process for setting up the infrastructure.

## Custom webhooks

## HTTP contract

The requests that the webhooks receive are defined in a Swagger file, [swagger.yaml](/webhooks/swagger.yaml). To visualize it, you can use [an online editor](https://editor.swagger.io/) or [Visual Studio Code extension](https://marketplace.visualstudio.com/items?itemName=Arjun.swagger-viewer).

## Authentication

At the moment, the single way to authenticate the plugin to a webhook is by leveraging the `GET` parameters.

For example, if you are creating a custom webhook (hosted at `<your_url>`), populate `SOLVE_WEBHOOK_URL` with `<your_url>/?token=<auth_token>` and implement a logic in the webhook to verify if the `token` parameter is set and has the value `<auth_token>`.
