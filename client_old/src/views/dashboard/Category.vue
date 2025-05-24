<template>
  <div>
    <n-button @click="showAddModal = true">
      添加
    </n-button>
    <n-space vertical>
      <n-table :bordered="false" :single-line="false" size="small">
        <thead>
        <tr>
          <th>编号</th>
          <th>名称</th>
          <th>操作</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(category, index) in categoryList">
          <td>{{ category.id }}</td>
          <td>{{ category.name }}</td>
          <td>
            <n-space>
              <n-button @click="toUpdate(category)">修改</n-button>
              <n-button @click="deleteCategory(category)">删除</n-button>
            </n-space>
          </td>
        </tr>
        </tbody>
      </n-table>
    </n-space>
  </div>
  <n-modal v-model:show="showAddModal" preset="dialog" title="Dialog">
    <template #header>
      <div>添加分类</div>
    </template>
    <div>
      <n-input v-model:value="addCategory.name" placeholder="请输入名称" type="text"/>
    </div>
    <template #action>
      <div>
        <n-button @click="add">提交</n-button>
      </div>
    </template>
  </n-modal>
  <n-modal v-model:show="showUpdateModal" preset="dialog" title="Dialog">
    <template #header>
      <div>修改分类</div>
    </template>
    <div>
      <n-input v-model:value="updateCategory.name" placeholder="请输入修改后的名称" type="text"/>
    </div>
    <template #action>
      <div>
        <n-button @click="update">提交</n-button>
      </div>
    </template>
  </n-modal>
</template>

<script setup>
import {inject, onMounted, reactive, ref} from 'vue'
import {AdminStore} from "@/stores/AdminStore.js";

import {useRoute, useRouter} from "vue-router";

const router = useRouter()
const route = useRoute()


const axios = inject("axios")
const message = inject("message")
const dialog = inject("dialog")
const adminStore = AdminStore()

const categoryList = ref([])
const showAddModal = ref(false)
const showUpdateModal = ref(false)
const addCategory = reactive({
  name: ""
})
const updateCategory = reactive({
  name: ""
})
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
}

const add = async () => {
  let res = await axios.post("/category/add", {name: addCategory.name})
  if (res.data.code === 200) {
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

</style>