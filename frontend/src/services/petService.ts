import { apiAuth } from './api';
import type { Pet } from '../types';

export const petService = {
  async getAll() {
    const response = await apiAuth.get<Pet[]>('/api/pets/');
    return response.data;
  },
  async getById(id: number | string) {
    const response = await apiAuth.get<Pet>(`/api/pets/${id}/`);
    return response.data;
  },
  async create(petData: Partial<Pet>) {
    const response = await apiAuth.post<Pet>('/api/pets/', petData);
    return response.data;
  },
};
