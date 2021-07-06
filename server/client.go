// Copyright 2013 The Gorilla WebSocket Authors. All rights reserved.
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file.

package server

import (
	"Websocket-chat/Protobuf"
	"Websocket-chat/db"
	"google.golang.org/protobuf/proto"
	"log"
	"net/http"
	"time"

	_ "Websocket-chat/Protobuf"
	_ "Websocket-chat/db"
	"github.com/gorilla/websocket"
)

const (
	// Time allowed to write a message to the peer.
	writeWait = 10 * time.Second

	// Time allowed to read the next pong message from the peer.
	pongWait = 60 * time.Second

	// Send pings to peer with this period. Must be less than pongWait.
	pingPeriod = (pongWait * 9) / 10

	// Maximum message size allowed from peer.
	maxMessageSize = 512
)

var (
	Newline = []byte{'\n'}
	Space   = []byte{' '}
)

var Upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

// Client is a middleman between the websocket connection and the hub.
type Client struct {
	Hub *Hub

	Username string
	// The websocket connection.
	Conn *websocket.Conn

	// Buffered channel of outbound messages.
	Send chan []byte
}

// readPump pumps messages from the websocket connection to the hub.
//
// The application runs readPump in a per-connection goroutine. The application
// ensures that there is at most one reader on a connection by executing all
// reads from this goroutine.
func (c *Client) ReadPump() {
	defer func() {
		c.Hub.Unregister <- c
		c.Conn.Close()
	}()
	c.Conn.SetReadLimit(maxMessageSize)
	c.Conn.SetReadDeadline(time.Now().Add(pongWait))
	c.Conn.SetPongHandler(func(string) error { c.Conn.SetReadDeadline(time.Now().Add(pongWait)); return nil })
	for {
		_, message, err := c.Conn.ReadMessage()
		if err != nil {
			if websocket.IsUnexpectedCloseError(err, websocket.CloseGoingAway, websocket.CloseAbnormalClosure) {
				log.Printf("error: %v", err)
			}
			break
		}
		//fmt.Println(message)
		obj := &Protobuf.Communication{}
		proto.Unmarshal(message, obj)

		//fmt.Println("ggggg",obj)
		msg := c.Username + ":" + obj.Msg
		if obj.Type == "1" {

			if obj.Msg == "userlist" { //浏览器输入userlist
				msg = db.GetAll()
			} else {
				log.Println(msg)
			}
			param := &Protobuf.Communication{
				Type: obj.Type,
				Msg:  msg,
			}
			//fmt.Println("msg",msg)
			data, _ := proto.Marshal(param)
			//fmt.Println("type = 1, message:", data)
			c.Hub.Broadcast <- data
		} else if obj.Type == "2" {
			param := &Protobuf.Communication{
				Type: obj.Type,
				Msg:  c.Username + "out",
			}
			data, _ := proto.Marshal(param)
			c.Hub.Broadcast <- data
			//fmt.Println("=+====="+string(data))
			break
		} else {
			msg = db.GetAll()
			param := &Protobuf.Communication{
				Type: obj.Type,
				Msg:  msg,
			}
			data, _ := proto.Marshal(param)
			c.Hub.Broadcast <- data
		}

	}
}

// writePump pumps messages from the hub to the websocket connection.
//
// A goroutine running writePump is started for each connection. The
// application ensures that there is at most one writer to a connection by
// executing all writes from this goroutine.
func (c *Client) WritePump() {
	ticker := time.NewTicker(pingPeriod)
	defer func() {
		ticker.Stop()
		c.Conn.Close()
	}()
	for {
		select {
		case message, ok := <-c.Send:
			c.Conn.SetWriteDeadline(time.Now().Add(writeWait))
			if !ok {
				// The hub closed the channel.
				c.Conn.WriteMessage(websocket.CloseMessage, []byte{})
				return
			}
			err := c.Conn.WriteMessage(websocket.BinaryMessage, message)
			if err != nil {
				log.Println(err)
				return
			}
		case <-ticker.C:
			c.Conn.SetWriteDeadline(time.Now().Add(writeWait))
			if err := c.Conn.WriteMessage(websocket.PingMessage, nil); err != nil {
				return
			}
		}
	}
}
