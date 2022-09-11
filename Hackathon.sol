// SPDX-License-Identifier: MIT


pragma solidity 0.8.17;

import "./Ownable.sol";
import "./ERC1155.sol";
// Производиться привязка параметров необходимых для функционирования стандарта ERC1155

contract NFT1155 is ERC1155, Ownable {
    
  string public name;
  string public symbol;
  uint public maxId;

  mapping(uint => string) public tokenURI;
// Создание связей и их отслеживание
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
// Создание токена
// Привязка ID к токену
//Количество созданных токенов
// Привязка URI к токену
  function mintBatch(address _to, uint[] memory _ids, uint[] memory _amounts) external onlyOwner {
    _mintBatch(_to, _ids, _amounts, "");
  }
// Чеканка токенов
  function burn(uint _id, uint _amount) external {
    _burn(msg.sender, _id, _amount);
  }
// Возможность сжечь ткен
  function burnBatch(uint[] memory _ids, uint[] memory _amounts) external {
    _burnBatch(msg.sender, _ids, _amounts);
  }

  function burnForMint(address _from, uint[] memory _burnIds, uint[] memory _burnAmounts, uint[] memory _mintIds, uint[] memory _mintAmounts) external onlyOwner {
    _burnBatch(_from, _burnIds, _burnAmounts);
    _mintBatch(_from, _mintIds, _mintAmounts, "");
  }
// Возможность сжечь уже существующий токен
  function setURI(uint _id, string memory _uri) external onlyOwner {
    tokenURI[_id] = _uri;
    emit URI(_uri, _id);
  // Привязка UrI к определённому токену
  function uri(uint _id) public override view returns (string memory) {
    return tokenURI[_id];
  }
// Воможность увидеть URI по ID токена
}