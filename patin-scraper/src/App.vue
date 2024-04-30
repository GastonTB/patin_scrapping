<template>
  <div>
    <!-- Overlay de carga -->
    <div
      v-if="loading"
      class="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50 z-50"
    >
      <div>
        <svg class="animate-spin h-5 w-5 mr-3 ..." viewBox="0 0 24 24">
          <!-- ... -->
        </svg>
        Cargando...
      </div>
    </div>

    <!-- Contenido principal -->
    <div class="py-3 bg-gradient-to-r from-black via-gray-700 to-gray-500 text-white">
      <p class="ml-3 font-bold">Lista de Precios de Patines Chile</p>
    </div>
    <div class="grid grid-cols-5 h-screen">
      <div class="col-span-1 bg-red-500"></div>
      <div class="col-span-4 bg-blue-500">
        <div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-6">
          <div
            v-for="item in apiData"
            :key="item.name"
            class="rounded-lg shadow bg-gray-800 border-gray-700"
          >
            <a :href="item.link">
              <img class="rounded-t-lg h-40 w-full object-cover" :src="item.image" alt="" />
            </a>
            <div class="p-5">
              <a :href="item.link">
                <h5 class="mb-2 text-xl font-bold tracking-tight text-white">{{ item.name }}</h5>
              </a>
              <p class="mb-3 font-normal text-gray-400">
                {{ item.description }}
              </p>
              <a
                :href="item.link"
                class="inline-block px-3 py-2 text-sm text-center text-white rounded-lg focus:ring-4 focus:outline-none bg-blue-600 hover:bg-blue-700 focus:ring-blue-800 font-bold uppercase"
              >
                Ir a la tienda
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const loading = ref(true)
const apiData = ref<any[]>([])

const fetchData = async () => {
  try {
    loading.value = true // Mostrar mensaje de carga
    const response = await axios.get<any[]>('http://localhost:8000/patines_agresivos_data')
    apiData.value = response.data
    console.log('Datos de la API:', apiData.value) // Agregado para depuración
  } catch (error) {
    console.error('Error al obtener los datos de la API:', error)
  } finally {
    loading.value = false // Ocultar mensaje de carga
  }
}

fetchData()
</script>

<style scoped>
/* Estilos opcionales */
</style>
