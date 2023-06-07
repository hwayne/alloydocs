sig Server {}

sig Client {
  , var connected_to: lone Server
}

pred connect[c: Client, s: Server] {
  c -> s not in connected_to
  connected_to' = connected_to ++ c -> s
}

pred spec {
  -- initially no connections
  no connected_to

  -- every step, a client connects to a new server
  always some c: Client, s: Server {
    c.connect[s]
  }
}

run spec