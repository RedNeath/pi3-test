<script setup>
import { ref, watch } from 'vue'
import { toast } from 'vue-sonner'

const props = defineProps({
  label: String,
  modelValue: Object,
  placeholder: String
})

const emit = defineEmits(['update:modelValue'])

const query = ref('')
const results = ref([])
const isOpen = ref(false)
const isLoading = ref(false)

let debounceTimer = null

const searchPlaces = async () => {
  if (query.value.length < 2) {
    results.value = []
    return
  }

  isLoading.value = true
  try {
    const response = await fetch(`http://localhost:3000/v1/places?cityName=${encodeURIComponent(query.value)}&limit=5`)
    if (response.ok) {
      results.value = await response.json()
    } else {
      const errorData = await response.json()
      console.error('Erreur API recherche lieux:', errorData)
    }
  } catch (error) {
    toast.error('Erreur lors de la recherche de lieux')
    console.error('Erreur lors de la recherche de lieux:', error)
  } finally {
    isLoading.value = false
  }
}

watch(query, (newQuery) => {
  clearTimeout(debounceTimer)
  if (newQuery && !props.modelValue || (props.modelValue && newQuery !== props.modelValue.city)) {
    debounceTimer = setTimeout(() => {
      searchPlaces()
      isOpen.value = true
    }, 300)
  }
})

const selectPlace = (place) => {
  query.value = place.city
  emit('update:modelValue', place)
  isOpen.value = false
}

// Initialiser si modelValue est présent
if (props.modelValue) {
  query.value = props.modelValue.city
}
</script>

<template>
  <div class="relative">
    <label class="block text-sm font-medium text-gray-700 mb-1">{{ label }}</label>
    <input
      v-model="query"
      type="text"
      :placeholder="placeholder"
      class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
      @focus="isOpen = query.length >= 2"
    />
    
    <div v-if="isOpen && results.length > 0" class="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto">
      <ul>
        <li
          v-for="place in results"
          :key="place.id"
          class="px-4 py-2 hover:bg-gray-100 cursor-pointer"
          @click="selectPlace(place)"
        >
          <div class="font-medium">{{ place.city }}</div>
          <div class="text-xs text-gray-500">{{ place.street }}, {{ place.nation }}</div>
        </li>
      </ul>
    </div>
    <div v-else-if="isOpen && query.length >= 2 && !isLoading" class="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg p-4 text-sm text-gray-500">
      Aucun résultat trouvé
    </div>
  </div>
</template>
