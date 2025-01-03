package client

import (
	"log"
	"net/http"
	"time"

	"github.com/google/uuid"
	"github.com/gorilla/websocket"

	"github.com/shinypantzzz/audiochat/server/internal/room"
)

const (
	pingPeriod     = 10 * time.Second
	maxMessageSize = 16384
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  16384,
	WriteBufferSize: 16384,
}

type Client struct {
	id      uuid.UUID
	room    *room.Room
	conn    *websocket.Conn
	recieve chan []byte
	pong    chan string
}

func NewClient(w http.ResponseWriter, r *http.Request, room *room.Room) (*Client, error) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		return nil, err
	}

	client := Client{
		id:      uuid.New(),
		room:    room,
		conn:    conn,
		recieve: make(chan []byte, 256),
		pong:    make(chan string, 16),
	}

	conn.SetReadLimit(maxMessageSize)
	conn.SetPongHandler(func(s string) error {
		client.pong <- s
		return nil
	})

	room.AddClient(&client)

	go client.listen()
	go client.send()

	return &client, nil
}

func (c *Client) Recieve(message []byte) {
	c.recieve <- message
}

func (c *Client) listen() {
	defer func() {
		c.room.RemoveClient(c)
		c.conn.Close()
	}()

	for {
		_, message, err := c.conn.ReadMessage()
		if err != nil {
			log.Printf("Client.listen: %v\n", err)
			break
		}
		retMessage := []byte{byte(len(c.id[:]))}
		retMessage = append(retMessage, c.id[:]...)
		retMessage = append(retMessage, message...)
		c.room.Broadcast(retMessage, c)
	}
}

func (c *Client) send() {
	ticker := time.NewTicker(pingPeriod)
	defer func() {
		ticker.Stop()
		c.conn.Close()
	}()
	err := c.conn.WriteMessage(websocket.PingMessage, nil)
	if err != nil {
		log.Printf("Client.send: %v\n", err)
		return
	}
	log.Println("Ping sent")

	for {
		for range len(c.recieve) {
			err := c.conn.WriteMessage(websocket.BinaryMessage, <-c.recieve)
			if err != nil {
				log.Printf("Client.send: %v\n", err)
				return
			}
		}
		select {
		case <-ticker.C:
			select {
			case <-c.pong:
				for range len(c.pong) {
					<-c.pong
				}
			default:
				c.conn.WriteMessage(websocket.CloseMessage, nil)
				log.Println("Did not receive pong message")
				return
			}

			err := c.conn.WriteMessage(websocket.PingMessage, nil)
			if err != nil {
				log.Printf("Client.send: %v\n", err)
				return
			}
			log.Println("Ping sent")
		default:

		}
	}
}
