package tcpserver

import (
	"database/sql"
	"encoding/json"
	"log"
	"mysqldb"
	"settings"
)

type Request interface {
	Process(data []byte, server *TcpServer) Response
}

type Response interface {
	Error() error
	GetResponse() []byte
}

type BaseRequest struct {
	Action    int    `json:"action"`
	RequestId string `json:"request_id"`
}

type BaseResponse struct {
	err       error
	ErrCode   int    `json:"errcode"`
	RequestId string `json:"request_id"`
}

type RegisterRequest struct {
	BaseRequest
	UserName string `json:"username"`
	Password string `json:"password"`
	Avatar   string `json:"avatar"`
}

type RegisterResponse struct {
	BaseResponse
	UserId   uint64 `json:"user_id"`
	UserName string `json:"username"`
}

type LoginRequest struct {
	BaseRequest
	UserName string `json:"username"`
	Password string `json:"password"`
}

type LoginReponse struct {
	BaseResponse
	UserId    uint64 `json:"user_id"`
	Session   string `json:"session"`
	LoginTime uint32 `json:"logintime"`
}

type GetUserInfoRequest struct {
	BaseRequest
	UserId   uint64 `json:"user_id"`
	UserName string `json:"username"`
}

type GetUserInfoReponse struct {
	BaseResponse
	UserId    uint64 `json:"user_id"`
	UserName  string `json:"username"`
	Avatar    string `json:"avatar"`
	Session   string `json:"session"`
	LoginTime uint32 `json:"logintime"`
}

func GetErrCode(err error) int {
	if err != nil {
		e, ok := err.(*settings.Error)
		if ok {
			return e.Errno
		} else {
			return settings.ERR_SYSTEM_ERROR
		}
	}
	return 0
}

func (r *GetUserInfoRequest) Process(data []byte, server *TcpServer) Response {
	resp := new(GetUserInfoReponse)

	err := json.Unmarshal(data, r)
	if err != nil {
		log.Printf("ERR: handle request failed, err: %v, req: %v", err, data)
		resp.err = err
		return resp
	}

	resp.RequestId = r.RequestId

	if r.UserId == 0 && r.UserName == "" {
		log.Printf("ERR: invalid request: %v", *r)
		resp.err = &settings.Error{Errno: settings.ERR_INVALID_REQUEST}
		return resp
	}

	var user mysqldb.User
	if r.UserId != 0 {
		user, err = server.db.GetUserById(r.UserId)
	} else {
		user, err = server.db.GetUserByName(r.UserName)
	}
	if err != nil {
		log.Printf("ERR: get user failed, req: %v, err: %v", *r, err)
		resp.err = err
		if err == sql.ErrNoRows {
			resp.err = &settings.Error{Errno: settings.ERR_USER_NOT_EXISTS}
		}
		return resp
	}

	resp.UserId = user.Id
	resp.UserName = user.Name
	resp.Avatar = user.Avatar
	resp.Session = user.Session
	resp.LoginTime = user.LoginTimestamp

	return resp
}

func (r *GetUserInfoReponse) GetResponse() (res []byte) {
	r.ErrCode = GetErrCode(r.err)

	var err error
	res, err = json.Marshal(r)
	if err != nil {
		log.Printf("ERR: json Marshal failed, req: %v, err: %v", *r, err)
		return nil
	}

	return res
}

func (r *GetUserInfoReponse) Error() error {
	return r.err
}

func (r *LoginRequest) Process(data []byte, server *TcpServer) Response {
	resp := new(LoginReponse)

	err := json.Unmarshal(data, r)
	if err != nil {
		log.Printf("ERR: handle request failed, err: %v, req: %v", err, data)
		resp.err = err
		return resp
	}

	resp.RequestId = r.RequestId

	if r.UserName == "" || r.Password == "" {
		log.Printf("ERR: invalid request: %v", *r)
		resp.err = &settings.Error{Errno: settings.ERR_INVALID_REQUEST}
		return resp
	}

	user, err := server.db.UserLogin(r.UserName, r.Password)
	if err != nil {
		log.Printf("ERR: user login failed, req: %v, err: %v", *r, err)
		resp.err = err
		return resp
	}

	resp.UserId = user.Id
	resp.Session = user.Session
	resp.LoginTime = user.LoginTimestamp

	return resp
}

func (r *LoginReponse) GetResponse() (res []byte) {
	r.ErrCode = GetErrCode(r.err)

	var err error
	res, err = json.Marshal(r)
	if err != nil {
		log.Printf("ERR: json Marshal failed, req: %v, err: %v", *r, err)
		return nil
	}

	return res
}

func (r *LoginReponse) Error() error {
	return r.err
}

func (r *RegisterRequest) Process(data []byte, server *TcpServer) Response {
	resp := new(RegisterResponse)

	err := json.Unmarshal(data, r)
	if err != nil {
		log.Printf("ERR: handle request failed, err: %v, req: %v", err, data)
		resp.err = err
		return resp
	}

	resp.RequestId = r.RequestId

	if r.UserName == "" || r.Password == "" {
		log.Printf("ERR: invalid request: %v", *r)
		resp.err = &settings.Error{Errno: settings.ERR_INVALID_REQUEST}
		return resp
	}
	user, err := server.db.RegisterUser(r.UserName, r.Password, r.Avatar)
	if err != nil {
		log.Printf("ERR: register user failed, req: %v, err: %v", *r, err)
		resp.err = err
		return resp
	}

	resp.UserId = user.Id
	resp.UserName = user.Name

	return resp
}

func (r *RegisterResponse) GetResponse() (res []byte) {
	r.ErrCode = GetErrCode(r.err)

	var err error
	res, err = json.Marshal(r)
	if err != nil {
		log.Printf("ERR: json Marshal failed, req: %v, err: %v", *r, err)
		return nil
	}

	return res
}

func (r *RegisterResponse) Error() error {
	return r.err
}
