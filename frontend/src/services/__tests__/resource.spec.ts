import { describe, it, expect, vi, beforeEach } from 'vitest';
import { petService } from '../petService';
import { insuranceService } from '../insuranceService';
import { apiAuth } from '../api';

vi.mock('../api', () => ({
  apiAuth: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('Resource Services', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('Pet Service', () => {
    it('fetches all pets', async () => {
      const mockPets = [{ id: 1, name: 'Fido' }];
      (apiAuth.get as any).mockResolvedValueOnce({ data: mockPets });

      const result = await petService.getAll();

      expect(apiAuth.get).toHaveBeenCalledWith('/api/pets/');
      expect(result).toEqual(mockPets);
    });

    it('creates a pet', async () => {
      const petData = { name: 'Fido', species: 'Dog' };
      (apiAuth.post as any).mockResolvedValueOnce({ data: { id: 1, ...petData } });

      const result = await petService.create(petData);

      expect(apiAuth.post).toHaveBeenCalledWith('/api/pets/', petData);
      expect(result.id).toBe(1);
    });
  });

  describe('Insurance Service', () => {
    it('creates a policy', async () => {
      const policyData = { pet_id: 1, policy_number: 'POL-123' };
      (apiAuth.post as any).mockResolvedValueOnce({ data: { id: 10, ...policyData } });

      const result = await insuranceService.create(policyData);

      expect(apiAuth.post).toHaveBeenCalledWith('/api/insurance/', policyData);
      expect(result.id).toBe(10);
    });
  });
});
