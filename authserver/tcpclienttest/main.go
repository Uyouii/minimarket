package main

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"log"
	"net"
	"os"
	"settings"
	"time"
)

func IntToBytes(n int32) []byte {
	bytesBuffer := bytes.NewBuffer([]byte{})
	binary.Write(bytesBuffer, binary.BigEndian, n)
	return bytesBuffer.Bytes()
}

func main() {
	connTimeout := settings.ServerTimeOut * time.Second
	conn, err := net.DialTimeout("tcp",
		fmt.Sprintf("%v:%v", settings.ServerAddress, settings.ServerPort), connTimeout) // 3s timeout
	if err != nil {
		log.Println("dial failed:", err)
		os.Exit(1)
	}
	defer conn.Close()

	for i := 1; i < 5; i++ {

		// data := []byte(`{"action":1,"username":"testuser1","password":"123456", "avatar":"https://avatars.githubusercontent.com/u/25459212?v=4"}`)

		data := []byte(`{"action":3, "request_id": "11","user_id":348232622276960}`)
		datalen := len(data)
		buffer := IntToBytes(int32(datalen))
		buffer = append(buffer, data...)
		n, err := conn.Write(buffer)
		if err != nil {
			log.Println("Write error:", err)
			return
		}
		log.Println("send:", n)
		recvbuffer := make([]byte, 256)
		n, err = conn.Read(recvbuffer)
		if err != nil {
			log.Println("Read failed:", err)
			break
		}
		log.Printf("INFO: recv msg, len: %v, %v", n, string(recvbuffer))
		time.Sleep(10 * time.Second)
	}
	time.Sleep(10 * time.Second)

	log.Println("done")
}
