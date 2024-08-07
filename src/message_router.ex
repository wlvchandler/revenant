defmodule MessageRouter do
  use GenServer

  @port 8080

  def start_link(_) do
    GenServer.start_link(__MODULE__, :ok, name: __MODULE__)
  end

  def init(:ok) do
    {:ok, _} = Application.ensure_all_started(:cowboy)
    
    dispatch = :cowboy_router.compile([
      {:_, [{"/ws", WsHandler, []}]}
    ])
    
    {:ok, _} = :cowboy.start_clear(:http, 
      [port: @port],
      %{env: %{dispatch: dispatch}}
    )

    :ets.new(:connections, [:named_table, :public, {:read_concurrency, true}])

    {:ok, %{}}
  end

  def stop() do
    :cowboy.stop_listener(:http)
  end

  def route_message(service_id, message) do
    case :ets.lookup(:connections, service_id) do
      [{^service_id, pid}] ->
        send(pid, {:send, message})
        :ok

      [] ->
        {:error, :service_not_found}
    end
  end
end
