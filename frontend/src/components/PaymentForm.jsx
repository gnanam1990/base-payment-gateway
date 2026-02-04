import React from 'react';

export function PaymentForm({ onSubmit }) {
  const [amount, setAmount] = React.useState('');
  const [merchant, setMerchant] = React.useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ amount, merchant });
  };
  
  return (
    <form onSubmit={handleSubmit} className="payment-form">
      <h3>Create Payment</h3>
      <input
        type="text"
        placeholder="Merchant Address"
        value={merchant}
        onChange={(e) => setMerchant(e.target.value)}
      />
      <input
        type="number"
        placeholder="Amount (ETH)"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
      />
      <button type="submit">Pay Now</button>
    </form>
  );
}
