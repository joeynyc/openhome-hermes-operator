# Security Policy

## Supported versions

This project is pre-1.0. Security fixes land on `main`.

## Reporting a vulnerability

Please do not open a public issue for security-sensitive reports.

Email: joeyr1983@gmail.com

Include:

- affected component
- reproduction steps
- impact
- suggested fix, if known

## Local deployment notes

The bridge is designed for trusted local networks. If exposed beyond localhost, set `HERMES_OPERATOR_TOKEN` and put it behind your normal LAN/VPN protections.

Never expose the Hermes API Server directly to the public internet.
