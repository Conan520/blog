package model

import "time"

type UserInfo struct {
	ID       uint64 `gorm:"column:id;primaryKey"`
	Username string `gorm:"column:username"`
	Password string `gorm:"column:password"`
}

func (UserInfo) TableName() string {
	return "user_info"
}

type Category struct {
	ID        uint64    `gorm:"primaryKey" json:"id""`
	Name      string    `gorm:"unique" json:"name"`
	CreatedAt time.Time `gorm:"autoCreateTime" json:"created_at"`
}

func (Category) TableName() string {
	return "category"
}

type Blog struct {
	ID         uint64 `json:"id"`
	CategoryId uint64 `gorm:"category_id" json:"category_id"`
	Title      string `json:"title"`
	Content    string `json:"content"`
	CreateTime uint64 `json:"create_time"`
}

func (Blog) TableName() string {
	return "blog"
}
