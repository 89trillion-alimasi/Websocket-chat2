package server

import (
	"Websocket-chat/config"
	"Websocket-chat/db"
	_ "Websocket-chat/db"
	"fmt"
	"log"
	"net/http"
	"net/url"
	"time"
)

// serveWs handles websocket requests from the peer.
func ServeWs(hub *config.Hub, w http.ResponseWriter, r *http.Request) {

	// 启动服务时将username存下来
	values, _ := url.ParseQuery(r.URL.RawQuery)
	db.Add(values["username"][0])

	// 升级这个请求为 `websocket` 协议
	conn, err := config.Upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println(err)
		return
	}
	fmt.Println("client connected:", conn.RemoteAddr())

	//初始化当前的客户端的实例，并与"hub"中心管理勾搭
	client := &config.Client{Hub: hub, Conn: conn, Send: make(chan []byte, 256), Username: values["username"][0]}

	client.Hub.Register <- client

	// 通过在新的goroutines中完成所有工作，允许调用者引用内存的集合。
	// 其实对当前 `websocket` 连接的 `I/O` 操作
	// 写操作（发消息到客户端）-> 这里 `Hub` 会统一处理
	go client.WritePump()
	// 读操作（对消息到客户端）-> 读完当前连接立即发 -> 交由 `Hub` 分发消息到所有连接
	go client.ReadPump()

	time.Sleep(3 * time.Millisecond)

}
