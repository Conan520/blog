<!-- 富文本组件 -->
<template>
  <div>
    <Toolbar :editor="editorRef" :defaultConfig="toolbarConfig" :mode="mode"
             style="border-bottom: 1px solid #ccc" />
    <Editor :defaultConfig="editorConfig" :mode="mode" v-model="valueHtml" style="height: 400px; overflow-y: hidden"
            @onCreated="handleCreated" @onChange="handleChange" />
  </div>
</template>

<script setup>
import '@wangeditor/editor/dist/css/style.css';
import { ref, reactive, inject, onMounted, onBeforeUnmount, shallowRef } from 'vue'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue';
import axios from "axios";

const server_url = inject("server_url")
// 编辑器实例，必须用 shallowRef，重要！
const editorRef = shallowRef();
const toolbarConfig = { excludeKeys:["uploadVideo"] };
const editorConfig = { placeholder: '请输入内容...' };
editorConfig.MENU_CONF = {}
editorConfig.MENU_CONF['uploadImage'] = {
  // base64LimitSize: 10 * 1024 * 1024, // 10kb
  // server: 'http://127.0.0.1:8000/upload/rich_editor_upload',
  // async customUpload(file, insertFn) {
  //   let imgData = new FormData();
  //   console.log(file);
  //   imgData.append("file", file);
  //   //调用上传图片接口，上传图片
  //   let res = axios.post("/upload/rich_editor_upload", imgData)
  //   console.log(res)
  //   if (res.data.errno === 0) {
  //     insertFn(url, alt, href)
  //   }
  // }
  async customUpload(file, insertFn) {
    let imgData = new FormData();
    imgData.append("file", file);
    //调用上传图片接口，上传图片
    let res = await axios.post("/upload/rich_editor_upload", imgData)
    let imgUrl = res.data.data.url
    if (res.data.errno === 0) {
      insertFn(imgUrl)
    }
  }
}

editorConfig.MENU_CONF['insertImage'] = {
  parseImageSrc:(src) =>{
    if(src.indexOf("http") !==0){
      return `${server_url}${src}`
    }
    return src
  }
}

const mode = ref("default")
const valueHtml = ref("")

const props = defineProps({
  modelValue: {
    type: String,
    default: ""
  }
})

const emit = defineEmits(["update:model-value"])
let initFinished = false

onMounted(() => {
  setTimeout(() => {
    valueHtml.value = props.modelValue;
    initFinished = true;
  }, 200);
});

// 组件销毁时，也及时销毁编辑器，重要！
onBeforeUnmount(() => {
  const editor = editorRef.value;
  if (editor == null) return;
  editor.destroy();
});

// 编辑器回调函数
const handleCreated = (editor) => {
  editorRef.value = editor; // 记录 editor 实例，重要！
};
const handleChange = (editor) => {
  if (initFinished) {
    emit("update:model-value", valueHtml.value)
  }
};

</script>

<style lang="scss" scoped>
</style>