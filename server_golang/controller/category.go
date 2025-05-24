package controller

import (
	"errors"
	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
	"server_golang/model"
	"server_golang/model/requests"
	"server_golang/model/response"
	"server_golang/utils"
)

func GetCategoryList(c *gin.Context) {
	db := utils.GetDB()
	var categories []model.Category
	tx := db.Find(&categories)
	if tx.Error != nil {
		if errors.Is(tx.Error, gorm.ErrRecordNotFound) {
			response.Success(c, 200, "", []string{})
		} else {
			response.Fail(c, 500, "Internal Server Error")
		}
		return
	}
	response.Success(c, 200, "ok", categories)
}

func AddCategory(c *gin.Context) {
	db := utils.GetDB()
	var category requests.Category
	if err := c.ShouldBindJSON(&category); err != nil {
		response.Fail(c, 400, "request body invalid")
		return
	}
	id, _ := utils.GenerateFlakeId()
	dbCategory := model.Category{
		ID:   uint64(id),
		Name: category.Name,
	}
	tx := db.Create(&dbCategory)
	if tx.Error != nil {
		if errors.Is(tx.Error, gorm.ErrInvalidData) {
			response.Fail(c, 400, "添加失败")
		} else {
			response.Fail(c, 500, "Internal Server Error")
		}
		return
	}
	response.Success(c, 200, "添加成功", dbCategory)
}

func DeleteCategory(c *gin.Context) {
	id := c.Param("id")
	db := utils.GetDB()
	tx := db.Delete(&model.Category{}, id)
	if tx.Error != nil {
		response.Fail(c, 500, "删除失败")
		return
	}
	response.Success(c, 200, "删除成功", nil)
}
