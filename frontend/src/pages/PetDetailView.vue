<template>
  <div v-if="loading" class="text-center">Loading...</div>
  <div v-else-if="pet" class="space-y-6">
    <div class="bg-white p-6 rounded-lg shadow">
      <h1 class="text-3xl font-bold">{{ pet.name }}</h1>
      <p class="text-gray-600">{{ pet.species }}</p>
    </div>

    <div class="flex justify-between items-center">
      <h2 class="text-xl font-semibold">Insurance Policies</h2>
      <router-link :to="'/insurance/create?petId=' + pet.id" class="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700">
        Add Policy
      </router-link>
    </div>

    <div v-if="policies.length === 0" class="bg-white p-8 text-center rounded-lg shadow">
      No insurance policies found for this pet.
    </div>
    <div v-else class="space-y-4">
      <div v-for="policy in policies" :key="policy.id" class="bg-white p-4 rounded-lg shadow flex justify-between">
        <div>
          <h3 class="font-medium">Policy #: {{ policy.policy_number }}</h3>
          <p class="text-sm text-gray-600">{{ policy.coverage_details }}</p>
        </div>
        <div class="text-right">
          <span :class="policy.is_active ? 'text-green-600' : 'text-red-600'">
            {{ policy.is_active ? 'Active' : 'Inactive' }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { petService } from '../services/petService';
import { insuranceService } from '../services/insuranceService';
import type { Pet, InsurancePolicy } from '../types';

const route = useRoute();
const pet = ref<Pet | null>(null);
const policies = ref<InsurancePolicy[]>([]);
const loading = ref(true);

async function loadData() {
  const id = route.params.id as string;
  loading.value = true;
  try {
    const [petData, allPolicies] = await Promise.all([
      petService.getById(id),
      insuranceService.getAll()
    ]);
    pet.value = petData;
    // Client-side filtering as per policy that users can only see their own pet's policies
    policies.value = allPolicies.filter(p => p.pet_id.toString() === id);
  } finally {
    loading.value = false;
  }
}

onMounted(loadData);
</script>
