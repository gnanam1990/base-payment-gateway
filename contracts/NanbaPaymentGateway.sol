// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title NanbaPaymentGateway
 * @dev Payment gateway for Base ecosystem with multi-token support
 * @author Nanba for k Я Λ T 0 Ƨ
 */

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract NanbaPaymentGateway is ReentrancyGuard, Ownable {
    
    // Payment status enum
    enum PaymentStatus { 
        PENDING, 
        COMPLETED, 
        REFUNDED, 
        FAILED 
    }
    
    // Payment struct
    struct Payment {
        address payer;
        address merchant;
        uint256 amount;
        address token;
        string paymentId;
        string metadata;
        PaymentStatus status;
        uint256 timestamp;
    }
    
    // Supported tokens mapping
    mapping(address => bool) public supportedTokens;
    
    // Payments mapping
    mapping(bytes32 => Payment) public payments;
    
    // Merchant balances
    mapping(address => mapping(address => uint256)) public merchantBalances;
    
    // Platform fee (in basis points, e.g., 250 = 2.5%)
    uint256 public platformFee = 250;
    uint256 public constant FEE_DENOMINATOR = 10000;
    
    // Events
    event PaymentCreated(
        bytes32 indexed paymentHash,
        address indexed payer,
        address indexed merchant,
        uint256 amount,
        address token,
        string paymentId
    );
    
    event PaymentCompleted(
        bytes32 indexed paymentHash,
        uint256 merchantAmount,
        uint256 platformFee
    );
    
    event PaymentRefunded(
        bytes32 indexed paymentHash,
        uint256 refundAmount
    );
    
    event TokenAdded(address indexed token);
    event TokenRemoved(address indexed token);
    event FeeUpdated(uint256 newFee);
    event FundsWithdrawn(address indexed merchant, address token, uint256 amount);
    
    constructor() Ownable(msg.sender) {}
    
    /**
     * @dev Add supported token
     */
    function addSupportedToken(address _token) external onlyOwner {
        supportedTokens[_token] = true;
        emit TokenAdded(_token);
    }
    
    /**
     * @dev Remove supported token
     */
    function removeSupportedToken(address _token) external onlyOwner {
        supportedTokens[_token] = false;
        emit TokenRemoved(_token);
    }
    
    /**
     * @dev Update platform fee
     */
    function updatePlatformFee(uint256 _newFee) external onlyOwner {
        require(_newFee <= 1000, "Fee too high"); // Max 10%
        platformFee = _newFee;
        emit FeeUpdated(_newFee);
    }
    
    /**
     * @dev Create and process payment
     */
    function processPayment(
        address _merchant,
        uint256 _amount,
        address _token,
        string calldata _paymentId,
        string calldata _metadata
    ) external nonReentrant returns (bytes32) {
        require(_merchant != address(0), "Invalid merchant");
        require(_amount > 0, "Invalid amount");
        require(supportedTokens[_token], "Token not supported");
        
        // Generate payment hash
        bytes32 paymentHash = keccak256(
            abi.encodePacked(
                msg.sender,
                _merchant,
                _amount,
                _token,
                _paymentId,
                block.timestamp
            )
        );
        
        require(payments[paymentHash].timestamp == 0, "Payment exists");
        
        // Transfer tokens from payer to contract
        IERC20 token = IERC20(_token);
        require(
            token.transferFrom(msg.sender, address(this), _amount),
            "Transfer failed"
        );
        
        // Calculate fees
        uint256 fee = (_amount * platformFee) / FEE_DENOMINATOR;
        uint256 merchantAmount = _amount - fee;
        
        // Store payment
        payments[paymentHash] = Payment({
            payer: msg.sender,
            merchant: _merchant,
            amount: _amount,
            token: _token,
            paymentId: _paymentId,
            metadata: _metadata,
            status: PaymentStatus.COMPLETED,
            timestamp: block.timestamp
        });
        
        // Update merchant balance
        merchantBalances[_merchant][_token] += merchantAmount;
        
        emit PaymentCreated(
            paymentHash,
            msg.sender,
            _merchant,
            _amount,
            _token,
            _paymentId
        );
        
        emit PaymentCompleted(paymentHash, merchantAmount, fee);
        
        return paymentHash;
    }
    
    /**
     * @dev Process ETH payment (for Base ETH)
     */
    function processEthPayment(
        address _merchant,
        string calldata _paymentId,
        string calldata _metadata
    ) external payable nonReentrant returns (bytes32) {
        require(_merchant != address(0), "Invalid merchant");
        require(msg.value > 0, "Invalid amount");
        
        address weth = address(0); // ETH represented as zero address
        
        bytes32 paymentHash = keccak256(
            abi.encodePacked(
                msg.sender,
                _merchant,
                msg.value,
                weth,
                _paymentId,
                block.timestamp
            )
        );
        
        require(payments[paymentHash].timestamp == 0, "Payment exists");
        
        uint256 fee = (msg.value * platformFee) / FEE_DENOMINATOR;
        uint256 merchantAmount = msg.value - fee;
        
        payments[paymentHash] = Payment({
            payer: msg.sender,
            merchant: _merchant,
            amount: msg.value,
            token: weth,
            paymentId: _paymentId,
            metadata: _metadata,
            status: PaymentStatus.COMPLETED,
            timestamp: block.timestamp
        });
        
        merchantBalances[_merchant][weth] += merchantAmount;
        
        emit PaymentCreated(
            paymentHash,
            msg.sender,
            _merchant,
            msg.value,
            weth,
            _paymentId
        );
        
        emit PaymentCompleted(paymentHash, merchantAmount, fee);
        
        return paymentHash;
    }
    
    /**
     * @dev Refund payment (only owner or merchant)
     */
    function refundPayment(bytes32 _paymentHash) external nonReentrant {
        Payment storage payment = payments[_paymentHash];
        require(payment.timestamp > 0, "Payment not found");
        require(
            payment.status == PaymentStatus.COMPLETED,
            "Invalid status"
        );
        require(
            msg.sender == owner() || msg.sender == payment.merchant,
            "Unauthorized"
        );
        
        uint256 refundAmount = payment.amount;
        
        if (payment.token == address(0)) {
            // ETH refund
            (bool success, ) = payment.payer.call{value: refundAmount}("");
            require(success, "ETH refund failed");
        } else {
            // ERC20 refund
            IERC20(payment.token).transfer(payment.payer, refundAmount);
        }
        
        // Deduct from merchant balance if already added
        uint256 fee = (refundAmount * platformFee) / FEE_DENOMINATOR;
        uint256 merchantAmount = refundAmount - fee;
        merchantBalances[payment.merchant][payment.token] -= merchantAmount;
        
        payment.status = PaymentStatus.REFUNDED;
        
        emit PaymentRefunded(_paymentHash, refundAmount);
    }
    
    /**
     * @dev Withdraw merchant funds
     */
    function withdrawFunds(address _token, uint256 _amount) external nonReentrant {
        require(_amount > 0, "Invalid amount");
        require(
            merchantBalances[msg.sender][_token] >= _amount,
            "Insufficient balance"
        );
        
        merchantBalances[msg.sender][_token] -= _amount;
        
        if (_token == address(0)) {
            // ETH withdrawal
            (bool success, ) = msg.sender.call{value: _amount}("");
            require(success, "ETH withdrawal failed");
        } else {
            // ERC20 withdrawal
            IERC20(_token).transfer(msg.sender, _amount);
        }
        
        emit FundsWithdrawn(msg.sender, _token, _amount);
    }
    
    /**
     * @dev Get payment details
     */
    function getPayment(bytes32 _paymentHash) external view returns (Payment memory) {
        return payments[_paymentHash];
    }
    
    /**
     * @dev Get merchant balance
     */
    function getMerchantBalance(address _merchant, address _token) external view returns (uint256) {
        return merchantBalances[_merchant][_token];
    }
    
    /**
     * @dev Check if token is supported
     */
    function isTokenSupported(address _token) external view returns (bool) {
        return supportedTokens[_token];
    }
    
    /**
     * @dev Withdraw platform fees (only owner)
     */
    function withdrawPlatformFees(address _token, uint256 _amount) external onlyOwner {
        if (_token == address(0)) {
            (bool success, ) = owner().call{value: _amount}("");
            require(success, "ETH transfer failed");
        } else {
            IERC20(_token).transfer(owner(), _amount);
        }
    }
    
    receive() external payable {}
}
