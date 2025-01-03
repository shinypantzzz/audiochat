package room

type Client interface {
	Recieve(message []byte)
}

type Message struct {
	client  Client
	message []byte
}

type Room struct {
	clients   map[Client]bool
	broadcast chan Message
}

func NewRoom() *Room {
	room := Room{
		clients:   make(map[Client]bool),
		broadcast: make(chan Message, 1024),
	}
	go room.run()
	return &room
}

func (r *Room) AddClient(client Client) {
	r.clients[client] = true
}

func (r *Room) RemoveClient(client Client) {
	delete(r.clients, client)
}

func (r *Room) run() {
	for {
		if message, ok := <-r.broadcast; ok {
			for client := range r.clients {
				if message.client == client {
					continue
				}
				client.Recieve(message.message)
			}
		}
	}
}

func (r *Room) Broadcast(message []byte, client Client) {
	r.broadcast <- Message{
		client:  client,
		message: message,
	}
}
