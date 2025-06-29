package response

import "github.com/gin-gonic/gin"

type BaseResponse struct {
	Code int         `json:"code"`
	Msg  string      `json:"msg"`
	Data interface{} `json:"data"`
}

func Success(ctx *gin.Context, code int, msg string, data any) {
	ctx.JSON(200, BaseResponse{
		Code: code,
		Msg:  msg,
		Data: data,
	})
}

func Fail(ctx *gin.Context, code int, msg string) {
	ctx.JSON(200, BaseResponse{
		Code: code,
		Msg:  msg,
	})
}
