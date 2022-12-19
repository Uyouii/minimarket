package mysqldb

import (
	"fmt"
	"log"
	"settings"
	"testing"
)

func TestRegisterUser(t *testing.T) {
	log.SetFlags(log.Lshortfile | log.LstdFlags)
	var mysqldb MysqlDb
	err := mysqldb.Start()
	if err != nil {
		t.Fatalf(`failed to start db, err: %v`, err)
	}
	user, err := mysqldb.RegisterUser("taiyoudong", "123456",
		"https://avatars.githubusercontent.com/u/25459212?v=4")
	if err != nil {
		if e, ok := err.(*settings.Error); !(ok && e.Errno == settings.ERR_USER_ALREADY_EXISTS) {
			t.Fatalf(`failed to start db, err: %v`, err)
		} else {
			log.Println("user already registered")
			return
		}
	}

	log.Println("register succeed, user:", user)
}

func TestBatchRegisterUser(t *testing.T) {
	log.SetFlags(log.Lshortfile | log.LstdFlags)
	var mysqldb MysqlDb
	err := mysqldb.Start()
	if err != nil {
		t.Fatalf(`failed to start db, err: %v`, err)
	}
	for i := 9293687; i < 10000000; i++ {
		username := fmt.Sprintf("testuser%v", i)
		user, err := mysqldb.RegisterUser(username, "123456", "https://avatars.githubusercontent.com/u/25459212?v=4")
		if err != nil {
			if e, ok := err.(*settings.Error); !(ok && e.Errno == settings.ERR_USER_ALREADY_EXISTS) {
				log.Printf("failed to start db, err: %v", err)
				i -= 1
			} else {
				log.Println("user already registered")
				continue
			}
		}
		log.Printf("register user: %v success", user.Name)
	}
	log.Println("success")
}

func TestUserLogin(t *testing.T) {
	log.SetFlags(log.Lshortfile | log.LstdFlags)
	var mysqldb MysqlDb
	err := mysqldb.Start()
	if err != nil {
		t.Fatalf(`failed to start db, err: %v`, err)
	}
	user, err := mysqldb.UserLogin("taiyoudong", "123456")
	if err != nil {
		t.Fatalf("ERR, register user failed: %v", err)
	}
	log.Println("user login succeed, user:", user)
}

func TestGetUserByName(t *testing.T) {
	var mysqldb MysqlDb
	err := mysqldb.Start()
	if err != nil {
		t.Fatalf(`failed to start db, err: %v`, err)
	}
	user, err := mysqldb.GetUserByName("taiyoudong")
	if err != nil {
		t.Fatalf("ERR, get user by name failed, err: %v", err)
	}
	log.Println("user:", user)
}

func TestGetUserById(t *testing.T) {
	var mysqldb MysqlDb
	err := mysqldb.Start()
	if err != nil {
		t.Fatalf(`failed to start db, err: %v`, err)
	}
	user, err := mysqldb.GetUserById(1498060041021696)
	if err != nil {
		t.Fatalf("ERR, get user by id failed, err: %v", err)
	}
	log.Println("user:", user)
}

func TestGetUserTableName(t *testing.T) {
	var mysqldb MysqlDb
	name := mysqldb.getUserTableByName("taiyoudong")
	log.Println("tablename:", name)
}

func TestGenUserId(t *testing.T) {
	user_name := "taiyoudong"
	var mysqldb MysqlDb
	user_id := mysqldb.genUserId(user_name)
	log.Println("user_id:", user_id)
	table_name := mysqldb.getUserTableNameById(user_id)
	user_table_name := mysqldb.getUserTableByName(user_name)
	if table_name != user_table_name {
		t.Fatalf("table id not equal from id and name, table_name_by_id: %v, table_name_by_name: %v",
			table_name, user_table_name)
	}
	log.Println("tablename:", table_name)
}

func TestUserPassword(t *testing.T) {
	pwd := "test"
	var mysqldb MysqlDb
	hashpwd := mysqldb.genUserHashPassword(pwd)
	log.Printf("hash password: %v", hashpwd)
	res := mysqldb.checkUserPassword(pwd, hashpwd)
	if res == false {
		t.Fatalf("password not match")
	}
	log.Println("pass")
}

func TestGenUserSession(t *testing.T) {
	var mysqldb MysqlDb
	session := mysqldb.genUserSession(22)
	log.Printf("session: %v", session)
}
