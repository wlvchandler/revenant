-module(message_router).
-export([start/0, stop/0, route_message/2]).

-define(SERVER, ?MODULE).

start() ->
    {ok, _} = application:ensure_all_started(cowboy),
    Dispatch = cowboy_router:compile([
        {'_', [{"/ws", ws_handler, []}]}
    ]),
    {ok, _} = cowboy:start_clear(?SERVER,
        [{port, 8080}],
        #{env => #{dispatch => Dispatch}}
    ),
    ets:new(connections, [named_table, public, {read_concurrency, true}]),
    ok.

stop() ->
    cowboy:stop_listener(?SERVER).

route_message(ServiceId, Message) ->
    case ets:lookup(connections, ServiceId) of
        [{ServiceId, Pid}] ->
            Pid ! {send, Message},
            ok;
        [] ->
            {error, service_not_found}
    end.
