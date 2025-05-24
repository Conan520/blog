package router

import (
	"github.com/gin-gonic/gin"
	"server_golang/controller"
	"server_golang/middleware"
)

func RegisterRouter(r *gin.Engine) {
	r.POST("/blog/admin/login", controller.Login)

	r.GET("/category/list", controller.GetCategoryList)
	r.POST("/category/add", middleware.AuthMiddleware(), controller.AddCategory)
	r.DELETE("/category/:id", middleware.AuthMiddleware(), controller.DeleteCategory)

	r.DELETE("/blog/:id", middleware.AuthMiddleware(), controller.DeleteBlog)
	r.POST("/blog/add", middleware.AuthMiddleware(), controller.AddBlog)
	r.PUT("/blog/update", middleware.AuthMiddleware(), controller.UpdateBlog)
	r.GET("/blog/search", controller.SearchBlogs)
	r.GET("/blog/detail/:id", middleware.AuthMiddleware(), controller.GetBlogDetail)
}
