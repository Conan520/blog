package response

import "github.com/gin-gonic/gin"

func Success(ctx *gin.Context, code int, msg string, data any) {
	ctx.JSON(200, gin.H{
		"code": code,
		"msg":  msg,
		"data": data,
	})
}

func Fail(ctx *gin.Context, code int, msg string) {
	ctx.JSON(200, gin.H{
		"code": code,
		"msg":  msg,
	})
}
