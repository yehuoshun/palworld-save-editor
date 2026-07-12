<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const pal = ref<any>(null)
const loading = ref(true)
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