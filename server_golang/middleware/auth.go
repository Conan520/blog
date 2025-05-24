package middleware

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
	"server_golang/model"
	"server_golang/utils"
)

func AuthMiddleware() gin.HandlerFunc {
	return func(ctx *gin.Context) {
		// 获取 authorization header
		tokenString := ctx.GetHeader("Authorization")
		if tokenString == "" {
			tokenString = ctx.GetHeader("token")
		}

		fmt.Print("请求token\n", tokenString)

		//validate token format
		if tokenString == "" {
			ctx.JSON(http.StatusUnauthorized, gin.H{
				"code": 401,
				"msg":  "权限不足",
			})
			ctx.Abort()
			return
		}

		jwt := utils.NewJWT()
		claims, err := jwt.ParseToken(tokenString)
		if err != nil {
			ctx.JSON(http.StatusUnauthorized, gin.H{
				"code": 401,
				"msg":  "权限不足",
				"err":  err.Error(),
			})
			ctx.Abort()
			return
		}

		//token通过验证, 获取claims中的UserID
		userId := claims.BaseClaims.ID
		DB := utils.GetDB()
		var user model.UserInfo
		DB.First(&user, userId)

		// 验证用户是否存在
		if user.ID == 0 {
			ctx.JSON(http.StatusUnauthorized, gin.H{
				"code": 401,
				"msg":  "权限不足",
			})
			ctx.Abort()
			return
		}

		//用户存在 将user信息写入上下文，需要的话可以用于权限分级
		ctx.Set("user", user)

		ctx.Next()
	}
}
