<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-xl font-semibold">Claims Submitted</h2>
    </div>

    <div v-if="claims.length === 0" class="bg-white p-8 text-center rounded-lg shadow">
      No claims submmited yet.
    </div>
    <div v-else class="space-y-4">
      <div v-for="claim in claims" :key="claim.id" class="bg-white p-4 rounded-lg shadow flex justify-between">
        <div>
          <h3 class="font-medium">Claim #: {{ claim.id }}</h3>
          <p class="text-sm text-gray-600"><strong>Pet:</strong> {{ claim.invoice_date }}</p>
          <p class="text-sm text-gray-600"><strong>Date of event:</strong> {{ formatDate(claim.date_of_event) }}</p>
          <p class="text-sm text-gray-600"><strong>Invoice date:</strong> {{ formatDate(claim.invoice_date) }}</p>
          <p class="text-sm text-gray-600"><strong>Amount:</strong> {{ claim.amount }}</p>
          <p class="text-sm text-gray-600"><strong>Review Note:</strong> {{ claim.review_notes }}</p>
        </div>
        <div class="text-right">
          <span class="text-orange-600">
            {{ claim.status}}
          </span>
        </div>
      </div>
    </div>
  </div>

  <div class="max-w-2xl mx-auto mt-4 bg-white p-8 rounded-lg shadow">
    <h1 class="text-2xl font-bold mb-6">Submit Reimbursement Claim</h1>
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700">Select Pet</label>
        <select v-model="form.pet_id" @change="handlePetChange" required class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2">
          <option v-for="pet in pets" :key="pet.id" :value="pet.id">{{ pet.name }}</option>
        </select>
      </div>

      <div v-if="filteredPolicies.length > 0">
        <label class="block text-sm font-medium text-gray-700">Select Insurance Policy</label>
        <select v-model="form.insurance_id" required class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2">
          <option v-for="policy in filteredPolicies" :key="policy.id" :value="policy.id">{{ policy.id }}</option>
        </select>
      </div>
      <div v-else-if="form.pet_id" class="text-red-500 text-sm">
        No active insurance found for this pet.
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Amount</label>
        <input v-model.number="form.amount" type="number" step="0.01" required class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Date of event</label>
        <input type="date" v-model="form.date_of_event" required class="w-full border p-2 rounded mt-1" />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Invocie Date</label>
        <input type="date" v-model="form.invoice_date" required class="w-full border p-2 rounded mt-1" />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Invoice File (PDF/Image)</label>
        <input type="file" @change="handleFileChange" required class="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100" />
      </div>

      <div class="flex justify-end space-x-2">
        <button type="button" @click="router.back()" class="bg-gray-200 px-4 py-2 rounded text-sm">Cancel</button>
        <button type="submit" :disabled="loading || !form.pet_id || filteredPolicies.length === 0" class="bg-blue-600 text-white px-4 py-2 rounded text-sm hover:bg-blue-700 disabled:bg-gray-400">
          {{ loading ? 'Submitting...' : 'Submit Claim' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { petService } from '../services/petService';
import { insuranceService } from '../services/insuranceService';
import { claimService } from '../services/claimService';
import { useNotificationStore } from '../store/notification';
import type { Pet, InsurancePolicy, Claim } from '../types';
import { formatDate } from '../utils/date';

const router = useRouter();
const notificationStore = useNotificationStore();

const pets = ref<Pet[]>([]);
const allPolicies = ref<InsurancePolicy[]>([]);
const loading = ref(false);
const selectedFile = ref<File | null>(null);
const claims = ref<Claim[]>([]);

const form = ref({
  pet_id: '',
  insurance_id: '',
  amount: 0,
  date_of_event: '',
  invoice_date: '',
});

const filteredPolicies = computed(() => {
  return allPolicies.value.filter(p => p.pet.toString() === form.value.pet_id.toString() && p.status === 'ACTIVE');
});

async function loadData() {
  try {
    const [petsData, policiesData, claimsData] = await Promise.all([
      petService.getAll(),
      insuranceService.getAll(),
      claimService.getAll(),
    ]);
    pets.value = petsData;
    allPolicies.value = policiesData;
    claims.value = claimsData;
  } catch (err) {
    notificationStore.add('Failed to load required data', 'error');
  }
}

function handlePetChange() {
  form.value.insurance_id = '';
}

function handleFileChange(event: Event) {
  const input = event.target as HTMLInputElement;
  const file = input.files?.[0];

  if (file && file.size > 1024 * 1024) {
    notificationStore.add('The file is too large (maximum 1MB).', 'error');
    input.value = '';
    selectedFile.value = null;
    return;
  }

  if (file) {
    selectedFile.value = file;
  }
}

async function handleSubmit() {
  if (!selectedFile.value) {
    notificationStore.add('Please select an invoice file', 'error');
    return;
  }

  loading.value = true;
  const formData = new FormData();
  formData.append('insurance', form.value.insurance_id);
  formData.append('invoice', selectedFile.value);
  formData.append('invoice_date', form.value.invoice_date);
  formData.append('amount', form.value.amount.toString());
  formData.append('date_of_event', form.value.date_of_event);
  
  try {
    await claimService.create(formData);
    notificationStore.add('Claim submitted successfully!', 'success');
    router.push('/pets');
  } catch (err) {
    notificationStore.add('Failed to submit claim', 'error');
  } finally {
    loading.value = false;
  }
}

onMounted(loadData);
</script>
