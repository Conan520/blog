package controller

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
	"server_golang/model"
	"server_golang/model/requests"
	"server_golang/model/response"
	"server_golang/utils"
	"strconv"
	"strings"
	"time"
)

func SearchBlogs(c *gin.Context) {
	page, _ := strconv.Atoi(c.Query("page"))
	pageSize, _ := strconv.Atoi(c.Query("pageSize"))
	keyword := c.Query("keyword")
	categoryId := c.Query("categoryId")
	params := make([]interface{}, 0)
	whereSqlStrs := make([]string, 0)
	if categoryId != "" {
		whereSqlStrs = append(whereSqlStrs, "`category_id` = ?")
		params = append(params, categoryId)
	}

	if keyword != "" {
		whereSqlStrs = append(whereSqlStrs, " (`title` LIKE ? OR `content` LIKE ?) ")
		params = append(params, "%"+keyword+"%", "%"+keyword+"%")
	}
	whereSqlStr := ""
	if len(whereSqlStrs) > 0 {
		whereSqlStr = " WHERE " + strings.Join(whereSqlStrs, " AND ")
	}
	sqlStat := "SELECT `id`,`category_id`,`create_time`,`title`,substr(`content`, 1, 50) AS `content` FROM `blog`" +
		whereSqlStr + " order by `create_time` DESC"
	db := utils.GetDB()
	var blogs []model.Blog
	err := db.Raw(sqlStat, params...).Scan(&blogs).Error
	if err != nil {
		response.Fail(c, 500, "")
		return
	}
	fmt.Println(page, pageSize)
	pageEnd := len(blogs)
	if page*pageSize < pageEnd {
		pageEnd = page * pageSize
	}
	paginatedBlogs := blogs[(page-1)*pageSize : pageEnd]
	response.Success(c, 200, "ok", gin.H{
		"results":   paginatedBlogs,
		"count":     len(blogs),
		"page":      page,
		"page_size": pageSize,
	})
}

func AddBlog(c *gin.Context) {
	var blogReq requests.BlogReq
	if err := c.ShouldBindJSON(&blogReq); err != nil {
		response.Fail(c, 400, "参数不合法")
		return
	}
	id, _ := utils.GenerateID()
	modelBlog := model.Blog{
		ID:         uint64(id),
		CategoryId: blogReq.CategoryId,
		Title:      blogReq.Title,
		Content:    blogReq.Content,
		CreateTime: uint64(time.Now().Unix()),
	}
	db := utils.GetDB()
	err := db.Transaction(func(tx *gorm.DB) error {
		// 在事务中执行一些 db 操作（从这里开始，您应该使用 'tx' 而不是 'db'）
		if err := tx.Create(&modelBlog).Error; err != nil {
			// 返回任何错误都会回滚事务
			return err
		}
		// 返回 nil 提交事务
		return nil
	})
	if err != nil {
		response.Fail(c, 1004, "数据库操作失败")
		return
	}
	response.Success(c, 200, "添加成功", nil)
}

func UpdateBlog(c *gin.Context) {
	var blogReq requests.UpdateBlogReq
	if err := c.ShouldBindJSON(&blogReq); err != nil {
		response.Fail(c, 400, "参数不合法")
		return
	}
	modelBlog := model.Blog{
		ID:         blogReq.ID,
		CategoryId: blogReq.CategoryId,
		Title:      blogReq.Title,
		Content:    blogReq.Content,
		CreateTime: uint64(time.Now().Unix()),
	}
	db := utils.GetDB()
	err := db.Save(&modelBlog).Error
	if err != nil {
		response.Fail(c, 1004, "database operation failed")
		return
	}
	response.Success(c, 200, "success", modelBlog)
}

func GetBlogDetail(c *gin.Context) {
	id := c.Param("id")
	db := utils.GetDB()
	var blog model.Blog
	err := db.First(&blog, id).Error
	if err != nil {
		response.Fail(c, 1006, "")
		return
	}
	response.Success(c, 200, "ok", blog)
}

func DeleteBlog(c *gin.Context) {
	id := c.Param("id")
	db := utils.GetDB()
	tx := db.Delete(&model.Blog{}, id)
	if tx.Error != nil {
		response.Fail(c, 500, "删除失败")
		return
	}
	response.Success(c, 200, "删除成功", nil)
}
