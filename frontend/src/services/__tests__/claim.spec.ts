import { describe, it, expect, vi, beforeEach } from 'vitest';
import { claimService } from '../claimService';
import { apiAuth } from '../api';

vi.mock('../api', () => ({
  apiAuth: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('Claim Service', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('submits a claim with FormData', async () => {
    const formData = new FormData();
    formData.append('pet', '1');
    (apiAuth.post as any).mockResolvedValueOnce({ data: { id: 100 } });

    const result = await claimService.create(formData);

    expect(apiAuth.post).toHaveBeenCalledWith('/api/claims/', formData, expect.objectContaining({
      headers: { 'Content-Type': 'multipart/form-data' }
    }));
    expect(result.id).toBe(100);
  });
});
