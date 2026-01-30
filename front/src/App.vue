<script setup>
import { Toaster } from 'vue-sonner'
import TransportForm from './components/TransportForm.vue'
</script>

<template>
  <Toaster position="top-right" richColors theme="light" />
  <div class="min-h-screen bg-gray-100 py-12">
    <header class="max-w-4xl mx-auto mb-8 px-6">
      <div class="flex items-center space-x-4">
        <img alt="Logo" src="./assets/logo.svg" class="w-12 h-12" />
        <h1 class="text-3xl font-extrabold text-gray-900">Transport Manager</h1>
      </div>
      <p class="mt-2 text-gray-600">Gérez vos demandes de transport de marchandises en toute simplicité.</p>
    </header>

    <main>
      <TransportForm />
    </main>
    
    <footer class="max-w-4xl mx-auto mt-12 px-6 text-center text-gray-500 text-sm">
      &copy; 2026 Transport API Example. Tous droits réservés.
    </footer>
  </div>
</template>

<style>
/* Suppression des styles par défaut qui pourraient entrer en conflit avec Tailwind */
body {
  margin: 0;
  padding: 0;
}
#app {
  max-width: none;
  margin: 0;
  padding: 0;
  display: block;
}
</style>
