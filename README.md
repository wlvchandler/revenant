
```
$ rebar clean
$ rebar compile
$ rebar shell
1> code:add_path("~/revenant/_build/default/lib/router/ebin").
true
2> c(message_router).
Recompiling /home/will/testcode/router/src/message_router.erl
{ok,message_router}
3> c(ws_handler).
Recompiling /home/will/testcode/router/src/ws_handler.erl
{ok,ws_handler}
4> message_router:start().
ok
```



Simulation output:
```
Script started. Entering main event loop...
Message generator starting...
Attempting to connect to the router...
Connected to the router. Registering as generator...
Registered as generator. Starting message generation...
Messages:1000   Time:1.11s      Rate:904.45 msg/s       Gen (2s):1000   Rate (2s):500.00 msg/s
Messages:2000   Time:2.21s      Rate:905.90 msg/s       Gen (2s):1811   Rate (2s):905.50 msg/s
Messages:3000   Time:3.31s      Rate:906.02 msg/s       Gen (2s):1813   Rate (2s):906.50 msg/s
Messages:4000   Time:4.42s      Rate:905.15 msg/s       Gen (2s):1810   Rate (2s):905.00 msg/s
Messages:5000   Time:5.53s      Rate:904.93 msg/s       Gen (2s):1808   Rate (2s):904.00 msg/s
Messages:6000   Time:6.63s      Rate:905.15 msg/s       Gen (2s):1809   Rate (2s):904.50 msg/s
```

```
$ ./start.sh  | grep --line-buffered Enricher
[Enricher] Registered as enricher
[Enricher] Received raw message: {"id": 658227, "content": "Message 788"}
[Enricher] Enriched and sent: {'id': 658227, 'content': 'Message 788', 'timestamp': 605316.976156269, 'enriched_value': 0.31314470635832237}
[Enricher] Received raw message: {"id": 27680, "content": "Message 156"}
[Enricher] Enriched and sent: {'id': 27680, 'content': 'Message 156', 'timestamp': 605316.97839979, 'enriched_value': 0.17207572793261938}
[Enricher] Received raw message: {"id": 72704, "content": "Message 690"}
[Enricher] Enriched and sent: {'id': 72704, 'content': 'Message 690', 'timestamp': 605316.980656146, 'enriched_value': 0.6122989876872176}
```