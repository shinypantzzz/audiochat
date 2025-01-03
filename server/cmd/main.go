package main

import (
	"audiochat/server/internal/client"
	"audiochat/server/internal/room"
	"log"
	"net/http"
)

func main() {
	rooms := make(map[string]*room.Room)

	http.HandleFunc("/connect", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "GET" {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}
		room_name := r.URL.Query().Get("room")
		if room_name == "" {
			http.Error(w, "Room is required", http.StatusBadRequest)
			return
		}
		room, ok := rooms[room_name]
		if !ok {
			http.Error(w, "Room does not exist", http.StatusNotFound)
			return
		}
		_, err := client.NewClient(w, r, room)
		if err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}
	})

	http.HandleFunc("/create_room", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "POST" {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}
		if err := r.ParseForm(); err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}
		room_name := r.PostForm.Get("name")
		if room_name == "" {
			http.Error(w, "Room name is required", http.StatusBadRequest)
			return
		}
		if _, ok := rooms[room_name]; ok {
			http.Error(w, "Room already exists", http.StatusConflict)
			return
		}
		room := room.NewRoom()
		rooms[room_name] = room
		log.Printf("Created room %s", room_name)

		w.Write(nil)
	})
	http.ListenAndServe("0.0.0.0:80", nil)
}
