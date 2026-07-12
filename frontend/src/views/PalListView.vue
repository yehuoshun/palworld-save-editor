<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const pals = ref<any[]>([])
const loading = ref(true)
const savePath = ref(localStorage.getItem('savePath') || '')
const search = ref('')

onMounted(async () => {
  await loadPals()
})

async function loadPals() {
  if (!savePath.value) return
  loading.value = true
  try {
    const res = await fetch(`/api/pals?save_path=${encodeURIComponent(savePath.value)}`)
    const data = await res.json()
    if (data.success) {
      pals.value = data.pals
      localStorage.setItem('savePath', savePath.value)
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function openDetail(id: string) {
  router.push(`/pal/${id}`)
}

const filteredPals = computed(() => {
  if (!search.value) return pals.value
  const q = search.value.toLowerCase()
  return pals.value.filter((p: any) =>
    p.nickname?.toLowerCase().includes(q) || p.character_id?.toLowerCase().includes(q)
  )
})
</script>

<template>
  <div>
    <div class="flex items-center gap-4 mb-4">
      <h2 class="text-xl font-bold">🐾 帕鲁列表</h2>
      <input
        v-model="search"
        placeholder="搜索名称或ID..."
        class="w-64"
      />
      <button
        class="px-4 py-1.5 bg-[var(--color-primary)] text-black font-semibold rounded-lg text-sm hover:opacity-90"
        @click="loadPals"
      >
        刷新
      </button>
    </div>

    <!-- 存档路径 -->
    <div v-if="!savePath" class="bg-[var(--color-bg-surface)] rounded-xl p-4 mb-4">
      <div class="flex gap-3">
        <input v-model="savePath" placeholder="存档路径" class="flex-1" />
        <button class="px-4 py-2 bg-[var(--color-primary)] text-black font-semibold rounded-lg text-sm" @click="loadPals">
          加载
        </button>
      </div>
    </div>

    <div v-if="loading" class="text-[var(--color-text-muted)] text-center mt-20">加载中...</div>

    <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3">
      <div
        v-for="pal in filteredPals"
        :key="pal.instance_id"
        class="bg-[var(--color-bg-surface)] rounded-xl p-3 cursor-pointer card-hover"
        @click="openDetail(pal.instance_id)"
      >
        <div class="text-sm font-semibold truncate">{{ pal.nickname || pal.character_id }}</div>
        <div class="text-xs text-[var(--color-text-muted)]">Lv.{{ pal.level }} · {{ pal.gender }}</div>
        <div class="mt-2 text-xs text-[var(--color-accent)]">HP {{ pal.hp }}</div>
      </div>
    </div>

    <div v-if="!loading && filteredPals.length === 0" class="text-[var(--color-text-muted)] text-center mt-20">
      暂无帕鲁数据
    </div>
  </div>
</template>