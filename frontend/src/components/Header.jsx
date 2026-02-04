import React from 'react';
import { ConnectButton } from '@rainbow-me/rainbowkit';

export function Header() {
  return (
    <header className="header">
      <div className="logo">
        <h1>🌙 Nanba Payment Gateway</h1>
      </div>
      <nav>
        <a href="/">Home</a>
        <a href="/payments">Payments</a>
        <a href="/dashboard">Dashboard</a>
      </nav>
      <ConnectButton />
    </header>
  );
}
