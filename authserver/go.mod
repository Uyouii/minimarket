module uyouii.cool/authserver

go 1.18

replace settings => ./settings

replace tcpserver => ./tcpserver

replace mysqldb => ./mysqldb

require tcpserver v0.0.0-00010101000000-000000000000

require (
	github.com/go-sql-driver/mysql v1.6.0 // indirect
	mysqldb v0.0.0-00010101000000-000000000000 // indirect
	settings v0.0.0-00010101000000-000000000000 // indirect
)
