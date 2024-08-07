#!/usr/bin/env escript
%%! -sname router_node

main(_) ->
    true = code:add_path("./_build/default/lib/router/ebin")
    message_router:start(),
    timer:sleep(infinity)