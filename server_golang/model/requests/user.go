package requests

type UserInfo struct {
	Username string `json:"username"` // 字段标签需与 JSON 键名一致
	Password string `json:"password"`
}
