// SPDX-License-Identifier: MIT


pragma solidity 0.8.17;

import "./Ownable.sol";
import "./ERC1155.sol";


contract NFT1155 is ERC1155, Ownable {
    
  string public name;
  string public symbol;
  uint public maxId;

  mapping(uint => string) public tokenURI;

  constructor() ERC1155("") {
    name = "DegreeTech";
    symbol = "DTM";
  }

  function mint(address _to, uint _id, uint _amount, string memory _uri) external onlyOwner {
    
    require(

            _id > maxId,

            "A token with this ID already exists in this smart contract!"

        );
    
    _mint(_to, _id, _amount, "");
    tokenURI[_id] = _uri;
    maxId = _id;
    emit URI(_uri, _id);
  }

  function mintBatch(address _to, uint[] memory _ids, uint[] memory _amounts) external onlyOwner {
    _mintBatch(_to, _ids, _amounts, "");
  }

  function burn(uint _id, uint _amount) external {
    _burn(msg.sender, _id, _amount);
  }

  function burnBatch(uint[] memory _ids, uint[] memory _amounts) external {
    _burnBatch(msg.sender, _ids, _amounts);
  }

  function burnForMint(address _from, uint[] memory _burnIds, uint[] memory _burnAmounts, uint[] memory _mintIds, uint[] memory _mintAmounts) external onlyOwner {
    _burnBatch(_from, _burnIds, _burnAmounts);
    _mintBatch(_from, _mintIds, _mintAmounts, "");
  }

  function setURI(uint _id, string memory _uri) external onlyOwner {
    tokenURI[_id] = _uri;
    emit URI(_uri, _id);
  }

  function uri(uint _id) public override view returns (string memory) {
    return tokenURI[_id];
  }

}