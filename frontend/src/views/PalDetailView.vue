<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const pal = ref<any>(null)
const loading = ref(true)
const saving = ref(false)
const savePath = ref(localStorage.getItem('savePath') || '')

onMounted(async () => {
  const id = route.params.id as string
  try {
    const res = await fetch(`/api/pal/${id}?save_path=${encodeURIComponent(savePath.value)}`)
    const data = await res.json()
    if (data.success) pal.value = data.pal
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})

function goBack() {
  router.push('/pals')
}

async function save() {
  if (!pal.value) return
  saving.value = true
  try {
    const fields: any = {
      level: Number(pal.value.level),
      exp: Number(pal.value.exp),
      nickname: pal.value.nickname,
      gender: pal.value.gender,
      hp: Number(pal.value.hp),
      max_hp: Number(pal.value.max_hp),
      stomach: Number(pal.value.stomach),
      sanity: Number(pal.value.sanity),
      star_rank: Number(pal.value.star_rank),
      talent_hp: Number(pal.value.talent_hp),
      talent_attack: Number(pal.value.talent_attack),
      talent_defense: Number(pal.value.talent_defense),
      soul_hp: Number(pal.value.soul_hp),
      soul_attack: Number(pal.value.soul_attack),
      soul_defense: Number(pal.value.soul_defense),
      soul_craftspeed: Number(pal.value.soul_craftspeed),
      active_skills: pal.value.active_skills || [],
      passive_skills: pal.value.passive_skills || [],
      friendship: Number(pal.value.friendship),
    }
    const res = await fetch(`/api/pal/${pal.value.instance_id}/update?save_path=${encodeURIComponent(savePath.value)}&instance_id=${pal.value.instance_id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ fields }),
    })
    const data = await res.json()
    if (data.success) {
      alert('保存成功！')
    } else {
      alert('保存失败: ' + data.error)
    }
  } catch (e: any) {
    alert('保存失败: ' + e.message)
  } finally {
    saving.value = false
  }
}

function getWorkIcon(name: string): string {
  const icons: Record<string, string> = {
    'EmitFlame': '🔥', 'Watering': '💧', 'Seeding': '🌱',
    'GenerateElectricity': '⚡', 'Handcraft': '🛠️', 'Collection': '🌾',
    'Deforest': '🪓', 'Mining': '⛏️', 'OilExtraction': '🛢️',
    'Cool': '❄️', 'Transport': '📦', 'MonsterFarm': '🐄',
  }
  return icons[name] || '📌'
}
</script>

<template>
  <div v-if="loading" class="text-center mt-20" style="color: var(--color-text-muted)">加载中...</div>

  <div v-else-if="pal">
    <!-- 顶部 -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center gap-3">
        <button class="text-sm" style="color: var(--color-accent)" @click="goBack">← 返回</button>
        <h2 class="text-xl font-bold">🐾 {{ pal.nickname || pal.character_id }}</h2>
      </div>
      <button
        class="px-5 py-2 text-black font-semibold rounded-lg"
        style="background: var(--color-primary)"
        :disabled="saving"
        @click="save"
      >
        {{ saving ? '保存中...' : '💾 保存' }}
      </button>
    </div>

    <div class="grid" style="grid-template-columns: 1fr 1fr; gap: 16px">
      <!-- 基础信息 -->
      <section class="rounded-xl p-4" style="background: var(--color-bg-surface)">
        <h3 class="text-sm font-semibold mb-3" style="color: var(--color-text-muted)">基础信息</h3>
        <div class="grid" style="grid-template-columns: 1fr 1fr 1fr; gap: 12px">
          <label class="text-xs" style="color: var(--color-text-muted)">
            等级
            <input v-model.number="pal.level" type="number" min="1" max="80" class="block w-full mt-1" />
          </label>
          <label class="text-xs" style="color: var(--color-text-muted)">
            性别
            <select v-model="pal.gender" class="block w-full mt-1">
              <option value="Male">♂ Male</option>
              <option value="Female">♀ Female</option>
            </select>
          </label>
          <label class="text-xs" style="color: var(--color-text-muted)">
            星级
            <input v-model.number="pal.star_rank" type="number" min="0" max="4" class="block w-full mt-1" />
          </label>
          <label class="text-xs" style="color: var(--color-text-muted)">
            HP
            <input v-model.number="pal.hp" type="number" min="0" class="block w-full mt-1" />
          </label>
          <label class="text-xs" style="color: var(--color-text-muted)">
            最大HP
            <input v-model.number="pal.max_hp" type="number" min="0" class="block w-full mt-1" />
          </label>
          <label class="text-xs" style="color: var(--color-text-muted)">
            经验
            <input v-model.number="pal.exp" type="number" min="0" class="block w-full mt-1" />
          </label>
          <label class="text-xs" style="color: var(--color-text-muted)">
            饱腹
            <input v-model.number="pal.stomach" type="number" step="0.1" class="block w-full mt-1" />
          </label>
          <label class="text-xs" style="color: var(--color-text-muted)">
            SAN
            <input v-model.number="pal.sanity" type="number" step="0.1" class="block w-full mt-1" />
          </label>
          <label class="text-xs" style="color: var(--color-text-muted)">
            亲密度
            <input v-model.number="pal.friendship" type="number" min="0" max="255" class="block w-full mt-1" />
          </label>
        </div>
      </section>

      <!-- 天赋 & 魂强化 -->
      <section class="rounded-xl p-4" style="background: var(--color-bg-surface)">
        <h3 class="text-sm font-semibold mb-3" style="color: var(--color-text-muted)">天赋 & 魂强化</h3>
        <div class="grid" style="grid-template-columns: 1fr 1fr 1fr 1fr; gap: 10px">
          <div class="text-center">
            <div class="text-xs" style="color: var(--color-text-muted)">HP</div>
            <input v-model.number="pal.talent_hp" type="number" min="0" max="255" class="w-full text-center mt-1" />
            <div class="text-xs mt-1" style="color: var(--color-accent)">魂 <input v-model.number="pal.soul_hp" type="number" min="0" max="255" class="w-12 text-center" /></div>
          </div>
          <div class="text-center">
            <div class="text-xs" style="color: var(--color-text-muted)">攻击</div>
            <input v-model.number="pal.talent_attack" type="number" min="0" max="255" class="w-full text-center mt-1" />
            <div class="text-xs mt-1" style="color: var(--color-accent)">魂 <input v-model.number="pal.soul_attack" type="number" min="0" max="255" class="w-12 text-center" /></div>
          </div>
          <div class="text-center">
            <div class="text-xs" style="color: var(--color-text-muted)">防御</div>
            <input v-model.number="pal.talent_defense" type="number" min="0" max="255" class="w-full text-center mt-1" />
            <div class="text-xs mt-1" style="color: var(--color-accent)">魂 <input v-model.number="pal.soul_defense" type="number" min="0" max="255" class="w-12 text-center" /></div>
          </div>
          <div class="text-center">
            <div class="text-xs" style="color: var(--color-text-muted)">手工</div>
            <div class="mt-1" style="color: var(--color-text-muted)">—</div>
            <div class="text-xs mt-1" style="color: var(--color-accent)">魂 <input v-model.number="pal.soul_craftspeed" type="number" min="0" max="255" class="w-12 text-center" /></div>
          </div>
        </div>
      </section>

      <!-- 主动技能 -->
      <section class="rounded-xl p-4" style="background: var(--color-bg-surface)">
        <h3 class="text-sm font-semibold mb-3" style="color: var(--color-text-muted)">主动技能</h3>
        <div class="flex flex-wrap gap-2 mb-2">
          <span
            v-for="(skill, i) in pal.active_skills"
            :key="i"
            class="px-2 py-1 rounded-full text-xs flex items-center gap-1"
            style="background: rgba(74,222,128,0.15); color: var(--color-primary)"
          >
            <input v-model="pal.active_skills[i]" class="w-24 text-center text-xs" style="background: transparent; border: none; padding: 0; color: inherit" />
            <button class="text-xs cursor-pointer" style="color: var(--color-danger)" @click="pal.active_skills.splice(i, 1)">×</button>
          </span>
          <button
            class="px-2 py-1 rounded-full text-xs cursor-pointer"
            style="background: rgba(74,222,128,0.1); color: var(--color-primary)"
            @click="pal.active_skills.push('')"
          >+ 添加</button>
        </div>
      </section>

      <!-- 被动技能 -->
      <section class="rounded-xl p-4" style="background: var(--color-bg-surface)">
        <h3 class="text-sm font-semibold mb-3" style="color: var(--color-text-muted)">被动技能</h3>
        <div class="flex flex-wrap gap-2 mb-2">
          <span
            v-for="(skill, i) in pal.passive_skills"
            :key="i"
            class="px-2 py-1 rounded-full text-xs flex items-center gap-1"
            style="background: rgba(245,158,11,0.15); color: var(--color-warm)"
          >
            <input v-model="pal.passive_skills[i]" class="w-24 text-center text-xs" style="background: transparent; border: none; padding: 0; color: inherit" />
            <button class="text-xs cursor-pointer" style="color: var(--color-danger)" @click="pal.passive_skills.splice(i, 1)">×</button>
          </span>
          <button
            class="px-2 py-1 rounded-full text-xs cursor-pointer"
            style="background: rgba(245,158,11,0.1); color: var(--color-warm)"
            @click="pal.passive_skills.push('')"
          >+ 添加</button>
        </div>
      </section>

      <!-- 工作适应 -->
      <section class="rounded-xl p-4" style="background: var(--color-bg-surface); grid-column: 1 / -1">
        <h3 class="text-sm font-semibold mb-3" style="color: var(--color-text-muted)">工作适应</h3>
        <div class="flex flex-wrap gap-4">
          <div v-for="(level, name) in pal.work_suitability" :key="name" class="text-center">
            <div class="text-lg">{{ getWorkIcon(name) }}</div>
            <div class="text-xs" style="color: var(--color-text-muted)">{{ name }}</div>
            <div class="text-sm font-semibold" style="color: var(--color-accent)">Lv.{{ level }}</div>
          </div>
          <span v-if="!Object.keys(pal.work_suitability || {}).length" class="text-xs" style="color: var(--color-text-muted)">无</span>
        </div>
      </section>
    </div>
  </div>

  <div v-else class="text-center mt-20" style="color: var(--color-danger)">帕鲁不存在</div>
</template>