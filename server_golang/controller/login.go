package controller

import (
	"errors"
	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
	"server_golang/model"
	"server_golang/model/requests"
	"server_golang/utils"
)

func Login(c *gin.Context) {
	var userReq requests.UserInfo
	// 使用 ShouldBindJSON 解析请求体中的 JSON 数据
	if err := c.ShouldBindJSON(&userReq); err != nil {
		c.JSON(200, gin.H{
			"code": 400,
			"msg":  "Invalid requests data",
			"data": ""})
		return
	}
	// 使用解析后的数据
	var userInfo model.UserInfo
	db := utils.GetDB()
	result := db.Where("username = ? AND password = ?",
		userReq.Username, userReq.Password).First(&userInfo)
	if result.Error != nil {
		if errors.Is(result.Error, gorm.ErrRecordNotFound) {
			c.JSON(404, gin.H{"error": "用户名或密码错误"})
		} else {
			c.JSON(500, gin.H{"error": "数据库查询失败"})
		}
		return
	}
	jwt := utils.NewJWT()
	baseClaims := requests.BaseClaims{
		ID:       uint(userInfo.ID),
		Username: userInfo.Username,
	}
	customClaims := jwt.CreateClaims(baseClaims)
	token, err := jwt.CreateToken(customClaims)
	if err != nil {
		c.JSON(500, gin.H{
			"code": 500,
			"msg":  "token create failed",
		})
		return
	}
	c.JSON(200, gin.H{
		"code": 200,
		"msg":  "ok",
		"data": gin.H{
			"id":       userInfo.ID,
			"access":   token,
			"username": userInfo.Username,
		},
	})
}
