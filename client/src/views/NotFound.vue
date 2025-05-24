<template>
  <div class="not-found-container">
    <div class="not-found-content">
      <div class="not-found-image">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 300" class="illustration">
          <!-- Background shapes -->
          <circle cx="250" cy="150" r="100" fill="#e1f0fa" />
          <circle cx="150" cy="80" r="40" fill="#ffecdf" />
          <circle cx="350" cy="220" r="30" fill="#e1f0fa" />
          
          <!-- Documents and magnifying glass illustration -->
          <g class="documents">
            <!-- Main document -->
            <rect x="180" y="100" width="100" height="130" rx="5" fill="white" stroke="#ddd" stroke-width="2" />
            <line x1="200" y1="120" x2="260" y2="120" stroke="#ccc" stroke-width="2" />
            <line x1="200" y1="140" x2="240" y2="140" stroke="#ccc" stroke-width="2" />
            <line x1="200" y1="160" x2="250" y2="160" stroke="#ccc" stroke-width="2" />
            
            <!-- Document stack -->
            <rect x="170" y="110" width="100" height="130" rx="5" fill="white" stroke="#ddd" stroke-width="2" transform="rotate(-5)" />
            <rect x="160" y="120" width="100" height="130" rx="5" fill="white" stroke="#ddd" stroke-width="2" transform="rotate(-10)" />
          </g>
          
          <!-- Magnifying glass -->
          <g class="magnifying-glass">
            <circle cx="300" cy="120" r="35" fill="none" stroke="var(--primary)" stroke-width="6" />
            <line x1="325" y1="145" x2="355" y2="175" stroke="var(--primary)" stroke-width="6" stroke-linecap="round" />
            <text x="278" y="135" font-family="Arial" font-size="30" font-weight="bold" fill="var(--accent)">?</text>
          </g>
          
          <!-- 404 text as part of illustration -->
          <text x="180" y="240" font-family="Arial" font-size="24" font-weight="bold" fill="var(--text-color-light)">404</text>
        </svg>
      </div>

      <h1 class="not-found-title">404</h1>
      <h2 class="not-found-subtitle">页面未找到</h2>
      <p class="not-found-message">
        很抱歉，您访问的页面不存在或已被移动。
      </p>

      <div class="search-container">
        <n-input 
          v-model:value="searchKeyword" 
          class="search-input" 
          placeholder="搜索文章内容..."
          round>
          <template #prefix>
            <n-icon>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path fill="currentColor" d="m19.6 21l-6.3-6.3q-.75.6-1.725.95T9.5 16q-2.725 0-4.612-1.888T3 9.5q0-2.725 1.888-4.612T9.5 3q2.725 0 4.612 1.888T16 9.5q0 1.1-.35 2.075T14.7 13.3l6.3 6.3l-1.4 1.4ZM9.5 14q1.875 0 3.188-1.313T14 9.5q0-1.875-1.313-3.188T9.5 5Q7.625 5 6.312 6.313T5 9.5q0 1.875 1.313 3.188T9.5 14Z"/>
              </svg>
            </n-icon>
          </template>
          <template #suffix>
            <n-button type="primary" class="search-button" round @click="handleSearch">
              <n-icon size="16" class="search-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                  <path fill="currentColor" d="m19.6 21l-6.3-6.3q-.75.6-1.725.95T9.5 16q-2.725 0-4.612-1.888T3 9.5q0-2.725 1.888-4.612T9.5 3q2.725 0 4.612 1.888T16 9.5q0 1.1-.35 2.075T14.7 13.3l6.3 6.3l-1.4 1.4ZM9.5 14q1.875 0 3.188-1.313T14 9.5q0-1.875-1.313-3.188T9.5 5Q7.625 5 6.312 6.313T5 9.5q0 1.875 1.313 3.188T9.5 14Z"/>
                </svg>
              </n-icon>
              搜索
            </n-button>
          </template>
        </n-input>
      </div>

      <div class="action-buttons">
        <n-button 
          type="primary" 
          class="home-button"
          size="large"
          @click="goToHome">
          <template #icon>
            <n-icon>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path fill="currentColor" d="M10 20v-6h4v6h5v-8h3L12 3L2 12h3v8z"/>
              </svg>
            </n-icon>
          </template>
          返回首页
        </n-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useMessage } from 'naive-ui';

const router = useRouter();
const message = useMessage();
const searchKeyword = ref('');

const goToHome = () => {
  router.push('/');
};

const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    router.push({
      path: '/',
      query: { keyword: searchKeyword.value }
    });
  } else {
    message.warning('请输入搜索关键词');
  }
};
</script>

<style scoped lang="scss">
.not-found-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem;
  background-color: var(--bg-color);
  color: var(--text-color);
}

.not-found-content {
  max-width: 600px;
  text-align: center;
  animation: fadeIn 0.6s ease-out;
}

.not-found-image {
  width: 100%;
  max-width: 400px;
  margin: 0 auto 2rem;
  
  img {
    width: 100%;
    height: auto;
  }
}

.not-found-title {
  font-size: 8rem;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(to right, var(--primary), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1;
}

.not-found-subtitle {
  font-size: 2.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: var(--text-color);
}

.not-found-message {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  color: var(--text-color-light);
}

.search-container {
  margin-bottom: 2rem;
  width: 100%;
  
  .search-input {
    width: 100%;
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

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  
  .home-button {
    background-color: var(--primary);
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    min-width: 150px;
    
    &:hover {
      background-color: var(--primary-hover);
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
    }
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .not-found-title {
    font-size: 6rem;
  }
  
  .not-found-subtitle {
    font-size: 2rem;
  }
}

@media (max-width: 480px) {
  .not-found-title {
    font-size: 4rem;
  }
  
  .not-found-subtitle {
    font-size: 1.5rem;
  }
  
  .not-found-message {
    font-size: 1rem;
  }
}
</style>