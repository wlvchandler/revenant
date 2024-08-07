
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
$ ./start.sh  | grep --line-buffered Enricher
[Enricher] Registered as enricher
[Enricher] Received raw message: {"id": 658227, "content": "Message 788"}
[Enricher] Enriched and sent: {'id': 658227, 'content': 'Message 788', 'timestamp': 605316.976156269, 'enriched_value': 0.31314470635832237}
[Enricher] Received raw message: {"id": 27680, "content": "Message 156"}
[Enricher] Enriched and sent: {'id': 27680, 'content': 'Message 156', 'timestamp': 605316.97839979, 'enriched_value': 0.17207572793261938}
[Enricher] Received raw message: {"id": 72704, "content": "Message 690"}
[Enricher] Enriched and sent: {'id': 72704, 'content': 'Message 690', 'timestamp': 605316.980656146, 'enriched_value': 0.6122989876872176}
```