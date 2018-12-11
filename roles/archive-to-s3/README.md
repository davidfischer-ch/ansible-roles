# Role archive-to-s3

## Status

Preview

## Setup

### Datadog Logs Ingestion

https://docs.datadoghq.com/logs/faq/why-do-my-logs-not-have-the-expected-timestamp/

Further explanations from Datadog support:

In order to get the correct date in your case, you need to redefine some rules in your pipelines.

For your python logs, the date is being processed from the log itself, the difference you are seeing
is due to the missing timezone parameter. You need to replace %{date("yyyy-MM-dd'T'HH:mm:ss.SSS")
with this format: %{date("yyyy-MM-dd'T'HH:mm:ss.SSSZ").

https://cl.ly/db7d8429776b

You might also need to update the date remapper, replace timestamp by time:

https://cl.ly/f7527446462f

Please note that the default pipelines (Nginx, Python...) can't be modified directly, you need to
clone them and disable the original ones(to avoid duplication), and then work with the cloned
pipelines. You can read more about processing rules for logs here:

https://docs.datadoghq.com/logs/processing/parsing/?tab=matcher#pagetitle
