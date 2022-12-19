package mysqldb

import (
	"database/sql"
	"log"
	"math/rand"
	"settings"
	"time"

	"github.com/go-sql-driver/mysql"
)

type MysqlDb struct {
	cfg  mysql.Config
	db   *sql.DB
	rand *rand.Rand
}

func (mysqldb *MysqlDb) Start() error {
	mysqldb.cfg = mysql.Config{
		User:                 "root",
		Passwd:               "asdfgh",
		Net:                  "tcp",
		Addr:                 "127.0.0.1:3306",
		DBName:               "minimarket_user_db",
		AllowNativePasswords: true,
	}

	var err error
	mysqldb.db, err = sql.Open("mysql", mysqldb.cfg.FormatDSN())
	if err != nil {
		log.Println("Err connect to mysql, err: ", err)
		return err
	}
	// restrict max connect count to mysql
	mysqldb.db.SetMaxOpenConns(settings.MysqlConnCount)
	mysqldb.db.SetMaxIdleConns(settings.MysqlConnCount / 2)

	pingErr := mysqldb.db.Ping()
	if pingErr != nil {
		log.Println("Err connect to mysql, err: ", pingErr)
		return pingErr
	}

	// 初始化随机数生成器
	mysqldb.rand = rand.New(rand.NewSource(time.Now().UnixNano()))

	log.Println("Mysql Connected!")
	return nil
}
