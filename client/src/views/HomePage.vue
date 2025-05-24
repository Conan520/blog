<template>
    <div class="page-container">
        <header class="header">
            <div class="logo">
                <n-icon size="28" color="var(--accent)">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M19 5v14H5V5h14m0-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2z"/><path fill="currentColor" d="M14 17H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>
                </n-icon>
                <h1 class="site-title">博客天地</h1>
            </div>
            <div class="nav">
                <div class="nav-item" :class="{ active: pageInfo.categoryId === 0 }" @click="homePage">
                    <n-icon>
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M10 20v-6h4v6h5v-8h3L12 3L2 12h3v8h5Z"/></svg>
                    </n-icon>
                    首页
                </div>
                <div class="nav-item">
                    <n-popselect @update:value="searchByCategory" v-model:value="selectedCategory" :options="categortyOptions" trigger="click">
                        <div class="category-selector">
                            <n-icon>
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2l-5.5 9h11L12 2zm0 3.84L13.93 9h-3.87L12 5.84zM17.5 13c-2.49 0-4.5 2.01-4.5 4.5s2.01 4.5 4.5 4.5s4.5-2.01 4.5-4.5s-2.01-4.5-4.5-4.5zm0 7c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5s2.5 1.12 2.5 2.5s-1.12 2.5-2.5 2.5zM3 21.5h8v-8H3v8zm2-6h4v4H5v-4z"/></svg>
                            </n-icon>
                            分类 <span class="category-badge" v-if="categoryName">{{ categoryName }}</span>
                        </div>
                    </n-popselect>
                </div>
                <div class="nav-item" @click="dashboard">
                    <n-icon>
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14z"/><path fill="currentColor" d="M7 12h2v5H7zm4-7h2v12h-2zm4 4h2v8h-2z"/></svg>
                    </n-icon>
                    后台
                </div>
            </div>
        </header>

        <div class="search-container">
            <n-input 
                v-model:value="pageInfo.keyword" 
                class="search-input" 
                placeholder="输入关键字搜索文章..."
                round>
                <template #prefix>
                    <n-icon>
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="m19.6 21l-6.3-6.3q-.75.6-1.725.95T9.5 16q-2.725 0-4.612-1.888T3 9.5q0-2.725 1.888-4.612T9.5 3q2.725 0 4.612 1.888T16 9.5q0 1.1-.35 2.075T14.7 13.3l6.3 6.3l-1.4 1.4ZM9.5 14q1.875 0 3.188-1.313T14 9.5q0-1.875-1.313-3.188T9.5 5Q7.625 5 6.312 6.313T5 9.5q0 1.875 1.313 3.188T9.5 14Z"/></svg>
                    </n-icon>
                </template>
                <template #suffix>
                    <n-button type="primary" class="search-button" round @click="loadBlogs(0)">
                        <n-icon size="16" class="search-icon">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="m19.6 21l-6.3-6.3q-.75.6-1.725.95T9.5 16q-2.725 0-4.612-1.888T3 9.5q0-2.725 1.888-4.612T9.5 3q2.725 0 4.612 1.888T16 9.5q0 1.1-.35 2.075T14.7 13.3l6.3 6.3l-1.4 1.4ZM9.5 14q1.875 0 3.188-1.313T14 9.5q0-1.875-1.313-3.188T9.5 5Q7.625 5 6.312 6.313T5 9.5q0 1.875 1.313 3.188T9.5 14Z"/></svg>
                        </n-icon>
                        搜索
                    </n-button>
                </template>
            </n-input>
        </div>

        <div class="blog-list fade-in">
            <div v-for="(blog, index) in blogListInfo" :key="blog.id" class="blog-card-wrapper">
                <n-card class="blog-card" hoverable @click="toDetail(blog)">
                    <template #header>
                        <div class="blog-header">
                            <h3 class="blog-title">{{ blog.title }}</h3>
                        </div>
                    </template>
                    
                    <div class="blog-excerpt">{{ blog.content }}</div>

                    <template #footer>
                        <div class="blog-footer">
                            <div class="blog-meta">
                                <n-icon size="16" color="var(--vt-c-text-light-2)">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10s10-4.5 10-10S17.5 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8s8 3.59 8 8s-3.59 8-8 8zm.5-13H11v6l5.2 3.2l.8-1.3l-4.5-2.7V7z"/></svg>
                                </n-icon>
                                <span>{{ blog.create_time }}</span>
                            </div>
                            <n-button text size="small">
                                阅读全文
                                <template>
                                    <n-icon>
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M16.01 11H4v2h12.01v3L20 12l-3.99-4v3z"/></svg>
                                    </n-icon>
                                </template>
                            </n-button>
                        </div>
                    </template>
                </n-card>
            </div>
        </div>

        <div class="pagination-container">
            <n-pagination 
                @update:page="loadBlogs" 
                v-model:page="pageInfo.page" 
                :page-count="pageInfo.pageCount"
                :page-slot="5"
                size="large" />
        </div>

        <footer class="footer">
            <div class="footer-content">
                <div>Power by Zhayubo</div>
                <div>XICP备XXXXX号-1</div>
            </div>
        </footer>
    </div>
</template>

<script setup>
import { ref, reactive, inject, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

// 路由
const router = useRouter()
const route = useRoute()

const message = inject("message")
const dialog = inject("dialog")
const axios = inject("axios")

// 选中的分类
const selectedCategory = ref(0)
// 分类选项
const categortyOptions = ref([])
// 文章列表
const blogListInfo = ref([])

// 查询和分页数据
const pageInfo = reactive({
    page: 1,
    pageSize: 3,
    pageCount: 0,
    count: 0,
    keyword: "",
    categoryId: 0,
})

onMounted(() => {
    loadCategorys();
    loadBlogs()
})

/**
 * 获取博客列表
 */
const loadBlogs = async (page = 0) => {
    if (page !== 0) {
        pageInfo.page = page;
    }
  let res = await axios.get(`/blog/search?keyword=${pageInfo.keyword}&page=${pageInfo.page}&pageSize=${pageInfo.pageSize}&categoryId=${pageInfo.categoryId}`)
  console.log("res = ", res)
  let temp_rows = res.data.data.results;
  for (let row of temp_rows) {
    row.content += "..."
    let d = new Date(row.create_time*1000)
    row.create_time = `${d.getFullYear()}/${d.getMonth() + 1}/${d.getDate()} ${d.getHours()}:${d.getMinutes()}`
  }
  blogListInfo.value = temp_rows;
  pageInfo.count = res.data.data.count;
  pageInfo.pageCount = parseInt(pageInfo.count / pageInfo.pageSize) + (pageInfo.count % pageInfo.pageSize > 0 ? 1 : 0)
}

const categoryName = computed(() => {
    //获取选中的分类
    let selectedOption = categortyOptions.value.find((option) => { return option.value === selectedCategory.value })
    //返回分类的名称
    return selectedOption ? selectedOption.label : ""
})

/**
 * 获取分类列表
 */
const loadCategorys = async () => {
    let res = await axios.get("/category/list")
    categortyOptions.value = res.data.data.map((item) => {
        return {
            label: item.name,
            value: item.id
        }
    })
    console.log(categortyOptions.value)
}

/**
 * 选中分类
 */
const searchByCategory = (categoryId)=>{
    pageInfo.categoryId = categoryId ;
    loadBlogs()
}

//页面跳转
const toDetail = (blog)=>{
    router.push({path:"/detail",query:{id:blog.id}})
}

const homePage = () => {
  pageInfo.keyword = ""
  pageInfo.categoryId = 0
  loadBlogs()
}

const dashboard = () => {
    router.push("/login")
}


</script>

<style lang="scss" scoped>
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 0;
    margin-bottom: 20px;

    .logo {
        display: flex;
        align-items: center;
        gap: 10px;
        
        .site-title {
            margin: 0;
            font-size: 24px;
            font-weight: 700;
            color: var(--vt-c-text-light-1);
            letter-spacing: -0.5px;
        }
    }
}

.nav {
    display: flex;
    gap: 20px;
    align-items: center;

    .nav-item {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        border-radius: var(--radius-md);
        cursor: pointer;
        font-weight: 500;
        transition: all 0.2s ease;
        color: var(--vt-c-text-light-2);

        &:hover, &.active {
            color: var(--accent);
            background-color: var(--accent-light);
        }

        .category-selector {
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .category-badge {
            font-size: 12px;
            background-color: var(--primary-light);
            color: var(--primary);
            padding: 2px 8px;
            border-radius: var(--radius-full);
            margin-left: 6px;
        }
    }
}

.search-container {
    margin-bottom: 24px;
    
    .search-input {
        max-width: 600px;
        margin: 0 auto;
    }
    
    .search-button {
        font-weight: 600;
        background-color: var(--accent) !important;
        color: white !important;
        border: none;
        padding: 0 20px;
        box-shadow: 0 4px 8px rgba(253, 118, 14, 0.3);
        margin-right: 5px;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 5px;
        
        &:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(253, 118, 14, 0.4);
            background-color: var(--accent-hover) !important;
        }
        
        .search-icon {
            margin-right: 4px;
        }
    }
}

.blog-list {
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
    margin-bottom: 30px;

    @media (min-width: 768px) {
        grid-template-columns: repeat(1, 1fr);
    }
}

.blog-card {
    height: 100%;
    display: flex;
    flex-direction: column;
    
    .blog-header {
        padding-bottom: 10px;
        
        .blog-title {
            margin: 0;
            color: var(--vt-c-text-light-1);
            font-size: 20px;
            line-height: 1.4;
        }
    }
    
    .blog-excerpt {
        color: var(--vt-c-text-light-2);
        line-height: 1.6;
        flex-grow: 1;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
    }
    
    .blog-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 16px;
        
        .blog-meta {
            display: flex;
            align-items: center;
            gap: 6px;
            color: var(--vt-c-text-light-2);
            font-size: 14px;
        }
    }
}

.pagination-container {
    display: flex;
    justify-content: center;
    margin: 30px 0;
}

.footer {
    margin-top: 50px;
    padding: 20px 0;
    border-top: 1px solid var(--vt-c-divider-light-2);
    
    .footer-content {
        text-align: center;
        font-size: 14px;
        color: var(--vt-c-text-light-2);
        line-height: 1.6;
    }
}
</style>