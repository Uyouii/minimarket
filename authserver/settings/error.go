package settings

import "fmt"

const (
	ERR_SYSTEM_ERROR int = 1000 + iota
	ERR_UNKNOWN_ACTION
	ERR_INVALID_REQUEST
	ERR_USER_ALREADY_EXISTS
	ERR_INVALID_FORMAT
	ERR_USER_NOT_EXISTS
	ERR_INVALID_PASSWORD
)

type Error struct {
	Errno  int `json:"errno"`
	errMsg string
}

func (e *Error) Error() string {
	switch e.Errno {
	case ERR_SYSTEM_ERROR:
		e.errMsg = fmt.Sprintf("errno: %v, system error", e.Errno)
	case ERR_UNKNOWN_ACTION:
		e.errMsg = fmt.Sprintf("errno: %v, unknown action", e.Errno)
	case ERR_INVALID_REQUEST:
		e.errMsg = fmt.Sprintf("errno: %v, invalid request", e.Errno)
	case ERR_USER_ALREADY_EXISTS:
		e.errMsg = fmt.Sprintf("errno: %v, user already exists", e.Errno)
	case ERR_INVALID_FORMAT:
		e.errMsg = fmt.Sprintf("errno: %v, invalid format", e.Errno)
	case ERR_USER_NOT_EXISTS:
		e.errMsg = fmt.Sprintf("errno: %v, user not exists", e.Errno)
	case ERR_INVALID_PASSWORD:
		e.errMsg = fmt.Sprintf("errno: %v, invalid password", e.Errno)
	default:
		e.errMsg = fmt.Sprintf("errno: %v, unknown error", e.Errno)
	}
	return e.errMsg
}
