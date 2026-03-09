export type Role = 'CUSTOMER' | 'ADMIN' | 'SUPPORT';
export type ClaimStatus = 'PENDING' | 'APPROVED' | 'REJECTED';

export interface User {
  id: string;
  username: string;
  email: string;
  role: Role;
}

export interface Pet {
  id: number | string;
  name: string;
  species: string;
  owner_id: number | string;
}

export interface InsurancePolicy {
  id: number | string;
  pet: number | string;
  status: string;
  coverage_start: string;
  coverage_end: string;
  owner: number | string;
}

export interface Claim {
  id: number | string;
  pet_id: number | string;
  insurance_id: number | string;
  amount: number;
  description: string;
  invoice_file: string; // URL to the file
  status: ClaimStatus;
  date_of_event: string;
}

export const SpeciesOptions = {
  DOG: 'DOG',
  CAT: 'CAT',
  OTHER: 'OTHER',
} as const;