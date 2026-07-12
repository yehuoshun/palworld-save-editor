<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()

const navItems = [
  { path: '/', label: '仪表盘', icon: '📊' },
  { path: '/pals', label: '帕鲁', icon: '🐾' },
]

function isActive(path: string) {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}
</script>

<template>
  <aside class="w-52 bg-[var(--color-bg-card)] border-r border-[var(--color-border)] flex flex-col">
    <div class="p-4 border-b border-[var(--color-border)]">
      <h1 class="text-lg font-bold text-[var(--color-primary)]">Pal Editor</h1>
      <p class="text-xs text-[var(--color-text-muted)]">存档编辑器</p>
    </div>

    <nav class="flex-1 p-2 space-y-1">
      <router-link
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors"
        :class="isActive(item.path)
          ? 'bg-[var(--color-primary)]/10 text-[var(--color-primary)]'
          : 'text-[var(--color-text-muted)] hover:bg-white/5 hover:text-[var(--color-text)]'"
      >
        <span>{{ item.icon }}</span>
        <span>{{ item.label }}</span>
      </router-link>
    </nav>

    <div class="p-3 border-t border-[var(--color-border)]">
      <div class="text-xs text-[var(--color-text-muted)]">
        未加载存档
      </div>
    </div>
  </aside>
</template>