// Import the HelloWorld contract...
const prescription = artifacts.require("Prescription");

module.exports = (deployer) => {
  // Deploy it!
  deployer.deploy(prescription,"some medicine",'0x6313596Ec2991b296C96760E3A7989C550A49b2a');
}
