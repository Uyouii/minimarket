module uyouii.cool/tcpserver

go 1.18

replace settings => ../settings

replace mysqldb => ../mysqldb

require (
	mysqldb v0.0.0-00010101000000-000000000000
	settings v0.0.0-00010101000000-000000000000
)

require github.com/go-sql-driver/mysql v1.6.0 // indirect
