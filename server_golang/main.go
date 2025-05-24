package main

import (
	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
	"os"
	"server_golang/middleware"
	"server_golang/router"
	"server_golang/utils"
)

func main() {
	//gin.SetMode(gin.ReleaseMode)
	InitConfig()
	utils.InitDB()
	r := gin.Default()
	r.Use(middleware.CORSMiddleware())
	router.RegisterRouter(r)
	r.Run(":8000")
}

func InitConfig() {
	workDir, _ := os.Getwd()
	viper.SetConfigName("config")
	viper.SetConfigType("yml")
	viper.AddConfigPath(workDir + "/config")
	err := viper.ReadInConfig()
	if err != nil {
		panic("")
	}
}
