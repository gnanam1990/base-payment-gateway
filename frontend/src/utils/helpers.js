import { ethers } from 'ethers';

export function formatAddress(address) {
  if (!address) return '';
  return `${address.slice(0, 6)}...${address.slice(-4)}`;
}

export function formatAmount(amount, decimals = 18) {
  return ethers.formatUnits(amount, decimals);
}

export function parseAmount(amount, decimals = 18) {
  return ethers.parseUnits(amount.toString(), decimals);
}

export function formatUSD(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(amount);
}

export function shortenText(text, maxLength = 50) {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
}
