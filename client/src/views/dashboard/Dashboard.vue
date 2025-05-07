<template>
  <div class="main-panel">
    <div class="menus">
      <div v-for="(menu, index) in menus" @click="toPage(menu)">
        {{menu.name}}
      </div>
    </div>
    <div class="vertical-line"></div>
    <div style="padding: 20px;width: 100%">
      <router-view></router-view>
    </div>
  </div>
  <div class="title">后台管理系统</div>
</template>

<script setup>
import {reactive, ref, inject} from 'vue'
import {AdminStore} from "@/stores/AdminStore.js";

import {useRouter, useRoute} from "vue-router";
const router = useRouter()
const route = useRoute()

const axios = inject("axios")
const message = inject("message")
const dialog = inject("dialog")
const adminStore = AdminStore()


let menus = [
  {name: "文章管理", href: "/dashboard/article"},
  {name: "分类管理", href: "/dashboard/category"},
  {name: "退出", href: "logout"},
]

const toPage = (menu) => {
  if (menu.href === "logout") {
    dialog.info({
      title: '温馨提示',
      content: `确定退出登录？`,
      positiveText: '退出',
      negativeText: '取消',
      draggable: true,
      onPositiveClick: () => {
        router.push("/login")
      },
      onNegativeClick: () => {
      }
    })
  } else {
    router.push(menu.href)
  }
}
</script>

<style scoped>
.main-panel {
  display: flex;
  color: #64676a;
  max-width: 1500px;
  margin: 0 auto;
}

.vertical-line {
  border-left: 1px solid #dadada;
  align-self: stretch;
}

.menus {
  padding: 20px 0;
  box-sizing: border-box;
  line-height: 55px;
  text-align: center;
  width: 180px;
  height: 95vh;
  border-right: 1px solid #dadada;

  div {
    cursor: pointer;
    &:hover {
      color: #fd760e;
    }
  }
}
.title {
  font-size: 65px;
  font-weight: bold;
  text-align: right;
  position: fixed;
  color: rgba(0, 0, 0, 20%);
  right: calc((100vw - 1500px)/2);
  bottom: 20px;
}
</style>