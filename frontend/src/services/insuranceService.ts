import { apiAuth } from './api';
import type { InsurancePolicy } from '../types';

export const insuranceService = {
  async getAll() {
    const response = await apiAuth.get<InsurancePolicy[]>('/api/insurances/');
    return response.data;
  },
  async getById(id: number | string) {
    const response = await apiAuth.get<InsurancePolicy>(`/api/insurances/${id}/`);
    return response.data;
  },
  async create(policyData: Partial<InsurancePolicy>) {
    const response = await apiAuth.post<InsurancePolicy>('/api/insurances/', policyData);
    return response.data;
  },
};
