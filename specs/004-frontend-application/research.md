# Research: Frontend Application Implementation

## 1. API Choice: Options API vs. Composition API
- **Decision**: Follow the **Constitution** and use **Composition API** with `<script setup>`.
- **Rationale**: The Constitution (v1.0.0) MANDATES the use of Vue.js 3 (Composition API) with `<script setup>`. While the user's initial prompt mentioned Options API, maintaining project-wide consistency and adhering to the governance document takes precedence.
- **Alternatives considered**: Using Options API as requested (rejected for violating the Constitution).

## 2. Testing Framework
- **Decision**: Use **Vitest** for unit/component testing and **Playwright** for E2E testing.
- **Rationale**: Vitest is the native choice for Vite-based projects, offering high performance and a Jest-compatible API. Playwright provides a modern and robust environment for browser-based testing.
- **Alternatives considered**: Jest (rejected due to slower performance with Vite), Cypress (rejected in favor of Playwright for better multi-browser support and speed).

## 3. JWT Refresh Strategy
- **Decision**: Implement an **Axios Interceptor** that detects 401 Unauthorized errors and attempts a token refresh via `/api/token/refresh/`.
- **Rationale**: This is the industry standard for maintaining user sessions securely and transparently. The `authStore` (Pinia) will hold the access and refresh tokens. If the refresh fails, the user is redirected to the login page.
- **Alternatives considered**: Manual refresh (too error-prone), using a dedicated auth library like Auth0 (rejected as we are using a custom DRF backend).

## 4. UI Framework Integration
- **Decision**: Use **Tailwind CSS** as a PostCSS plugin via Vite.
- **Rationale**: Mandated by the Constitution and highly efficient for building custom, responsive UIs quickly.
- **Alternatives considered**: Component libraries like Vuetify or Element Plus (rejected to maintain minimal bundle size and design flexibility).

## 5. File Upload Handling
- **Decision**: Use `multipart/form-data` with Axios `FormData` object for claim submissions.
- **Rationale**: Required for transmitting binary files (invoices) along with structured JSON-like data.
- **Alternatives considered**: Base64 encoding (rejected for performance and overhead reasons).
