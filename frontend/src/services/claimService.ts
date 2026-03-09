import { apiAuth } from './api';
import type { Claim } from '../types';

export const claimService = {
  async getAll() {
    const response = await apiAuth.get<Claim[]>('/api/claims/');
    return response.data;
  },
  async getById(id: number | string) {
    const response = await apiAuth.get<Claim>(`/api/claims/${id}/`);
    return response.data;
  },
  async create(claimData: FormData) {
    // Note: Use FormData for multipart/form-data
    const response = await apiAuth.post<Claim>('/api/claims/', claimData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};
