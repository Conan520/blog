<template>
  <div class="login-panel">
    <n-card title="管理后台登录">
      <n-form :rules="rules" :model="admin">
        <n-form-item path="account" label="账号">
          <n-input v-model:value="admin.account" placeholder="请输入账号"/>
        </n-form-item>
        <n-form-item path="password" label="密码">
          <n-input v-model:value="admin.password" type="password" placeholder="请输入密码"/>
        </n-form-item>
      </n-form>
      <template #footer>
        <n-checkbox v-model:checked="admin.remember" label="记住我"/>
        <n-button @click="login">登录</n-button>
      </template>
    </n-card>

  </div>
</template>


<script setup>
import {reactive, ref, inject} from 'vue'
import {AdminStore} from "@/stores/AdminStore.js";

import {useRouter, useRoute} from "vue-router";

const router = useRouter()
const route = useRoute()

const axios = inject("axios")
const message = inject("message")
const adminStore = AdminStore()

let rules = {
  account: [
    {required: true, message: "请输入账号", trigger: "blur"},
    {min: 3, max: 12, message: "账号长度在3-12个字符", trigger: "blur"}
  ],
  password: [
    {required: true, message: "请输入密码", trigger: "blur"},
    {min: 6, max: 18, message: "密码长度在6-18个字符", trigger: "blur"}
  ],
}

const admin = reactive({
  account: localStorage.getItem("account") || "",
  password: localStorage.getItem("password") || "",
  remember: localStorage.getItem("remember") === "1" || false,
})

async function login() {
  const instance = axios.create({
    headers: {
      "Content-Type": "application/json",
    }
  })
  let result = await instance.post("blog/admin/login", {
    username: admin.account,
    password: admin.password
  })
  console.log(result.data)
  if (result.data.code === 200) {
    adminStore.token = result.data.data.access
    adminStore.account = result.data.data.username
    adminStore.id = result.data.data.id

    if (admin.remember) {
      localStorage.setItem("account", admin.account)
      localStorage.setItem("password", admin.password)
      localStorage.setItem("token", adminStore.token)
      localStorage.setItem("remember", admin.remember ? "1" : "0")
    }
    await router.push("/dashboard/article")
    message.info("登录成功")
  } else {
    message.error("登录失败")
  }
  console.log(result)
}
</script>

<style lang="scss" scoped>
.login-panel {
  width: 500px;
  margin: 130px auto 0;
}
</style>