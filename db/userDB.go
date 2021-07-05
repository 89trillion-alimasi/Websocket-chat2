package db

type User struct {
	UserName string
}

// 用于存储的内存容器
var users map[string][]*User

// 存储数据
func Add(username string) {
	if users == nil {
		users = make(map[string][]*User)
	}
	users[username] = append(users[username])
}

// 获取数据
func GetAll() string {
	userStr := ""
	if users == nil {
		return userStr
	}
	for key, _ := range users {
		userStr += key + ","
	}
	//fmt.Println(userStr)
	return userStr
}

// 删除数据
func Del(username string) {
	delete(users, username)
}
