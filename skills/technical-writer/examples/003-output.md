# Architectural Decision Record (ADR)

## Webhook Handler Integration

- **Context:** Payments integration needed robust state updates.
- **Decision:** Integrated the Stripe SDK Webhook handler directly.
- **Impact:** Real-time billing events are now captured securely.