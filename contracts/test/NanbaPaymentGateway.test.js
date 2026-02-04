const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("NanbaPaymentGateway", function () {
  let gateway;
  let owner, merchant, payer;
  
  beforeEach(async function () {
    [owner, merchant, payer] = await ethers.getSigners();
    
    const NanbaPaymentGateway = await ethers.getContractFactory("NanbaPaymentGateway");
    gateway = await NanbaPaymentGateway.deploy();
    await gateway.waitForDeployment();
  });
  
  describe("Deployment", function () {
    it("Should set the right owner", async function () {
      expect(await gateway.owner()).to.equal(owner.address);
    });
    
    it("Should have correct platform fee (2.5%)", async function () {
      expect(await gateway.platformFee()).to.equal(250);
    });
  });
  
  describe("Token Management", function () {
    it("Should add supported token", async function () {
      const mockToken = ethers.Wallet.createRandom().address;
      await gateway.addSupportedToken(mockToken);
      expect(await gateway.isTokenSupported(mockToken)).to.be.true;
    });
    
    it("Should remove supported token", async function () {
      const mockToken = ethers.Wallet.createRandom().address;
      await gateway.addSupportedToken(mockToken);
      await gateway.removeSupportedToken(mockToken);
      expect(await gateway.isTokenSupported(mockToken)).to.be.false;
    });
  });
  
  describe("ETH Payments", function () {
    it("Should process ETH payment", async function () {
      const paymentId = "test-payment-1";
      const metadata = "Test payment";
      const amount = ethers.parseEther("1.0");
      
      const tx = await gateway.connect(payer).processEthPayment(
        merchant.address,
        paymentId,
        metadata,
        { value: amount }
      );
      
      await expect(tx)
        .to.emit(gateway, "PaymentCreated")
        .withArgs(
          await gateway.payments(0),
          payer.address,
          merchant.address,
          amount,
          ethers.ZeroAddress,
          paymentId
        );
    });
  });
});
