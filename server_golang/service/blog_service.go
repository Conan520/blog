package service

import (
	"gorm.io/gorm"
	"server_golang/model"
	"server_golang/model/requests"
)

type BlogService interface {
	SearchBlogs(page, pageSize int, keyword, categoryId string) ([]model.Blog, int, error)
	AddBlog(req requests.BlogReq) error
	UpdateBlog(req requests.UpdateBlogReq) error
	GetBlogDetail(id uint64) (model.Blog, error)
	DeleteBlog(id uint64) error
}

func NewBlogService() BlogService {
	return &blogService{}
}

type blogService struct {
	db *gorm.DB
}

func (b blogService) SearchBlogs(page, pageSize int, keyword, categoryId string) ([]model.Blog, int, error) {
	//TODO implement me
	panic("implement me")
}

func (b blogService) AddBlog(req requests.BlogReq) error {
	//TODO implement me
	panic("implement me")
}

func (b blogService) UpdateBlog(req requests.UpdateBlogReq) error {
	//TODO implement me
	panic("implement me")
}

func (b blogService) GetBlogDetail(id uint64) (model.Blog, error) {
	//TODO implement me
	panic("implement me")
}

func (b blogService) DeleteBlog(id uint64) error {
	//TODO implement me
	panic("implement me")
}

var _ BlogService = (*blogService)(nil)
