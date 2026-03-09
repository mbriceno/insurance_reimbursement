<template>
  <div class="max-w-2xl mx-auto bg-white p-8 rounded-lg shadow">
    <h1 class="text-2xl font-bold mb-6">Create Insurance Policy</h1>
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700">Select Pet</label>
        <select v-model="form.pet_id" required class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2">
          <option v-for="pet in pets" :key="pet.id" :value="pet.id">{{ pet.name }} ({{ pet.species }})</option>
        </select>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Policy Number</label>
        <input v-model="form.policy_number" required class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Coverage Details</label>
        <textarea v-model="form.coverage_details" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" rows="3"></textarea>
      </div>

      <div class="flex items-center">
        <input v-model="form.is_active" type="checkbox" class="h-4 w-4 text-blue-600 rounded" />
        <label class="ml-2 block text-sm text-gray-900 font-medium">Policy is Active</label>
      </div>

      <div class="flex justify-end space-x-2">
        <button type="button" @click="router.back()" class="bg-gray-200 px-4 py-2 rounded text-sm">Cancel</button>
        <button type="submit" :disabled="loading" class="bg-blue-600 text-white px-4 py-2 rounded text-sm hover:bg-blue-700">
          {{ loading ? 'Creating...' : 'Create Policy' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { petService } from '../services/petService';
import { insuranceService } from '../services/insuranceService';
import { useNotificationStore } from '../store/notification';
import type { Pet } from '../types';

const route = useRoute();
const router = useRouter();
const notificationStore = useNotificationStore();

const pets = ref<Pet[]>([]);
const loading = ref(false);

const form = ref({
  pet_id: route.query.petId?.toString() || '',
  policy_number: '',
  coverage_details: '',
  is_active: true,
});

async function loadPets() {
  try {
    pets.value = await petService.getAll();
    if (pets.value.length === 0) {
      notificationStore.add('You need to add a pet before creating a policy.', 'warning');
      router.push('/pets');
    }
  } catch (err) {
    notificationStore.add('Failed to load pets', 'error');
  }
}

async function handleSubmit() {
  loading.value = true;
  try {
    await insuranceService.create(form.value);
    notificationStore.add('Policy created successfully!', 'success');
    router.push('/pets/' + form.value.pet_id);
  } catch (err) {
    notificationStore.add('Failed to create policy', 'error');
  } finally {
    loading.value = false;
  }
}

onMounted(loadPets);
</script>
