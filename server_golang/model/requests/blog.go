package requests

type BlogReq struct {
	CategoryId uint64 `json:"categoryId"`
	Title      string `json:"title"`
	Content    string `json:"content"`
}

type UpdateBlogReq struct {
	ID         uint64 `json:"id"`
	CategoryId uint64 `json:"categoryId"`
	Title      string `json:"title"`
	Content    string `json:"content"`
}
