# User Authentication Documentation
**Author:** Colby Wirth
**Version:** December 8, 2025

## JWT Secret and Token Generation

GrantGuru uses **JWT-based authentication** to manage user sessions in a secure manner. The process works as follows:

### 1. JWT Secret Key
- The server maintains a **single, secure, 32-byte hexadecimal JWT secret key**.
- This secret key is stored in the server’s `.env` file and is used to **sign all JWT tokens**.
- The secret ensures that tokens **cannot be forged or tampered with**, and allows the server to verify authenticity without storing tokens in the database.

### 2. Token Generation
- When a user logs in successfully, the server generates a **JWT token** that encodes the user’s **UUID**.
- The token is **signed using the JWT secret key**, which guarantees its integrity.
- The signed token is returned to the client and is stored in **session storage**.

### 3. Token Verification
- For subsequent requests, the client includes the JWT in the `Authorization: Bearer <token>` header.
- The server verifies the token’s **signature** using the same JWT secret key.
- Once verified, the server extracts the **UUID** from the token payload to identify the user and authorize access **only to their own data**.
