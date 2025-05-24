<template>
  <n-card class="dashboard-container">
    <div class="header-actions">
      <h3 class="section-title">分类管理</h3>
      <n-button type="primary" @click="showAddModal = true" class="add-button">
        <template #icon><n-icon><plus /></n-icon></template>
        添加新分类
      </n-button>
    </div>
    
    <div class="search-container">
      <n-input v-model:value="searchQuery" placeholder="搜索分类..." class="search-input">
        <template #prefix>
          <n-icon><search /></n-icon>
        </template>
      </n-input>
    </div>

    <n-empty v-if="filteredCategories.length === 0" description="暂无分类" />
    <n-card v-else class="table-card" embedded>
      <n-data-table
        :columns="columns"
        :data="filteredCategories"
        :bordered="true"
        :single-line="false"
        size="small"
        :pagination="{ pageSize: 10 }"
        :row-class-name="rowClassName"
      />
    </n-card>
  </n-card>
  <n-modal v-model:show="showAddModal" preset="card" style="width: 450px" title="添加新分类" :bordered="false">
    <n-form>
      <n-form-item label="分类名称" required>
        <n-input v-model:value="addCategory.name" placeholder="请输入分类名称" type="text" clearable autofocus />
      </n-form-item>
      <div class="form-actions">
        <n-button @click="showAddModal = false" quaternary>取消</n-button>
        <n-button @click="add" type="primary" :disabled="!addCategory.name.trim()">
          <template #icon><n-icon><save /></n-icon></template>
          保存
        </n-button>
      </div>
    </n-form>
  </n-modal>
  
  <n-modal v-model:show="showUpdateModal" preset="card" style="width: 450px" title="修改分类" :bordered="false">
    <n-form>
      <n-form-item label="分类名称" required>
        <n-input v-model:value="updateCategory.name" placeholder="请输入修改后的名称" type="text" clearable autofocus />
      </n-form-item>
      <div class="form-actions">
        <n-button @click="showUpdateModal = false" quaternary>取消</n-button>
        <n-button @click="update" type="primary" :disabled="!updateCategory.name.trim()">
          <template #icon><n-icon><save /></n-icon></template>
          保存
        </n-button>
      </div>
    </n-form>
  </n-modal>
</template>

<script setup>
import { inject, onMounted, reactive, ref, computed, h } from 'vue'
import { AdminStore } from "@/stores/AdminStore.js";
import { useRoute, useRouter } from "vue-router";
import {
  AddOutline as Plus,
  SearchOutline as Search,
  SaveOutline as Save
} from '@vicons/ionicons5';
import {NButton, NGradientText, NText} from "naive-ui";

const router = useRouter()
const route = useRoute()

const axios = inject("axios")
const message = inject("message")
const dialog = inject("dialog")
const adminStore = AdminStore()

const categoryList = ref([])
const searchQuery = ref('')
const showAddModal = ref(false)
const showUpdateModal = ref(false)
const addCategory = reactive({
  name: ""
})
const updateCategory = reactive({
  name: "",
  id: 0
})

// Filter categories based on search query
const filteredCategories = computed(() => {
  if (!searchQuery.value) return categoryList.value;
  const query = searchQuery.value.toLowerCase();
  return categoryList.value.filter(category => 
    category.name.toLowerCase().includes(query)
  );
});

function renderTooltip(trigger, content) {
  return h(NTooltip, null, {
    trigger: () => trigger,
    default: () => content
  })
}

// Table columns configuration
const columns = [
  {
    title: "编号",
    key: 'id',
    sorter: 'default',
    width: 200
  },
  {
    title: '名称',
    key: 'name',
    className: 'category-name'
  },
  {
    title: '操作',
    key: 'actions',
    width: 150,
    render: (row) => {
      return h('div', { class: 'action-buttons' }, [
        h(
          NButton,
          {
            size: 'small',
            // strong: true,
            type: 'primary',
            // ghost: true,
            onClick: () => toUpdate(row),
            style: 'margin-right: 8px;'
          },
          { default: () => '编辑', }
        ),
        h(
          NButton,
          {
            size: 'small',
            type: 'error',
            // ghost: true,
            onClick: () => deleteCategory(row)
          },
          { default: () => '删除', }
        )
      ])
    }
  }
];

// Row class based on index for zebra striping
const rowClassName = (row) => {
  return row.index % 2 === 0 ? 'even-row' : 'odd-row';
};

onMounted(
    () => {
      adminStore.token = localStorage.getItem("token")
      if (!localStorage.getItem("token")) {
        router.push("/login")
      }
      loadDatas()
    }
)

const loadDatas = async () => {
  let res = await axios.get("/category/list")
  console.log(res)
  if (res.status === 401) {
    message.error("请先登录")
    await router.push("/login")
    return
  }
  categoryList.value = res.data.data
  console.log(res)
}

const add = async () => {
  let res = await axios.post("/category/add", {name: addCategory.name})
  console.log("addCategory", res)
  if (res.data.code === 200) {
    console.log("addCategory success")
    await loadDatas()
    message.info(res.data.msg)
  } else {
    message.error(res.data.msg)
  }
  showAddModal.value = false
  console.log(res)
}

const toUpdate = async (category) => {
  showUpdateModal.value = true
  updateCategory.id = category.id
  updateCategory.name = category.name
}

const update = async () => {
  let res = await axios.put("/category", {id: updateCategory.id, name: updateCategory.name})
  if (res.data.code === 200) {
    await loadDatas()
    message.info(res.data.msg)
  } else {
    message.error(res.data.msg)
  }
  showUpdateModal.value = false
  console.log(res)
}

const deleteCategory = async (category) => {
  dialog.warning({
    title: '警告',
    content: `是否要删除名称为${category.name}的分类？`,
    positiveText: '确定',
    negativeText: '取消',
    draggable: true,
    onPositiveClick: async () => {
      let res = await axios.delete(`/category/${category.id}`)
      if (res.data.code === 200) {
        await loadDatas()
        message.info(res.data.msg)
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

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 16px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: #333;
}

.search-container {
  margin-bottom: 16px;
}

.search-input {
  width: 300px;
  max-width: 100%;
}

.table-card {
  margin-top: 16px;
  box-shadow: none;
}

.action-buttons {
  display: flex;
  justify-content: flex-end;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 24px;
  gap: 12px;
}

.add-button {
  min-width: 120px;
}

:deep(.even-row td) {
  font-weight: 700;
  color: rgb(204, 86, 86);
}

:deep(.odd-row) {
  color: #ba5555;
}

:deep(.category-name) {
  font-weight: 500;
  color: #333;
}
</style>