<script setup>
import { reactive, ref } from 'vue'
import { toast } from 'vue-sonner'
import PlaceSearch from './PlaceSearch.vue'

const loadTypes = ['PACKAGE', 'STANDARD', 'WIDE_LOAD', 'EMPTY']

const form = reactive({
  from: null,
  to: null,
  loadType: 'STANDARD',
  quantity: 1
})

const isSubmitting = ref(false)

const submitForm = async () => {
  if (!form.from || !form.to) {
    toast.error('Veuillez sélectionner un lieu de départ et d\'arrivée.')
    return
  }

  isSubmitting.value = true

  try {
    const response = await fetch('http://localhost:3000/v1/transport-requests', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        ...form,
        requestedAt: new Date().toISOString()
      })
    })

    if (response.ok) {
      const result = await response.json()
      toast.success(`Demande créée avec succès ! ID: ${result.id}`)
      // Reset form
      form.from = null
      form.to = null
      form.quantity = 1
      form.loadType = 'STANDARD'
    } else {
      const errorData = await response.json()
      const errorMsg = errorData.error || errorData.message || response.statusText
      toast.error(`Erreur lors de la création : ${errorMsg}`)
    }
  } catch (error) {
    toast.error('Erreur réseau ou serveur.')
    console.error(error)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="max-w-2xl mx-auto p-6 bg-white rounded-xl shadow-md">
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-800">Nouvelle Demande de Transport</h2>
      <div class="h-1 w-20 bg-gradient-to-r from-blue-600 to-blue-400 rounded-full mt-2"></div>
    </div>
    
    <form @submit.prevent="submitForm" class="space-y-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <PlaceSearch
          v-model="form.from"
          label="Départ"
          placeholder="Ville de départ..."
        />
        
        <PlaceSearch
          v-model="form.to"
          label="Arrivée"
          placeholder="Ville d'arrivée..."
        />
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Type de Chargement</label>
          <select
            v-model="form.loadType"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            <option v-for="type in loadTypes" :key="type" :value="type">{{ type }}</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Quantité</label>
          <input
            v-model.number="form.quantity"
            type="number"
            min="1"
            class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
      </div>


      <button
        type="submit"
        :disabled="isSubmitting"
        class="w-full bg-blue-600 text-white py-3 px-6 rounded-md font-semibold hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 transition-colors"
      >
        <span v-if="isSubmitting">Envoi en cours...</span>
        <span v-else>Créer la demande</span>
      </button>
    </form>
  </div>
</template>
