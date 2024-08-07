defmodule WsHandler do
  @behaviour :cowboy_websocket

  def init(req, state) do
    {:cowboy_websocket, req, state}
  end

  def websocket_init(state) do
    {:ok, state}
  end

  def websocket_handle({:text, <<"register:", service_id::binary>>}, state) do
    :ets.insert(:connections, {service_id, self()})
    {:ok, state}
  end

  def websocket_handle({:text, message}, state) do
    case String.split(message, ":") do
      [dest_service_id, payload] ->
        MessageRouter.route_message(dest_service_id, payload)
      _ ->
        Logger.error("Invalid message format: #{message}")
    end
    {:ok, state}
  end

  def websocket_handle(_frame, state) do
    {:ok, state}
  end

  def websocket_info({:send, message}, state) do
    {:reply, {:text, message}, state}
  end

  def websocket_info(_info, state) do
    {:ok, state}
  end

  def terminate(_reason, _req, _state) do
    :ok
  end
end
