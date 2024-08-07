
```
$ rebar clean
$ rebar compile
$ rebar shell
1> code:add_path("/home/will/testcode/router/_build/default/lib/router/ebin").
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