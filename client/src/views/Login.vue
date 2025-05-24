<template>
  <div class="login-container">
    <div class="login-panel">
      <div class="login-header">
        <n-icon size="48" color="var(--primary)">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M4 21q-.825 0-1.412-.587T2 19V5q0-.825.588-1.412T4 3h16q.825 0 1.413.588T22 5v14q0 .825-.587 1.413T20 21H4Zm0-2h16V9H4v10Zm5-1q-.825 0-1.412-.587T7 16V6h2v10h9v2H9Zm-5-9h16V5H4v4Zm0 0V5v4Z"/></svg>
        </n-icon>
        <h2 class="login-title">管理后台登录</h2>
      </div>
      
      <n-card class="login-card" bordered="false">
        <n-form :rules="rules" :model="admin">
          <n-form-item path="account">
            <n-input 
              v-model:value="admin.account" 
              placeholder="请输入账号"
              round
              size="large"
              class="login-input">
              <template #prefix>
                <n-icon>
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M12 3c2.76 0 5 2.24 5 5c0 1.91-1.09 3.54-2.65 4.37A1.998 1.998 0 0 1 16 14v.62c0 .27-.04.53-.09.79C19 16.53 21 18.74 21 21.5c0 .28-.22.5-.5.5h-17C3.22 22 3 21.78 3 21.5c0-2.76 2-4.97 5.09-5.09c-.05-.26-.09-.52-.09-.79V14c0-.83.52-1.58 1.3-1.87C8.12 11.36 7 9.57 7 7.5C7 4.46 9.24 2 12 2zm0 2c-1.65 0-3 1.35-3 3c0 1.3.84 2.4 2 2.82V9c0 .55.45 1 1 1s1-.45 1-1V8.82c1.16-.41 2-1.51 2-2.82c0-1.65-1.35-3-3-3zm-4.5 12c-1.02 0-1.92.39-2.62 1h10.24c-.7-.61-1.6-1-2.62-1h-5z"/></svg>
                </n-icon>
              </template>
            </n-input>
          </n-form-item>
          <n-form-item path="password">
            <n-input 
              v-model:value="admin.password" 
              type="password" 
              placeholder="请输入密码"
              round
              size="large"
              class="login-input">
              <template #prefix>
                <n-icon>
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M12 17a2 2 0 1 1 0-4a2 2 0 0 1 0 4Zm-1-10v3h2V7h-2Zm1 13a8 8 0 1 1 0-16a8 8 0 0 1 0 16Zm0-2a6 6 0 1 0 0-12a6 6 0 0 0 0 12Z"/></svg>
                </n-icon>
              </template>
            </n-input>
          </n-form-item>
          
          <div class="login-options">
            <n-checkbox v-model:checked="admin.remember">
              <span class="remember-text">记住我</span>
            </n-checkbox>
          </div>
          
          <n-button 
            type="primary" 
            class="login-button" 
            size="large" 
            block 
            @click="login">登录</n-button>
          
          <div class="login-back">
            <n-button text @click="goBack">
              <template #icon>
                <n-icon>
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="m10 18l-6-6l6-6l1.4 1.45L6.85 12l4.55 4.55z"/></svg>
                </n-icon>
              </template>
              返回博客首页
            </n-button>
          </div>
        </n-form>
      </n-card>
    </div>
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

const goBack = () => {
  router.push("/")
}

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
  console.log(result)
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
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, var(--primary-light) 0%, var(--accent-light) 100%);
  padding: 20px;
}

.login-panel {
  width: 400px;
  animation: fadeIn 0.6s ease;
}

.login-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
  gap: 10px;
  
  .login-title {
    color: var(--vt-c-text-light-1);
    font-size: 24px;
    font-weight: 600;
    margin: 0;
  }
}

.login-card {
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  overflow: hidden;
}

.login-input {
  margin-bottom: 5px;
}

.login-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 16px 0;
  
  .remember-text {
    font-size: 14px;
    color: var(--vt-c-text-light-2);
  }
}

.login-button {
  margin: 20px 0;
  height: 46px;
  font-size: 16px;
  font-weight: 500;
  border-radius: var(--radius-full);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
  
  &:active {
    transform: translateY(0);
  }
}

.login-back {
  text-align: center;
  margin-top: 16px;
  
  .n-button {
    color: var(--vt-c-text-light-2);
    font-size: 14px;
    
    &:hover {
      color: var(--primary);
    }
  }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>