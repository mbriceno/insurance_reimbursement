<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold">My Pets</h1>
      <button @click="showAddModal = true" class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
        Add Pet
      </button>
    </div>

    <div v-if="loading" class="text-center">Loading...</div>
    <div v-else-if="pets.length === 0" class="bg-white p-8 text-center rounded-lg shadow">
      No pets found. Add your first pet!
    </div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="pet in pets" :key="pet.id" class="bg-white p-6 rounded-lg shadow">
        <h3 class="text-xl font-semibold">{{ pet.name }}</h3>
        <p class="text-gray-600">{{ pet.species }}</p>
        <div class="mt-4 flex space-x-2">
          <router-link :to="'/pets/' + pet.id" class="text-blue-600 hover:underline">Details</router-link>
          <router-link :to="'/insurance/create?petId=' + pet.id" class="text-green-600 hover:underline">Add Insurance</router-link>
        </div>
      </div>
    </div>

    <!-- Add Pet Modal Placeholder -->
    <div v-if="showAddModal" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4">
       <div class="bg-white p-6 rounded-lg w-full max-w-md">
         <h2 class="text-xl font-bold mb-4">Add New Pet</h2>
         <form @submit.prevent="handleAddPet">
            <div class="mb-4">
              <label class="block text-sm font-medium">Name</label>
              <input v-model="newPet.name" required class="w-full border p-2 rounded mt-1" />
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium">Species</label>
              <select v-model="newPet.species" required class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2">
                <option v-for="spicies in speciesList" :key="spicies.value" :value="spicies.value">{{ spicies.label }}</option>
              </select>
            </div>
            <div class="mb-4">
              <label class="block text-sm font-medium">Name</label>
              <input type="date" v-model="newPet.birth_date" required class="w-full border p-2 rounded mt-1" />
            </div>
            <div class="flex justify-end space-x-2">
              <button type="button" @click="showAddModal = false" class="bg-gray-200 px-4 py-2 rounded">Cancel</button>
              <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">Save</button>
            </div>
         </form>
       </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { petService } from '../services/petService';
import { useNotificationStore } from '../store/notification';
import type { Pet } from '../types';
import { SpeciesOptions } from '../types';

const pets = ref<Pet[]>([]);
const speciesList = Object.values(SpeciesOptions).map(value => ({
  label: value.charAt(0) + value.slice(1).toLowerCase(), // Formateo: "Dog", "Cat"
  value: value
}));
const loading = ref(true);
const showAddModal = ref(false);
const newPet = ref({ name: '', species: ref<typeof SpeciesOptions | ''>(''), birth_date: ''});
const notificationStore = useNotificationStore();


async function loadPets() {
  loading.value = true;
  try {
    pets.value = await petService.getAll();
  } finally {
    loading.value = false;
  }
}

async function handleAddPet() {
  try {
    await petService.create(newPet.value);
    notificationStore.add('Pet added successfully!', 'success');
    showAddModal.value = false;
    newPet.value = { name: '', species: ref<typeof SpeciesOptions | ''>(''), birth_date: ''};
    loadPets();
  } catch (err) {
    notificationStore.add('Failed to add pet', 'error');
  }
}

onMounted(loadPets);
</script>
