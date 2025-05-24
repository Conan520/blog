package middleware

import (
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"time"
)

func CORSMiddleware() gin.HandlerFunc {
	return cors.New(cors.Config{
		AllowOrigins:     []string{"http://127.0.0.1:5173", "http://localhost:5173"},
		AllowMethods:     []string{"DELETE", "GET", "POST", "PUT"}, // 明确允许 DELETE
		AllowHeaders:     []string{"Content-Type", "Authorization", "token"},
		AllowCredentials: true,
		MaxAge:           12 * time.Hour, // 预检结果缓存时间（秒）
	})
}
