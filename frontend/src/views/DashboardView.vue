<script setup lang="ts">
import { ref } from 'vue'

const savePath = ref('')
const loading = ref(false)
const info = ref<any>(null)
const error = ref('')

async function loadSave() {
  if (!savePath.value) return
  loading.value = true
  error.value = ''
  try {
    const res = await fetch('/api/load', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ save_path: savePath.value }),
    })
    const data = await res.json()
    if (data.success) {
      info.value = data.info
    } else {
      error.value = data.error
    }
  } catch (e: any) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div>
    <h2 class="text-xl font-bold mb-4">📊 仪表盘</h2>

    <!-- 加载存档 -->
    <div class="bg-[var(--color-bg-surface)] rounded-xl p-4 mb-6">
      <div class="flex gap-3">
        <input
          v-model="savePath"
          placeholder="存档路径，如 C:\...\Level.sav"
          class="flex-1"
          @keyup.enter="loadSave"
        />
        <button
          class="px-5 py-2 bg-[var(--color-primary)] text-black font-semibold rounded-lg hover:opacity-90 disabled:opacity-50"
          :disabled="loading"
          @click="loadSave"
        >
          {{ loading ? '加载中...' : '加载存档' }}
        </button>
      </div>
      <p v-if="error" class="mt-2 text-sm text-[var(--color-danger)]">{{ error }}</p>
    </div>

    <!-- 世界信息 -->
    <div v-if="info" class="grid grid-cols-4 gap-4">
      <div class="bg-[var(--color-bg-surface)] rounded-xl p-4">
        <div class="text-xs text-[var(--color-text-muted)] mb-1">世界名称</div>
        <div class="text-lg font-semibold">{{ info.world_name }}</div>
      </div>
      <div class="bg-[var(--color-bg-surface)] rounded-xl p-4">
        <div class="text-xs text-[var(--color-text-muted)] mb-1">帕鲁</div>
        <div class="text-lg font-semibold text-[var(--color-primary)]">{{ info.pal_count }}</div>
      </div>
      <div class="bg-[var(--color-bg-surface)] rounded-xl p-4">
        <div class="text-xs text-[var(--color-text-muted)] mb-1">玩家</div>
        <div class="text-lg font-semibold text-[var(--color-accent)]">{{ info.player_count }}</div>
      </div>
      <div class="bg-[var(--color-bg-surface)] rounded-xl p-4">
        <div class="text-xs text-[var(--color-text-muted)] mb-1">公会</div>
        <div class="text-lg font-semibold text-[var(--color-warm)]">{{ info.guild_count }}</div>
      </div>
    </div>

    <div v-else-if="!loading" class="text-[var(--color-text-muted)] text-center mt-20">
      输入存档路径并点击"加载存档"开始
    </div>
  </div>
</template>