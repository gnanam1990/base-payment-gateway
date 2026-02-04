const hre = require("hardhat");

async function main() {
  console.log("🚀 Deploying NanbaPaymentGateway...");
  
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying with account:", deployer.address);
  
  const balance = await hre.ethers.provider.getBalance(deployer.address);
  console.log("Account balance:", hre.ethers.formatEther(balance), "ETH");
  
  // Deploy contract
  const NanbaPaymentGateway = await hre.ethers.getContractFactory("NanbaPaymentGateway");
  const gateway = await NanbaPaymentGateway.deploy();
  
  await gateway.waitForDeployment();
  
  const address = await gateway.getAddress();
  console.log("✅ Contract deployed to:", address);
  console.log("📊 Network:", hre.network.name);
  
  // Add supported tokens (Base Sepolia test tokens)
  if (hre.network.name === "baseSepolia") {
    console.log("📝 Adding test tokens...");
    
    // USDC on Base Sepolia
    const usdcAddress = "0x036CbD53842c5426634e7929541eC2318f3dCF7e";
    await gateway.addSupportedToken(usdcAddress);
    console.log("✅ Added USDC:", usdcAddress);
  }
  
  console.log("\n📋 Deployment Summary:");
  console.log("====================");
  console.log("Contract:", address);
  console.log("Network:", hre.network.name);
  console.log("Owner:", deployer.address);
  console.log("Platform Fee: 2.5%");
  
  // Save deployment info
  const fs = require("fs");
  const deploymentInfo = {
    contract: "NanbaPaymentGateway",
    address: address,
    network: hre.network.name,
    deployer: deployer.address,
    timestamp: new Date().toISOString()
  };
  
  fs.writeFileSync(
    "deployment.json",
    JSON.stringify(deploymentInfo, null, 2)
  );
  
  console.log("\n💾 Deployment info saved to deployment.json");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ Deployment failed:", error);
    process.exit(1);
  });
