package main

import (
	"flag"
	"log"
	"tcpserver"
)

func main() {
	log.SetFlags(log.Lshortfile | log.LstdFlags)

	var modeStr string
	flag.StringVar(&modeStr, "m", "release", "defaut is release")
	flag.Parse()

	mode := tcpserver.RELEASE
	if modeStr == "debug" {
		log.Println("debug mode")
		mode = tcpserver.DEBUG
	} else {
		log.Println("release mode")
	}

	server := &tcpserver.TcpServer{Mode: mode}
	if err := server.Start(); err != nil {
		log.Fatalf("ERR: server start failed: %v", err)
	}
}
