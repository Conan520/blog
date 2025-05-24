<template>
    <div class="page-container">
        <div class="article-header">
            <n-button @click="back" size="large" class="back-button">
                <template #icon>
                    <n-icon>
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="m10 18l-6-6l6-6l1.4 1.45L6.85 12l4.55 4.55z"/></svg>
                    </n-icon>
                </template>
                返回
            </n-button>
        </div>

        <div class="article-container">
            <!-- 标题 -->
            <h1 class="article-title">{{ blogInfo.title }}</h1>
            
            <div class="article-meta" v-if="blogInfo.create_time">
                <n-icon size="16" color="var(--vt-c-text-light-2)">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10s10-4.5 10-10S17.5 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8s8 3.59 8 8s-3.59 8-8 8zm.5-13H11v6l5.2 3.2l.8-1.3l-4.5-2.7V7z"/></svg>
                </n-icon>
                <span>发布于: {{ formatDate(blogInfo.create_time) }}</span>
            </div>
            
            <!-- 文章内容 -->
            <div class="blog-content">
                <n-card>
                    <div v-html="blogInfo.content"></div>
                </n-card>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, inject, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const blogInfo = ref({})
const axios = inject("axios")

onMounted(() => {
    loadBlog()
})

/**
 * 读取文章详情
 */
const loadBlog = async () => {
    let res = await axios.get("/blog/detail/" + route.query.id)
    blogInfo.value = res.data.data;
}

// Format timestamp to readable date
const formatDate = (timestamp) => {
    if (!timestamp) return '';
    const d = new Date(timestamp * 1000);
    return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日 ${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}`;
}

const back = () => {
    router.push("/")
}

</script>

<style>
.blog-content img {
    max-width: 100% !important;
    border-radius: var(--radius-md);
}
</style>

<style lang="scss" scoped>
.page-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    animation: fadeIn 0.4s ease;
}

.article-header {
    margin-bottom: 24px;
    
    .back-button {
        border-radius: var(--radius-md);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        
        &:hover {
            transform: translateX(-3px);
            box-shadow: var(--shadow-md);
        }
    }
}

.article-container {
    max-width: 800px;
    margin: 0 auto;
}

.article-title {
    font-size: 32px;
    color: var(--vt-c-text-light-1);
    margin-bottom: 16px;
    line-height: 1.3;
    font-weight: 700;
}

.article-meta {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 24px;
    font-size: 14px;
    color: var(--vt-c-text-light-2);
}

.blog-content {
    line-height: 1.8;
    font-size: 16px;
    
    .n-card {
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-md);
        padding: 0;
        
        :deep(h1, h2, h3, h4, h5, h6) {
            margin-top: 1.5em;
            margin-bottom: 0.75em;
            color: var(--vt-c-text-light-1);
        }
        
        :deep(p) {
            margin-bottom: 1rem;
            line-height: 1.8;
        }
        
        :deep(a) {
            color: var(--primary);
            text-decoration: none;
            
            &:hover {
                text-decoration: underline;
            }
        }
        
        :deep(ul, ol) {
            padding-left: 1.5em;
            margin-bottom: 1rem;
        }
        
        :deep(blockquote) {
            border-left: 4px solid var(--primary);
            padding-left: 1rem;
            color: var(--vt-c-text-light-2);
            font-style: italic;
            margin: 1rem 0;
        }
        
        :deep(pre) {
            background-color: var(--vt-c-black-soft);
            padding: 1rem;
            border-radius: var(--radius-md);
            overflow-x: auto;
            margin: 1rem 0;
        }
        
        :deep(code) {
            font-family: monospace;
            background-color: var(--vt-c-black-soft);
            padding: 2px 4px;
            border-radius: var(--radius-sm);
        }
    }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>