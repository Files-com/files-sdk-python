# FrontendMetric

## Example FrontendMetric Object

```
{
  "metric_type": "increment",
  "subkey": "abc123",
  "ms": 100
}
```

* `metric_type` (string): Statsd metric type
* `subkey` (string): Where in statsd to store the metric. The final key in statsd will be `files-react.[environment].[subkey]`
* `ms` (int64): For timing metrics, the number of milliseconds. Required if `metric_type` is `timing`.


---

## Submit Frontend Metric data

```
files_sdk.frontend_metric.create({
  "metric_type": "metric_type",
  "subkey": "abc123",
  "ms": 100
})
```

### Parameters

* `metric_type` (string): Required - Statsd metric type.  Use `timing` to submit the amount of time something took, or `increment` to increment a counter
* `subkey` (string): Required - Where in statsd to store the metric. The final key in statsd will be `files-react.[environment].[subkey]`
* `ms` (int64): For timing metrics, the number of milliseconds. Required if `metric_type` is `timing`.
