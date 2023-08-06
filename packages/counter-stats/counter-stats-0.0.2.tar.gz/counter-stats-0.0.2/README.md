# counter-stats
A python module for keeping stats.

This repo has been split-off from the 'aacommons' repo at:
    https://github.com/tbastian66/aacommons

## Installation

```
pip install counter-stats
```

## Usage

### CounterEvent

```python
import json
from time import sleep, time

from stats import CounterEvent

stats = CounterEvent(name="ThingsCounter")

# the following loops automatically creates 3 counts split up into 2 different
# groups.
for i in range(0, 10):
    stats.increment('counter1', 'group1', increment=1)
    stats.increment('counter1', 'group1', increment=1)
    stats.increment('counter2', 'group1', increment=1)
    stats.increment('counter2', 'group1', increment=1)
    stats.increment('counter3', 'group2', increment=1)
    sleep(1)

# Get a snapshot of the counters and the group aggregates

# stop_ts needs to be specified as you might have multiple CounterEvent() objects
# that you want to use the same stop timestamp
stop_ts = time()
# Gets a dictionary (munch)
stats_snapshot = stats.snapshot(update_stats=True, stop_ts=stop_ts)
# pretty print the dict
print(json.dumps(stats_snapshot, indent=4))
```

```JSON
{
    "name": "ThingsCounter",
    "original_start_ts": 1654496276.5894873,
    "start_ts": 1654496276.5894873,
    "stop_ts": 1654496286.59915,
    "uptime": 10.01,
    "time_active": 10.01,
    "original_start_time_str": "2022-06-06 14:17:56.589487+0800 (HKT)",
    "start_time_str": "2022-06-06 14:17:56.589487+0800 (HKT)",
    "stop_time_str": "2022-06-06 14:18:06.599150+0800 (HKT)",
    "topic_counts": {
        "group1": {
            "counter1": 20,
            "counter2": 20
        },
        "group2": {
            "counter3": 10
        }
    },
    "group_counts": {
        "group1": 40,
        "group2": 10
    },
    "topic_latest_ts": {
        "group1": {
            "counter1": 1654496285.5980132,
            "counter2": 1654496285.5980191
        },
        "group2": {
            "counter3": 1654496285.5980208
        }
    },
    "group_latest_ts": {
        "group1": 1654496285.5980191,
        "group2": 1654496285.5980208
    },
    "rates": {
        "number_of_topics": {
            "group1": 2,
            "group2": 1
        },
        "interval": 10.01,
        "number_of_groups": 2,
        "topic_rates": {
            "group1": {
                "counter1": 1.998,
                "counter2": 1.998
            },
            "group2": {
                "counter3": 0.999
            }
        },
        "group_rates": {
            "group1": 3.996,
            "group2": 0.999
        },
        "topic_percentage": {
            "group1": {
                "counter1": 0.5,
                "counter2": 0.5
            },
            "group2": {
                "counter3": 1.0
            }
        }
    }
}
```
### CounterTime

### CounterTrio

