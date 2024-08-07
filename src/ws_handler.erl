-module(ws_handler).
-behavior(cowboy_websocket).

-export([init/2, websocket_init/1, websocket_handle/2, websocket_info/2, terminate/3]).

init(Req, State) ->
    {cowboy_websocket, Req, State}.

websocket_init(State) ->
    {ok, State}.

websocket_handle({text, <<"register:", ServiceId/binary>>}, State) ->
    ets:insert(connections, {ServiceId, self()}),
    {ok, State};

websocket_handle({text, Message}, State) ->
    % Parse the message and route it to the appropriate service
    case binary:split(Message, <<":">>) of
        [DestServiceId, Payload] ->
            message_router:route_message(DestServiceId, Payload);
        _ ->
            error_logger:error_msg("Invalid message format: ~p", [Message])
    end,
    {ok, State};

websocket_handle(_Frame, State) ->
    {ok, State}.

websocket_info({send, Message}, State) ->
    {reply, {text, Message}, State};

websocket_info(_Info, State) ->
    {ok, State}.

terminate(_Reason, _Req, _State) ->
    ok.
