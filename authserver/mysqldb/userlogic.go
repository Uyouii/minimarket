package mysqldb

import (
	"crypto/md5"
	cryptorand "crypto/rand"
	"database/sql"
	"encoding/hex"
	"fmt"
	"log"
	"settings"
	"strconv"
	"strings"
	"time"

	"hash/fnv"
)

type User struct {
	Id              uint64
	Name            string
	Password        string
	CreateTimestamp uint32
	Avatar          string
	Session         string
	LoginTimestamp  uint32
}

func (mysqldb *MysqlDb) GetUserByName(name string) (User, error) {
	tbname := mysqldb.getUserTableByName(name)
	querystr := fmt.Sprintf("select * from %v where name = ?", tbname)
	row := mysqldb.db.QueryRow(querystr, name)

	user, err := mysqldb.scanSingleRow(row)
	if err != nil {
		log.Printf("ERR: GetUserByName faild, tbname: %v, username: %v",
			tbname, name)
		return user, err
	}

	return user, nil
}

func (mysqldb *MysqlDb) GetUserById(id uint64) (User, error) {
	tbname := mysqldb.getUserTableNameById(id)
	querystr := fmt.Sprintf("select * from %v where id = ?", tbname)
	row := mysqldb.db.QueryRow(querystr, id)

	user, err := mysqldb.scanSingleRow(row)
	if err != nil {
		log.Printf("ERR: GetUserById faild, tbname: %v, id: %v",
			tbname, id)
		return user, err
	}

	return user, nil
}

func (mysqldb *MysqlDb) RegisterUser(name string, pwd string, avatar string) (User, error) {
	str_req := fmt.Sprintf("name: %v, password: %v, avatar: %v", name, pwd, avatar)
	var user User
	if name == "" || pwd == "" {
		log.Printf("invalid req: %v", str_req)
		return user, &settings.Error{Errno: settings.ERR_INVALID_REQUEST}
	}

	user, err := mysqldb.GetUserByName(name)
	if err != nil && err != sql.ErrNoRows {
		log.Printf("err to find user: %v", err)
		return user, err
	}

	if err == nil {
		log.Printf("INFO: user already exists: %v", user)
		return user, &settings.Error{Errno: settings.ERR_USER_ALREADY_EXISTS}
	}

	user.Name, user.Avatar = name, avatar
	user.CreateTimestamp = uint32(time.Now().Unix())
	user.Id = mysqldb.genUserId(name)
	user.Password = mysqldb.genUserHashPassword(pwd)
	user.Session, user.LoginTimestamp = "", 0

	if err = mysqldb.insertUser(user); err != nil {
		log.Printf("ERR, insertuser failed, user: %v, err: %v", user, err)
		return user, err
	}

	log.Printf("INFO: register success, user: %v", user)
	return user, nil
}

func (mysqldb *MysqlDb) UserLogin(name string, pwd string) (User, error) {
	str_req := fmt.Sprintf("name: %v, password: %v", name, pwd)
	var user User
	if name == "" || pwd == "" {
		log.Printf("invalid req: %v", str_req)
		return user, &settings.Error{Errno: settings.ERR_INVALID_REQUEST}
	}

	user, err := mysqldb.GetUserByName(name)
	if err != nil && err != sql.ErrNoRows {
		log.Printf("err to find user: %v", err)
		return user, err
	}

	if err == sql.ErrNoRows {
		log.Println("user has't register, req:", str_req)
		return user, &settings.Error{Errno: settings.ERR_USER_NOT_EXISTS}
	}

	valid := mysqldb.checkUserPassword(pwd, user.Password)
	if valid == false {
		log.Printf("ERR: invalid password, req: %v, user: %v", str_req, user)
		return user, &settings.Error{Errno: settings.ERR_INVALID_PASSWORD}
	}

	user.Session = mysqldb.genUserSession(int64(user.Id))
	user.LoginTimestamp = uint32(time.Now().Unix())

	if err = mysqldb.setUserSession(user); err != nil {
		log.Printf("ERR: err to set user session: %v", err)
		return user, err
	}

	// log.Printf("user login success, user: %v", user)

	return user, nil
}

func (mysqldb *MysqlDb) genUserSession(user_id int64) string {
	rand_byte := make([]byte, 8)
	cryptorand.Read(rand_byte)
	rand_str := hex.EncodeToString(rand_byte)
	timestamp := time.Now().UnixNano()
	hash32 := fnv.New32()
	hash32.Write([]byte(fmt.Sprintf("%v", user_id+timestamp)))
	session_str := fmt.Sprintf("%v%x", rand_str, hash32.Sum32())
	return session_str
}

// md5 hash + salt
// salt:hashpwd
// eg: 90a8731:39e862f93162e9835a257e529e06fae3
func (mysqldb *MysqlDb) genUserHashPassword(pwd string) string {
	random_num := mysqldb.rand.Uint32()
	random_str := strconv.FormatUint(uint64(random_num), 16)
	md5hash := md5.Sum([]byte(fmt.Sprintf("%v:%v", random_str, pwd)))
	md5str := fmt.Sprintf("%x", md5hash)
	return fmt.Sprintf("%v:%v", random_str, md5str)
}

func (mysqldb *MysqlDb) checkUserPassword(pwd string, hashpwd string) bool {
	vec_str := strings.Split(hashpwd, ":")
	if len(vec_str) != 2 {
		log.Printf("ERR: hashpwd invalid format: %v", hashpwd)
		return false
	}
	md5hash := md5.Sum([]byte(fmt.Sprintf("%v:%v", vec_str[0], pwd)))
	md5str := fmt.Sprintf("%x", md5hash)
	return md5str == vec_str[1]
}

/*
|-1bit-|---41bit mstime---|---15bit random num---|---7bit tableid---|
|---------------------------- 64 bit -------------------------------|
confim that can get same table id from username and user_id
*/
func (mysqldb *MysqlDb) genUserId(name string) uint64 {
	mstime := uint64(time.Now().UnixNano()/1e6) - settings.InitMsTimeStamp
	name_hash := mysqldb.getUserNameHash(name)
	random_num := mysqldb.rand.Uint64()
	id := (mstime << 22) + ((random_num & 0x7fff) << 7) + uint64(name_hash%10)
	return id
}

func (mysqldb *MysqlDb) getUserNameHash(name string) uint32 {
	hash32 := fnv.New32()
	hash32.Write([]byte(name))
	return hash32.Sum32()
}

// hash user name for sharing table
// use fnv hash func
func (mysqldb *MysqlDb) getUserTableByName(name string) string {
	table_id := mysqldb.getUserNameHash(name) % settings.UserShareTableCount
	return fmt.Sprintf("user_tab_%v", table_id)
}

func (mysqldb *MysqlDb) getUserTableNameById(id uint64) string {
	num := id & 0x3f
	return fmt.Sprintf("user_tab_%v", num)
}

func (mysqldb *MysqlDb) scanSingleRow(row *sql.Row) (User, error) {
	var user User
	if err := row.Scan(&user.Id, &user.Name, &user.Password, &user.CreateTimestamp,
		&user.Avatar, &user.Session, &user.LoginTimestamp); err != nil {

		if err == sql.ErrNoRows {
			log.Println("ERR: no users")
			return user, err
		}
		log.Println("ERR: faild to find user")
		return user, err
	}
	return user, nil
}

func (mysqldb *MysqlDb) insertUser(user User) error {
	tbname := mysqldb.getUserTableNameById(user.Id)

	exe_str := fmt.Sprintf("insert into %v (id, name, password, create_timestamp, avatar, session, login_timestamp) values(?, ?, ?, ?, ?, ?, ?)", tbname)

	res, err := mysqldb.db.Exec(exe_str, user.Id, user.Name,
		user.Password, user.CreateTimestamp, user.Avatar, user.Session, user.LoginTimestamp)

	if err != nil {
		log.Printf("ERR: insert user failed, user: %v, error: %v", user, err)
		return err
	}

	_, err = res.LastInsertId()
	if err != nil {
		log.Printf("ERR: insert user failed, user: %v, error: %v", user, err)
		return err
	}
	return nil
}

func (mysqldb *MysqlDb) setUserSession(user User) error {
	tbname := mysqldb.getUserTableNameById(user.Id)
	exe_str := fmt.Sprintf("update %v set session=?,login_timestamp=? where id=?", tbname)

	res, err := mysqldb.db.Exec(exe_str, user.Session, user.LoginTimestamp, user.Id)

	if err != nil {
		log.Printf("ERR: set user session failed, user: %v, error: %v", user, err)
		return err
	}

	_, err = res.LastInsertId()
	if err != nil {
		log.Printf("ERR: set user session failed, user: %v, error: %v", user, err)
		return err
	}
	return nil
}
