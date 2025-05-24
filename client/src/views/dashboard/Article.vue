<template>
  <n-card class="dashboard-container">
    <n-tabs v-model:value="tabValue" justify-content="start" type="line" animated>
      <n-tab-pane name="list" tab="文章列表">
        <div class="action-bar">
          <n-button type="primary" @click="tabValue = 'add'" class="add-button">
            <template #icon><n-icon><plus /></n-icon></template>
            添加新文章
          </n-button>
          <n-input v-model:value="searchQuery" placeholder="搜索文章..." class="search-input">
            <template #prefix>
              <n-icon><search /></n-icon>
            </template>
          </n-input>
        </div>

        <n-empty v-if="filteredBlogs.length === 0" description="暂无文章" />
        <div v-else>
          <div v-for="(blog, index) in filteredBlogs" :key="blog.id" class="blog-card-container">
            <n-card :title="blog.title" class="blog-card" hoverable>
              <n-ellipsis :line-clamp="2" class="blog-content">
                {{ blog.content }}
              </n-ellipsis>

              <template #footer>
                <div class="blog-footer">
                  <div class="blog-info">
                    <n-tag type="info" size="small">
                      <template #icon>
                        <n-icon><calendar /></n-icon>
                      </template>
                      {{ blog.create_time }}
                    </n-tag>
                  </div>
                  <div class="blog-actions">
                    <n-button size="small" type="primary" @click="toUpdate(blog)">
                      <template #icon><n-icon><edit /></n-icon></template>
                      编辑
                    </n-button>
                    <n-button size="small" type="error" ghost @click="toDelete(blog)">
                      <template #icon><n-icon><trash /></n-icon></template>
                      删除
                    </n-button>
                  </div>
                </div>
              </template>
            </n-card>
          </div>
        </div>

        <div class="pagination-container">
          <n-pagination v-model:page="page" :page-count="pageInfo.pageCount" @update:page="toPage" size="medium" />
        </div>
      </n-tab-pane>
    <n-tab-pane name="add" tab="添加文章">
      <n-card class="form-card">
        <n-form>
          <n-grid :cols="24" :x-gap="24">
            <n-form-item-gi :span="24" label="标题">
              <n-input v-model:value="addArticle.title" placeholder="请输入标题" clearable />
            </n-form-item-gi>
            <n-form-item-gi :span="24" label="分类">
              <n-select v-model:value="addArticle.categoryId" :options="categortyOptions" clearable placeholder="选择文章分类" />
            </n-form-item-gi>
            <n-form-item-gi :span="24" label="内容">
              <div class="editor-container">
                <rich-text-editor v-model="addArticle.content"></rich-text-editor>
              </div>
            </n-form-item-gi>
            <n-form-item-gi :span="24">
              <div class="form-actions">
                <n-button type="default" @click="tabValue = 'list'">
                  <template #icon><n-icon><arrow-left /></n-icon></template>
                  返回列表
                </n-button>
                <n-button type="primary" @click="add">
                  <template #icon><n-icon><save /></n-icon></template>
                  保存文章
                </n-button>
              </div>
            </n-form-item-gi>
          </n-grid>
        </n-form>
      </n-card>
    </n-tab-pane>

    <n-tab-pane name="update" tab="修改文章">
      <n-card class="form-card">
        <n-form>
          <n-grid :cols="24" :x-gap="24">
            <n-form-item-gi :span="24" label="标题">
              <n-input v-model:value="updateArticle.title" placeholder="请输入标题" clearable />
            </n-form-item-gi>
            <n-form-item-gi :span="24" label="分类">
              <n-select v-model:value="updateArticle.categoryId" :options="categortyOptions" clearable placeholder="选择文章分类" />
            </n-form-item-gi>
            <n-form-item-gi :span="24" label="内容">
              <div class="editor-container">
                <rich-text-editor v-model="updateArticle.content"></rich-text-editor>
              </div>
            </n-form-item-gi>
            <n-form-item-gi :span="24">
              <div class="form-actions">
                <n-button type="default" @click="tabValue = 'list'">
                  <template #icon><n-icon><arrow-left /></n-icon></template>
                  返回列表
                </n-button>
                <n-button type="primary" @click="update">
                  <template #icon><n-icon><save /></n-icon></template>
                  更新文章
                </n-button>
              </div>
            </n-form-item-gi>
          </n-grid>
        </n-form>
      </n-card>
    </n-tab-pane>
  </n-tabs>
  </n-card>
</template>

<script setup>
import { AdminStore } from '@/stores/AdminStore.js'
import { ref, reactive, inject, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import RichTextEditor from '../../components/RichTextEditor.vue'
import { 
  CalendarOutline as Calendar,
  TrashOutline as Trash,
  CreateOutline as Edit,
  AddOutline as Plus,
  SearchOutline as Search,
  ArrowBackOutline as ArrowLeft,
  SaveOutline as Save
} from '@vicons/ionicons5'
const router = useRouter()  //用于做路由跳转
const route = useRoute()

const message = inject("message")
const dialog = inject("dialog")
const axios = inject("axios")

const adminStore = AdminStore()
const page = ref(1)
const searchQuery = ref('')

//文章添加数据
const addArticle = reactive({
  categoryId: 0,
  title: "",
  content: "",
})

//文章修改数据
const updateArticle = reactive({
  id: 0,
  categoryId: 0,
  title: "",
  content: "",
})

//分类选项
const categortyOptions = ref([])
const blogListInfo = ref([])

// 根据搜索查询过滤博客
const filteredBlogs = computed(() => {
  if (!searchQuery.value) return blogListInfo.value
  const query = searchQuery.value.toLowerCase()
  return blogListInfo.value.filter(blog => 
    blog.title.toLowerCase().includes(query) || 
    blog.content.toLowerCase().includes(query)
  )
})
//标签页
const tabValue = ref("list")

//分页数据
const pageInfo = reactive({
  page: 1,
  pageSize: 3,
  pageCount: 0,
  count: 0,
})

onMounted(() => {
  loadBlogs()
  loadCategorys()
})

//读取博客列表
const loadBlogs = async () => {
  let res = await axios.get(`/blog/search?page=${pageInfo.page}&pageSize=${pageInfo.pageSize}`)
  let temp_rows = res.data.data.results;
  console.log(res)
  for (let row of temp_rows) {
    row.content += "..."
    let d = new Date(row.create_time*1000)
    row.create_time = `${d.getFullYear()}/${d.getMonth() + 1}/${d.getDate()} ${d.getHours()}:${d.getMinutes()}`
  }
  blogListInfo.value = temp_rows;
  pageInfo.count = res.data.data.count;
  pageInfo.pageCount = parseInt(pageInfo.count / pageInfo.pageSize) + (pageInfo.count % pageInfo.pageSize > 0 ? 1 : 0)
}

//读取分类
const loadCategorys = async () => {
  let res = await axios.get("/category/list")
  categortyOptions.value = res.data.data.map((item) => {
    return {
      label: item.name,
      value: item.id
    }
  })
}

const add = async () => {
  let res = await axios.post("/blog/add", addArticle)
  if (res.data.code === 200) {
    message.info(res.data.msg)
    await loadBlogs()
  } else {
    message.error(res.data.msg)
  }
}

const toPage = (pageNum) => {
  console.log(pageNum)
  page.value = pageNum
  pageInfo.page = pageNum
  loadBlogs()
}

const toUpdate = async (blog) => {
  tabValue.value = "update"
  let res = await axios.get("/blog/detail/" + blog.id)
  console.log(res)
  updateArticle.id = blog.id
  updateArticle.title = res.data.data.title
  updateArticle.content = res.data.data.content
  updateArticle.categoryId = res.data.data.category_id
}

const update = async () => {
  let res = await axios.put("/blog/update", updateArticle)
  if (res.data.code === 200) {
    message.info(res.data.msg)
    await loadBlogs()
    tabValue.value = "list"
  } else {
    message.error(res.data.msg)
  }
}

const toDelete = async (blog) => {
  dialog.warning({
    title: '警告',
    content: `是否要删除名称为${blog.title}的文章？`,
    positiveText: '确定',
    negativeText: '取消',
    draggable: true,
    onPositiveClick: async () => {
      let res = await axios.delete("/blog/"+blog.id)
      if (res.data.code === 200) {
        message.info(res.data.msg)
        await loadBlogs()
      } else {
        message.error(res.data.msg)
      }
    },
    onNegativeClick: () => {
    }
  })
}

</script>

<style lang="scss" scoped>
.dashboard-container {
  margin-bottom: 24px;
}

.action-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
  gap: 16px;
  flex-wrap: wrap;
}

.add-button {
  min-width: 120px;
}

.search-input {
  width: 300px;
  flex-shrink: 0;
}

.blog-card-container {
  margin-bottom: 16px;
}

.blog-card {
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-2px);
  }
}

.blog-content {
  margin: 16px 0;
  color: #666;
  line-height: 1.6;
}

.blog-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.blog-actions {
  display: flex;
  gap: 8px;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

.editor-container {
  border: 1px solid #e9e9e9;
  border-radius: 3px;
  margin-top: 8px;
  min-height: 400px;
}

.form-card {
  margin-top: 16px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  margin-top: 24px;
}
</style>