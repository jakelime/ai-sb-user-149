# Guide to setup gcloud stuffs on your local environment

## Configure ADC with your Google Account

To configure ADC with a Google Account, you use the Google Cloud CLI:

Install and initialize the gcloud CLI.

When you initialize the gcloud CLI, be sure to specify a Google Cloud project in which you have permission to access the resources your application needs.

Configure ADC:

```shell
gcloud auth application-default login
A sign-in screen appears. After you sign in, your credentials are stored in the local credential file used by ADC.
```
