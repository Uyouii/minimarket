package tcpserver

import (
	"encoding/json"
	"fmt"
	"log"
	"mysqldb"
	"net"
	"settings"
)

const (
	DEBUG int = iota
	RELEASE
)

type RespChan struct {
	channel chan []byte
	status  int
}

type TcpServer struct {
	Mode     int
	Port     int
	listener net.Listener
	db       *mysqldb.MysqlDb
}

func (server *TcpServer) Start() error {

	// start db first
	server.db = &mysqldb.MysqlDb{}
	err := server.db.Start()
	if err != nil {
		log.Println("Fail Start database, err:", err)
		return err
	}

	server.Port = settings.ServerPort

	address := fmt.Sprintf("%v:%v", settings.ServerAddress, server.Port)
	server.listener, err = net.Listen("tcp", address)
	if err != nil {
		log.Fatal(err)
	}
	log.Println("Tcp Server Started.")

	server.Run()

	return nil
}

func (server *TcpServer) Run() {
	for {
		conn, err := server.listener.Accept()
		if err != nil {
			log.Println(err)
			continue
		}
		go server.handleConn(conn)
	}
}

/*
response format:
|-- 4bit len --|-- data --|
to handle multi response come together
*/
func (server *TcpServer) handleResp(conn net.Conn, resp_channel chan []byte) {
	for {
		resp_data, ok := <-resp_channel
		if !ok {
			// log.Printf("conn %v closed", conn.RemoteAddr())
			break
		}
		sendbuffer := IntToBytes(int32(len(resp_data)))
		sendbuffer = append(sendbuffer, resp_data...)
		n, err := conn.Write(sendbuffer)
		if err != nil {
			log.Printf("ERR: failed to send data to client, err: %v", err)
			continue
		}
		if server.Mode == DEBUG {
			log.Printf("INFO: send len: %v, msg: %v", n, string(resp_data))
		}
	}
}

/*
request format:
|-- 4byte len --|-- data --|
to handle multi request come together
*/
func (server *TcpServer) handleConn(conn net.Conn) {
	log.Printf("new conn from %v", conn.RemoteAddr())
	defer conn.Close()
	var buffer []byte
	recvdata := make([]byte, settings.DataBufferSize)

	resp_channel := RespChan{
		make(chan []byte, settings.ResponseChannelSize), 0}

	go server.handleResp(conn, resp_channel.channel)
	for {
		n, err := conn.Read(recvdata)
		if err != nil {
			log.Println("Read failed:", err)
			break
		}
		if server.Mode == DEBUG {
			log.Printf("INFO: recv msg, len: %v, %v", n, string(buffer))
		}
		buffer = append(buffer, recvdata[:n]...)

		for len(buffer) > 4 {
			datalen := BytesToInt(buffer[:4])
			if len(buffer) < int(datalen+4) {
				break
			}
			req_data := buffer[4 : 4+datalen]
			buffer = buffer[4+datalen:]
			go server.HandleRequest(conn, req_data, &resp_channel)
		}
	}
	resp_channel.status = settings.CHANNEL_STATUS_DELETE
	close(resp_channel.channel)
	log.Printf("conn %v closed", conn.RemoteAddr())
}

func (server *TcpServer) HandleRequest(conn net.Conn, data []byte, resp_channel *RespChan) error {
	var base_req BaseRequest

	err := json.Unmarshal(data, &base_req)
	if err != nil {
		log.Printf("handle request failed, err: %v, req: %v", err, string(data))
		return err
	}

	var request Request

	switch base_req.Action {
	case settings.ACTION_REGISTER:
		request = new(RegisterRequest)
	case settings.ACTION_LOGIN:
		request = new(LoginRequest)
	case settings.ACTION_GET_USER_INFO:
		request = new(GetUserInfoRequest)
	default:
		log.Printf("ERR: Unknown request, req: %v", data)
		return &settings.Error{Errno: settings.ERR_UNKNOWN_ACTION}
	}

	response := request.Process(data, server)
	if err = response.Error(); err != nil {
		log.Printf("ERR: Process failed, req: %v, err: %v", string(data), err)
	}

	resp_data := response.GetResponse()
	if server.Mode == DEBUG {
		log.Printf("INFO: Handle Request, req: %v, resp: %v",
			string(data), string(resp_data))
	}
	if resp_channel.status == settings.CHANNEL_STATUS_OK {
		resp_channel.channel <- resp_data
	}

	return nil
}
