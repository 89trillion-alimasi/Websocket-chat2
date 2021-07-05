// Copyright 2013 The Gorilla WebSocket Authors. All rights reserved.
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file.

package main

import (
	"Websocket-chat/router"
	"flag"
	"log"
	"net/http"
	"os"
)

//http 地址
var addr = flag.String("addr", ":8080", "http service address")

func main() {
	os.Mkdir("log", 0777)
	logtext, err := os.OpenFile("log/result.log", os.O_CREATE|os.O_APPEND|os.O_RDWR, 0644)
	if err != nil {
		log.Fatalf("file open error : %v", err)
	}
	log.SetOutput(logtext)
	defer logtext.Close()

	flag.Parse()

	router.Httpconnect()
	err = http.ListenAndServe(*addr, nil)

	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}
