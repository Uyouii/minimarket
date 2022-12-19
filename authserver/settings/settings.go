package settings

const (
	ServerAddress              = "127.0.0.1"
	ServerPort                 = 9999
	ServerTimeOut              = 30 // 单位 s
	DataBufferSize             = 1024 * 16
	UserShareTableCount        = 10 // 用户分表数量
	InitMsTimeStamp     uint64 = 1649560925481
	MysqlConnCount             = 128 // mysql数据库连接数量
	ResponseChannelSize        = 64
	SessionValidTime           = 3600 * 24
)

const (
	ACTION_REGISTER int = 1 + iota
	ACTION_LOGIN
	ACTION_GET_USER_INFO
)

const (
	CHANNEL_STATUS_OK int = iota
	CHANNEL_STATUS_DELETE
)
